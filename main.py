"""Entry point demonstrating the Friday AI workflow."""

import module1
import module2
import module3


def main() -> None:
    """Run the startup, runtime, and boot phases sequentially."""

    module1.start()
    module2.run()
    module3.boot()


if __name__ == "__main__":
    main()
