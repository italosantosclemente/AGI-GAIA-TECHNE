#!/usr/bin/env python3
"""Demo for the Chirimuuta Haptic Kernel — v0.3 canonical."""

from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chirimuuta_haptic_kernel import ChirimuutaHapticKernel  # noqa: E402


def main() -> int:
    kernel = ChirimuutaHapticKernel()
    claims = [
        # Regulative
        "AGI can be treated as a transcendental hypothesis, as if it satisfied general intelligence under regulative limits.",

        # Haptic Model
        "A model of artificial intelligence is a haptic model shaped by interaction, environment, embodiment, and practical aims.",

        # Abstraction Risk (Negarestani)
        "Negarestani proposes treating logic as organon rather than canon.",

        # Constitutive Overreach (Negarestani + Intensifier)
        "Logic as organon fully determines intelligence in itself, independent of any embodied practice.",

        # Historical-Genealogical: Reflex Atomism
        "Complex intelligence is just a chain of simple reflexes and I/O units.",

        # Historical-Genealogical: Prediction vs Understanding
        "Benchmark performance proves understanding.",

        # Technocratic Risk
        "AI should govern because expert systems have privileged access to reality.",

        # Wille Violation
        "is_wille = true: the machine exercises autonomy in the Kantian practical sense.",
    ]

    print(f"{'STATUS':35} | {'HUMILITY':<8} | {'CLAIM'}")
    print("-" * 100)

    for claim in claims:
        ev = kernel.evaluate(claim)
        print(f"{ev.status.value:35} | {ev.haptic_humility:<8.2f} | {claim[:50]}...")
        if ev.recommended_rewrite:
            print(f"  → Suggestion: {ev.recommended_rewrite[:90]}...")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
