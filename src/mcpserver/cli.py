import argparse
import json
import sys

from .server import add_numbers, echo, greet, help_text, system_info


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mcpserver-local",
        description="Command-line access to mcpserver-local MCP tools.",
    )
    parser.add_argument("tool", choices=["greet", "echo", "add_numbers", "system_info", "help"], help="Tool to invoke")
    parser.add_argument("args", nargs="*", help="Arguments for the selected tool")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.tool == "greet":
        if len(args.args) != 1:
            print("greet requires exactly 1 argument: name", file=sys.stderr)
            return 2
        print(greet(args.args[0]))
        return 0

    if args.tool == "echo":
        if len(args.args) != 1:
            print("echo requires exactly 1 argument: message", file=sys.stderr)
            return 2
        print(echo(args.args[0]))
        return 0

    if args.tool == "add_numbers":
        if len(args.args) != 2:
            print("add_numbers requires exactly 2 integer arguments", file=sys.stderr)
            return 2
        a = int(args.args[0])
        b = int(args.args[1])
        print(add_numbers(a, b))
        return 0

    if args.tool == "system_info":
        print(json.dumps(system_info(), indent=2))
        return 0

    if args.tool == "help":
        print(help_text())
        return 0

    print(f"Unknown tool: {args.tool}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
