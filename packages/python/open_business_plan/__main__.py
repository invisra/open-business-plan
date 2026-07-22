"""Command-line entry point: parse business-plan JSON files and report results.

Usage::

    python -m open_business_plan file.json [file2.json ...]

Prints a check mark and exits 0 when every file parses, or lists validation
errors and exits 1 otherwise.
"""

from __future__ import annotations

import sys

from pydantic import ValidationError

from . import load_business_plan_file


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("Usage: python -m open_business_plan <file.json> [file2.json ...]", file=sys.stderr)
        return 2

    all_valid = True
    for path in args:
        try:
            plan = load_business_plan_file(path)
            print(f"✔ {path} is a valid business plan ({plan.name})")
        except ValidationError as err:
            all_valid = False
            print(f"✘ {path} is invalid:")
            for error in err.errors():
                location = ".".join(str(part) for part in error["loc"]) or "(root)"
                print(f"  - {location}: {error['msg']}")
        except (OSError, ValueError) as err:
            all_valid = False
            print(f"✘ {path} could not be read/parsed: {err}")

    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
