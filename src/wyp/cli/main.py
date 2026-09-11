"""
WYP? — What's Your Problem?
It's Deterministically Solved!

Command-line interface for the WYP deterministic engine.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ..api import solve


PROGRAM_NAME = "wyp"
PROGRAM_DESCRIPTION = (
    "WYP? What's Your Problem? It's Deterministically Solved!"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="WYP 1.0.0",
    )

    parser.add_argument(
        "--problem",
        type=str,
        required=False,
        help=(
            "Problem represented as a JSON object. "
            'Example: \'{"x":"12","y":"12"}\''
        ),
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Print the result as formatted JSON.",
    )

    return parser


def _parse_problem(value: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON problem: {exc}"
        ) from exc

    if not isinstance(parsed, dict):
        raise ValueError(
            "The problem must be a JSON object."
        )

    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.problem is None:
        parser.print_help()
        return 0

    try:
        problem = _parse_problem(args.problem)
        result = solve(problem)
    except (TypeError, ValueError, KeyError) as exc:
        print(
            f"WYP ERROR: {exc}",
            file=sys.stderr,
        )
        return 1

    if args.pretty:
        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
        )
    else:
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                default=str,
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
