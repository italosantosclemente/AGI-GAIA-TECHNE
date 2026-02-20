import unittest
import sympy as sp
from src.firewall_agi.firewall_agi import KantianFirewall
from src.automato_resolver.automato_resolver import AutomatoResolver

class TestV7Python(unittest.TestCase):
    def test_firewall_universalizability(self):
        firewall = KantianFirewall()
        # Maxim: Always tell the truth
        # In this simple model, we use a symbol to represent the truth-telling action
        maxim = sp.Symbol("truth")
        context = {"num_agents": 3}
        verdict = firewall.check_universalizability(maxim, context)
        self.assertTrue(verdict.permitted)

    def test_automato_resolution(self):
        resolver = AutomatoResolver(n_agents=5)
        problem = sp.sympify("x + y")
        solutions = resolver.resolve(problem, mode="auseinandersetzung")
        self.assertGreater(len(solutions), 0)
        resolver.shutdown()

if __name__ == "__main__":
    unittest.main()
