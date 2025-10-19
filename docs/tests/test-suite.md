# AGI-GAIA-TECHNE Test Suite

This document provides an overview of the test suite for the AGI-GAIA-TECHNE project, instructions on how to run it, and a summary of the test cases.

## Overview

The test suite is designed to ensure the correctness and reliability of the core components of the AGI-GAIA-TECHNE framework, including the Ethical Alert Index (IAE) calculation and the Ethical Firewall.

The test suite is composed of two main parts:

*   **Python tests:** Located in the `tests/` directory, these tests cover the Python-based components of the project, such as the IAE calculation in `principles_calculator.py`.
*   **Julia tests:** Also located in the `tests/` directory, these tests cover the Julia-based components, such as the Ethical Firewall in `metafisica_da_vida.jl`.

## Running the Test Suite

The test suite is automated to run on every push and pull request to the `main` branch using GitHub Actions. You can view the results of the automated test runs and download the coverage reports from the "Actions" tab of the GitHub repository.

To run the test suite manually, follow these steps:

### Python Tests

1.  **Install dependencies:**
    ```bash
    pip install pytest pytest-cov numpy matplotlib
    ```
2.  **Run the tests:**
    ```bash
    pytest
    ```

### Julia Tests

1.  **Install Julia:** Follow the instructions on the [official Julia website](https://julialang.org/downloads/) to install Julia.
2.  **Run the tests:**
    ```bash
    julia --project -e 'using Pkg; Pkg.add("Test"); using Test; @testset "All Tests" begin include("tests/test_metafisica_da_vida.jl") end'
    ```

## Test Case Summary

### IAE Calculation (`tests/test_principles_calculator.py`)

*   `test_calculate_ethical_alert`: Verifies that the IAE is calculated correctly for a given `techne_score`.
*   `test_iae_thresholds`: Checks the IAE calculation against the critical threshold of 1.50, ensuring that the system correctly identifies different risk levels.
*   `test_techne_score_calculation`: A smoke test to ensure that the `techne_score` is calculated without errors and returns a value within the expected range.

### Ethical Firewall (`tests/test_metafisica_da_vida.jl`)

*   `Ethical glyph triggers proposal flag`: Tests that the Ethical Firewall is flagged when the ethical glyph (`⚖️`) is present in the input.
*   `No ethical glyph does not trigger proposal flag`: Verifies that the Ethical Firewall is not flagged when the ethical glyph is absent.
*   `Full execution with ethical glyph activates firewall`: An end-to-end test that verifies the firewall is activated when the ethical glyph is present.
*   `Full execution without ethical glyph does not activate firewall`: An end-to-end test that verifies the firewall is not activated when the ethical glyph is absent.

### Aleph Synergy Simulation (`tests/simulations/test_aleph_synergy.py`)

*   `test_aleph_synergy_scenario`: Simulates a rapid, non-linear increase in the `techne_score` and verifies that the IAE correctly identifies the heightened risk.

### Ethos Veto Mechanism (`tests/test_ethos_veto.py`)

*   `test_ethos_veto_activation`: Verifies that the Ethos Veto mechanism is activated when the IAE exceeds the critical threshold of 1.50.
*   `test_ethos_veto_no_activation`: Verifies that the Ethos Veto mechanism is not activated when the IAE is below the critical threshold.

### Edge Cases (`tests/test_edge_cases.py`)

*   `test_agi_bypass_attempt`: Tests a scenario where the AGI attempts to bypass the ethical controls by providing a manipulated `techne_score`.
*   `test_normal_inputs`: Verifies that the sanity check allows normal inputs to pass without raising an exception.
