"""Command line interface for chatting with Friday."""
from __future__ import annotations

import argparse
import sys
from typing import Iterable

from .engine import FridayBrain


def chat_loop(brain: FridayBrain, *, stream: Iterable[str] = None) -> None:
    """Run an interactive chat loop with the provided Friday brain."""
    input_stream = iter(stream) if stream is not None else None
    print("🔥 Friday się budzi. Napisz coś albo wciśnij Ctrl+C, żeby zakończyć.")
    try:
        while True:
            if input_stream is None:
                prompt = input("Ty > ")
            else:
                try:
                    prompt = next(input_stream)
                except StopIteration:
                    break
            response = brain.respond(prompt)
            print(f"Friday > {response}")
    except KeyboardInterrupt:
        print("\nFriday > Elo, widzimy się następnym razem.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Uruchom Friday w wersji CLI.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Ustal ziarno generatora odpowiedzi, żeby uzyskać powtarzalne konwersacje.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    brain = FridayBrain(seed=args.seed)
    chat_loop(brain)
    return 0


if __name__ == "__main__":
    sys.exit(main())
