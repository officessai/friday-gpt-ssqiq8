"""HuAI v1 demonstration script."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from huai import HuAIContext, HuAIOrchestrator


def main() -> None:
    orchestrator = HuAIOrchestrator()
    context = HuAIContext(
        user_input="Design a customer onboarding assistant with a simple rollout plan."
    )
    result = orchestrator.run(context)

    for line in result.trace:
        print(line)

    print("\n=== Final Response ===")
    print(result.text)


if __name__ == "__main__":
    main()
