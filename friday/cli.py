"""Command line interface for chatting with Friday."""
from __future__ import annotations

import argparse
from pathlib import Path

from .bot import FridayBot
from .config import load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Odpal Friday'ego w terminalu.")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Ścieżka do config.json z niestandardowymi tekstami.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = load_config(args.config)
    bot = FridayBot(config)

    print("Friday: Siema! Żeby mnie obudzić, rzuć hasło-wake word.")

    try:
        while True:
            user_input = input("Ty: ")
            response = bot.handle_message(user_input)
            print(f"Friday: {response}")
    except (KeyboardInterrupt, EOFError):
        print("\nFriday: Spadam, trzymaj się!")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

