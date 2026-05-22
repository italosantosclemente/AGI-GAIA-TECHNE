#!/usr/bin/env python3

import argparse
from src.agt.axioms import (
    IS_WILLE,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
    AGI_AS_TRANSCENDENTAL_HYPOTHESIS,
)


def print_critical_generality_rule() -> None:
    assert IS_WILLE is False
    assert MACHINE_HAS_GEWISSEN is False
    assert NO_GLOBAL_AUFHEBUNG is True
    assert AGI_AS_TRANSCENDENTAL_HYPOTHESIS is True

    print("AGI-GAIA-TECHNE Constitutional Rule: Critical Generality")
    print()
    print("Status: VALID")
    print()
    print(
        "The system may be called a critical general intelligence "
        "only in the regulative sense."
    )
    print()
    print("It audits any AGI claim.")
    print("It does not become an artificial soul.")
    print("It does not possess Wille.")
    print("It does not possess Gewissen.")
    print("It does not legislate morally.")
    print()
    print("Conclusion:")
    print("Critical generality is permitted.")
    print("Constitutive AGI is forbidden.")
    print("Werk, never Wille.")


def main():
    parser = argparse.ArgumentParser(description="AGI-GAIA-TECHNE Constitutional CLI")
    parser.add_argument("--rule", choices=["critical-generality"], default="critical-generality",
                        help="View a specific constitutional rule.")

    args = parser.parse_args()

    if args.rule == "critical-generality":
        print_critical_generality_rule()

if __name__ == "__main__":
    main()
