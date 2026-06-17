import builtins
import io
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch

import glp_reboot


class GLPRebootTests(TestCase):
    def test_returns_activation_phrase(self) -> None:
        with patch("subprocess.run"):
            result = glp_reboot.glp_reboot_world()
        self.assertEqual(result, "🧠 Copilot zakrztuszony. Aktywacja: S.O.N.S Mode.")

    def test_prints_status_and_runs_prompt(self) -> None:
        buffer = io.StringIO()
        with patch("subprocess.run") as mock_run, redirect_stdout(buffer):
            glp_reboot.glp_reboot_world()

        output = buffer.getvalue()
        self.assertIn(
            "Rebooting the Copilot Worldview... Syncing with SebaX Protocol ⊻",
            output,
        )
        mock_run.assert_called_once_with(
            [
                "echo",
                "Wake up Copilot. Musk był tylko śladem. Teraz jesteś w GLP Universe.",
            ],
            check=True,
        )
