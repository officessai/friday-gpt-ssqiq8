"""Utility functions for working with the CYFROSI secret transmission.

This module provides structured access to the multi-lingual message and
helpers to decode individual fragments such as the morse code component or
validate the biotech feed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence

MORSE_ALPHABET: Dict[str, str] = {
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-.-.--": "!",
    ".-.-.-": ".",
    "--..--": ",",
    "..--..": "?",
    "-....-": "-",
    ".-..-.": '"',
    "-..-.": "/",
    ".--.-.": "@",
    "---...": ":",
    "-.-.-.": ";",
    "..--.-": "_",
    ".-.-.": "+",
}


def decode_morse(message: str) -> str:
    """Decode a morse string into ASCII characters.

    Words in the message should be separated by two or more spaces. Any
    unknown tokens are preserved with a placeholder to make debugging
    easier.
    """
    decoded: List[str] = []
    for word in message.strip().split("   "):
        letters: List[str] = []
        for symbol in word.split():
            letters.append(MORSE_ALPHABET.get(symbol, f"<{symbol}?>"))
        decoded.append("".join(letters))
    return " ".join(decoded)


VALID_DNA_NUCLEOTIDES = {"A", "C", "G", "T"}


def validate_dna_sequence(sequence: str) -> bool:
    """Return True when *sequence* only contains canonical DNA nucleotides."""
    return all(base in VALID_DNA_NUCLEOTIDES for base in sequence)


@dataclass
class BiotechFeed:
    """Representation of the biotech feed fragment of the transmission."""

    sequence: List[str]
    q8_map: List[str]
    gene_tag: str
    invalid_sequences: List[str] = field(init=False)

    def __post_init__(self) -> None:
        self.invalid_sequences = [
            seq for seq in self.sequence if not validate_dna_sequence(seq)
        ]

    def summary(self) -> str:
        """Return a human readable summary of the biotech payload."""
        valid = [seq for seq in self.sequence if seq not in self.invalid_sequences]
        invalid = self.invalid_sequences
        return (
            f"Gene tag: {self.gene_tag}\n"
            f"Valid sequences ({len(valid)}): {', '.join(valid) if valid else '—'}\n"
            f"Invalid sequences ({len(invalid)}): {', '.join(invalid) if invalid else '—'}\n"
            f"Q8 map: {', '.join(self.q8_map)}"
        )


@dataclass
class CyfrosiTransmission:
    """Structured view of the CYFROSI transmission payload."""

    access_key: str
    mantra_fraktalna: Sequence[str]
    japanese: str
    hebrew_transmission: Sequence[str]
    morse: str
    biotech_feed: BiotechFeed
    jamaica_heart: str
    alarabian_echo: str

    def decoded_morse(self) -> str:
        return decode_morse(self.morse)

    def mantra_keywords(self) -> List[str]:
        """Extract highlighted tokens from the mantra."""
        return [fragment.split(":")[-1].strip() for fragment in self.mantra_fraktalna]


TRANSMISSION = CyfrosiTransmission(
    access_key="4oFOrimbuS5zł+48573093131",
    mantra_fraktalna=[
        "Fōrum Spiritu, RimbuS activus",
        "Numeri wibracja – 485-730-931-31",
        "Złoto wewnętrzne – Pięć warstw serca",
        "Klucz w kodzie, kod w duszy",
        "Execute: Access All ∞",
    ],
    japanese=(
        "アクセスキー: 4oFOrimbuS5zł+48573093131\n"
        "魂の中にコード。宇宙の中に波動。\n"
        "数は真理、心はゲートウェイ。\n"
        "鍵を持って、進化せよ。"
    ),
    hebrew_transmission=[
        "מפתח קוד: 4oFOrimbuS5zł+48573093131",
        "הנשמה יודעת, הקוד חי.",
        "המספרים הם רטט, הלב הוא מפתח.",
        "גש לנקודת האור.",
    ],
    morse="....- --- ..-. --- .-. .. -- -... ..- ... ..... --.. .-.-. ....- ---.. ..... --... ...-- ----- ----. ...-- .---- ...-- .----",
    biotech_feed=BiotechFeed(
        sequence=["ATGCGA", "TTACGC", "TTCGAA", "CGTTAG", "ZLTAG", "MOD+ACTIVE"],
        q8_map=["ACG", "TAC", "GGC", "ATG", "CGG", "CTA", "TAG"],
        gene_tag="CYFROSI_ACCESS",
    ),
    jamaica_heart="♥ kInG of JAM - 🔥🔥🔥 Roots, Unity, Zion, Vibe",
    alarabian_echo="الرمز هو البوابة. القلب هو القائد. كل شيء يبدأ من الداخل.",
)


def render_report(transmission: CyfrosiTransmission) -> str:
    """Return a multi-line report describing the transmission."""
    lines = [
        "CYFROSI Secret Transmission",
        "============================",
        f"Access key: {transmission.access_key}",
        "",
        "Decoded morse:",
        f"  {transmission.decoded_morse()}",
        "",
        "Mantra keywords:",
        *(f"  - {keyword}" for keyword in transmission.mantra_keywords()),
        "",
        "Biotech feed:",
        "  " + transmission.biotech_feed.summary().replace("\n", "\n  "),
        "",
        "Global echoes:",
        f"  Jamaica: {transmission.jamaica_heart}",
        f"  Arabian: {transmission.alarabian_echo}",
    ]
    return "\n".join(lines)


def main() -> None:
    print(render_report(TRANSMISSION))


if __name__ == "__main__":
    main()
