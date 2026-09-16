"""
WYP HTTP API server.

Exposes the existing WYP deterministic engine through
a minimal standard-library HTTP interface.

No third-party dependencies.
No binary floating-point arithmetic.
"""

from __future__ import annotations

import json
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from .api import solve


HOST = os.getenv("WYP_HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", os.getenv("WYP_PORT", "8000")))

CORS_ORIGIN = os.getenv(
    "WYP_CORS_ORIGIN",
    "http://127.0.0.1:8080",
)


class WYPRequestHandler(BaseHTTPRequestHandler):
    """HTTP interface for the WYP solver."""

    def _send_cors_headers(self) -> None:
        """Send CORS headers for the web frontend."""

        self.send_header(
            "Access-Control-Allow-Origin",
            CORS_ORIGIN,
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS",
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )

    def _send_json(
        self,
        status: int,
        payload: dict[str, Any],
    ) -> None:
        """Send a JSON HTTP response."""

        body = json.dumps(
            payload,
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(body)),
        )

        self._send_cors_headers()

        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        """Handle CORS preflight requests."""

        self.send_response(204)

        self._send_cors_headers()

        self.end_headers()

    def do_GET(self) -> None:
        """Return API status information."""

        if self.path != "/":
            self._send_json(
                404,
                {
                    "status": "NOT_FOUND",
                    "service": "WYP",
                },
            )
            return

        self._send_json(
            200,
            {
                "status": "ONLINE",
                "service": "WYP",
                "system": (
                    "What's Your Problem? "
                    "It's Deterministically Solved!"
                ),
            },
        )

    def do_POST(self) -> None:
        """Solve a WYP problem submitted as JSON."""

        if self.path != "/solve":
            self._send_json(
                404,
                {
                    "status": "NOT_FOUND",
                    "service": "WYP",
                },
            )
            return

        try:
            content_length = int(
                self.headers.get(
                    "Content-Length",
                    "0",
                )
            )

            if content_length <= 0:
                raise ValueError(
                    "Request body is empty."
                )

            raw_body = self.rfile.read(
                content_length
            )

            payload = json.loads(
                raw_body.decode("utf-8")
            )

            if not isinstance(payload, dict):
                raise TypeError(
                    "Request JSON must be an object."
                )

            problem = payload.get("problem")

            if not isinstance(problem, dict):
                raise TypeError(
                    "'problem' must be a JSON object."
                )

            result = solve(problem)

            self._send_json(
                200,
                {
                    "status": "SUCCESS",
                    "result": result,
                },
            )

        except (
            ValueError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:
            self._send_json(
                400,
                {
                    "status": "ERROR",
                    "error": str(exc),
                },
            )

        except Exception:
            self._send_json(
                500,
                {
                    "status": "ENGINE_ERROR",
                    "error": "Solver execution failed.",
                },
            )

    def log_message(
        self,
        format: str,
        *args: Any,
    ) -> None:
        """Keep standard HTTP logging concise."""

        print(
            f"[WYP] {self.address_string()} "
            f"- {format % args}"
        )


def create_server(
    host: str = HOST,
    port: int = PORT,
) -> HTTPServer:
    """Create a WYP HTTP server."""

    return HTTPServer(
        (host, port),
        WYPRequestHandler,
    )


def main() -> None:
    """Start the WYP HTTP API server."""

    server = create_server()

    print(
        f"WYP API ONLINE — "
        f"http://{HOST}:{PORT}"
    )

    print(
        f"WYP SOLVE ENDPOINT — "
        f"http://{HOST}:{PORT}/solve"
    )

    print(
        f"WYP CORS ORIGIN — "
        f"{CORS_ORIGIN}"
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nWYP API SHUTDOWN")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()
