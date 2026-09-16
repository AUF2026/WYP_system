"""
WYP public HTTP gateway.

AUF2026 / WYP_system

This module exposes the public WYP HTTP interface and forwards
solver requests to the protected AOS PRIVATE CORE.

The public repository contains no protected solver implementation.

Architecture:

    PUBLIC WYP
        |
        | HTTP request
        v
    PUBLIC GATEWAY
        |
        | HTTPS
        v
    AOS PRIVATE CORE
        |
        | protected execution
        v
    RESPONSE

No proprietary resolver, mathematical logic or private-core
implementation is executed by this public module.
"""

from __future__ import annotations

import json
import os
from http.client import HTTPResponse
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HOST = os.getenv(
    "WYP_HOST",
    "127.0.0.1",
)

PORT = int(
    os.getenv(
        "PORT",
        os.getenv(
            "WYP_PORT",
            "8000",
        ),
    )
)

PRIVATE_API_URL = os.getenv(
    "WYP_PRIVATE_API_URL",
    "",
).rstrip("/")

CORS_ORIGIN = os.getenv(
    "WYP_CORS_ORIGIN",
    "*",
)

REQUEST_TIMEOUT = float(
    os.getenv(
        "WYP_API_TIMEOUT",
        "30",
    )
)


class WYPRequestHandler(BaseHTTPRequestHandler):
    """
    Public HTTP gateway for WYP.

    This handler does not execute the protected solver.

    Requests are forwarded to the AOS PRIVATE CORE API.
    """

    server_version = "WYP-Gateway/1.0"

    def _send_cors_headers(self) -> None:
        """Send CORS headers for the public WYP interface."""

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
        """Send a JSON response."""

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
        """
        Return public gateway status.

        This endpoint does not expose private-core implementation
        details or configuration.
        """

        if self.path != "/":
            self._send_json(
                404,
                {
                    "status": "NOT_FOUND",
                    "service": "WYP",
                },
            )

            return

        private_configured = bool(
            PRIVATE_API_URL
        )

        self._send_json(
            200,
            {
                "status": "ONLINE",
                "service": "WYP",
                "gateway": "PUBLIC",
                "private_core": (
                    "CONFIGURED"
                    if private_configured
                    else "NOT_CONFIGURED"
                ),
                "system": (
                    "What's Your Problem? "
                    "It's Deterministically Solved!"
                ),
            },
        )

    def do_POST(self) -> None:
        """
        Forward a WYP solve request to the protected AOS API.

        The public gateway does not interpret or solve the problem.
        """

        if self.path != "/solve":
            self._send_json(
                404,
                {
                    "status": "NOT_FOUND",
                    "service": "WYP",
                },
            )

            return

        if not PRIVATE_API_URL:
            self._send_json(
                503,
                {
                    "status": "PRIVATE_CORE_UNAVAILABLE",
                    "error": (
                        "The protected AOS API endpoint "
                        "is not configured."
                    ),
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

            if not isinstance(
                payload,
                dict,
            ):
                raise TypeError(
                    "Request JSON must be an object."
                )

            request_body = json.dumps(
                payload,
                ensure_ascii=False,
            ).encode("utf-8")

            private_url = (
                f"{PRIVATE_API_URL}/solve"
            )

            request = Request(
                private_url,
                data=request_body,
                method="POST",
                headers={
                    "Content-Type": (
                        "application/json"
                    ),
                    "Accept": (
                        "application/json"
                    ),
                },
            )

            with urlopen(
                request,
                timeout=REQUEST_TIMEOUT,
            ) as response:

                response_body = response.read()

                response_status = (
                    response.status
                )

                response_content_type = (
                    response.headers.get(
                        "Content-Type",
                        "application/json",
                    )
                )

            try:
                response_payload = json.loads(
                    response_body.decode("utf-8")
                )

            except (
                UnicodeDecodeError,
                json.JSONDecodeError,
            ):
                self._send_json(
                    502,
                    {
                        "status": "INVALID_PRIVATE_RESPONSE",
                        "error": (
                            "The protected core "
                            "returned an invalid "
                            "JSON response."
                        ),
                    },
                )

                return

            if not isinstance(
                response_payload,
                dict,
            ):
                self._send_json(
                    502,
                    {
                        "status": "INVALID_PRIVATE_RESPONSE",
                        "error": (
                            "The protected core "
                            "returned an invalid "
                            "response object."
                        ),
                    },
                )

                return

            self.send_response(
                response_status
            )

            self.send_header(
                "Content-Type",
                response_content_type,
            )

            self.send_header(
                "Content-Length",
                str(len(response_body)),
            )

            self._send_cors_headers()

            self.end_headers()

            self.wfile.write(
                response_body
            )

        except HTTPError as exc:
            self._handle_private_http_error(
                exc
            )

        except URLError:
            self._send_json(
                502,
                {
                    "status": "PRIVATE_CORE_UNAVAILABLE",
                    "error": (
                        "Unable to reach "
                        "the protected AOS API."
                    ),
                },
            )

        except TimeoutError:
            self._send_json(
                504,
                {
                    "status": "PRIVATE_CORE_TIMEOUT",
                    "error": (
                        "The protected AOS API "
                        "did not respond in time."
                    ),
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
                502,
                {
                    "status": "PRIVATE_CORE_ERROR",
                    "error": (
                        "Protected solver execution "
                        "could not be completed."
                    ),
                },
            )

    def _handle_private_http_error(
        self,
        error: HTTPError,
    ) -> None:
        """
        Forward a structured HTTP error from the private API
        without exposing private implementation details.
        """

        try:
            body = error.read()

            payload = json.loads(
                body.decode("utf-8")
            )

            if isinstance(
                payload,
                dict,
            ):
                self._send_json(
                    error.code,
                    payload,
                )

                return

        except Exception:
            pass

        self._send_json(
            502,
            {
                "status": "PRIVATE_CORE_ERROR",
                "error": (
                    "The protected AOS API "
                    "returned an error."
                ),
            },
        )

    def log_message(
        self,
        format: str,
        *args: Any,
    ) -> None:
        """Keep HTTP logging concise."""

        print(
            f"[WYP] {self.address_string()} "
            f"- {format % args}"
        )


def create_server(
    host: str = HOST,
    port: int = PORT,
) -> HTTPServer:
    """Create the public WYP gateway."""

    return HTTPServer(
        (host, port),
        WYPRequestHandler,
    )


def main() -> None:
    """Start the public WYP gateway."""

    server = create_server()

    print(
        "WYP PUBLIC GATEWAY ONLINE — "
        f"http://{HOST}:{PORT}"
    )

    print(
        "WYP SOLVE ENDPOINT — "
        f"http://{HOST}:{PORT}/solve"
    )

    if PRIVATE_API_URL:
        print(
            "WYP PRIVATE CORE — CONFIGURED"
        )

    else:
        print(
            "WYP PRIVATE CORE — "
            "NOT CONFIGURED"
        )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print(
            "\nWYP PUBLIC GATEWAY SHUTDOWN"
        )

    finally:
        server.server_close()


if __name__ == "__main__":
    main()
