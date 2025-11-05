#!/usr/bin/env python3
"""Generate a deterministic "All Access Manifest" for a supplied numeric identifier.

The script produces a playful but structured manifest that can be used to
identify members of the fictional Friday / SSQiQ8 universe.  The content is
purely deterministic – re-running the script with the same identifier always
outputs the same manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from textwrap import indent


# --- Domain specific vocabulary -------------------------------------------------

FRAGMENTS = {
    "clearance": [
        "TRUST_α",
        "TRUST_β",
        "TRUST_γ",
        "TRUST_δ",
        "TRUST_ε",
        "TRUST_ζ",
        "TRUST_η",
        "TRUST_θ",
        "TRUST_λ",
        "TRUST_∞",
    ],
    "channels": [
        "CYFROSI_MAIN",
        "GLP_NEURAL_NET",
        "BERVISION",
        "SONCHAIN_ALPHA",
        "FRIDAY_DIRECT",
        "NIM_SYNC",
        "SPECTRUM_Q8",
        "HYPERLOOP",
    ],
    "domains": [
        "URBAN-OS",
        "POLY-SYNTH",
        "QUANTUM-LINK",
        "NARRATIVE-MATRIX",
        "SENSOR-NET",
        "MEMORY-STACK",
        "CORE-LOOP",
        "GRADIENT-FIELD",
    ],
    "frequencies": [
        "41.20 Hz",
        "64.00 Hz",
        "72.09 Hz",
        "80.00 Hz",
        "120.88 Hz",
        "144.00 Hz",
        "188.08 Hz",
        "256.20 Hz",
    ],
    "icons": [
        "🛸",
        "🕶️",
        "💠",
        "🌐",
        "🛰️",
        "🔁",
        "🧠",
        "⚡",
    ],
    "status": [
        "ACTIVE",
        "IDLE",
        "LISTENING",
        "REGENERATING",
        "FIELD_DEPLOYED",
        "HYPERSLEEP",
        "ARCHIVED",
        "VALIDATED",
    ],
}


@dataclass(frozen=True)
class Manifest:
    identifier: int
    checksum: str
    issued_at: datetime
    clearance: str
    access_channel: str
    domain: str
    resonance_frequency: str
    icon: str
    status: str

    def to_multiline(self) -> str:
        header = f"ALL ACCESS MANIFEST :: {self.identifier}"
        details = (
            f"Checksum         : {self.checksum}\n"
            f"Issued (UTC)     : {self.issued_at.isoformat()}\n"
            f"Clearance        : {self.clearance}\n"
            f"Access Channel   : {self.access_channel}\n"
            f"Domain Alignment : {self.domain}\n"
            f"Resonance Freq   : {self.resonance_frequency}\n"
            f"Status           : {self.status}\n"
            f"Iconography      : {self.icon}\n"
        )
        footer = "⊻ EXECUTE / Maintain gradient integrity"
        return f"{header}\n{indent(details, '  ')}\n{footer}"


# --- Utility helpers ------------------------------------------------------------


def _select(fragment_key: str, digest: bytes, offset: int) -> str:
    pool = FRAGMENTS[fragment_key]
    index = digest[offset] % len(pool)
    return pool[index]


def _render_manifest(identifier: int) -> Manifest:
    encoded = str(identifier).encode("utf-8")
    digest = hashlib.sha256(encoded).digest()
    checksum = hashlib.sha1(encoded).hexdigest()[:12].upper()

    issued_at = datetime.fromtimestamp(
        int.from_bytes(digest[:6], byteorder="big") % 2_147_483_647,
        tz=timezone.utc,
    )

    clearance = _select("clearance", digest, 0)
    access_channel = _select("channels", digest, 5)
    domain = _select("domains", digest, 11)
    resonance = _select("frequencies", digest, 17)
    icon = _select("icons", digest, 23)
    status = _select("status", digest, 29)

    return Manifest(
        identifier=identifier,
        checksum=checksum,
        issued_at=issued_at,
        clearance=clearance,
        access_channel=access_channel,
        domain=domain,
        resonance_frequency=resonance,
        icon=icon,
        status=status,
    )


# --- CLI ------------------------------------------------------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an All Access Manifest for a numeric identifier.",
    )
    parser.add_argument(
        "identifier",
        type=int,
        help="Numeric identifier to manifest (e.g. 4321888).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        manifest = _render_manifest(args.identifier)
    except ValueError as exc:  # pragma: no cover - defensive clause
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(manifest.to_multiline())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
