"""firewall_agi.py — Ethical firewall based on Kantian categorical imperative."""

import sympy as sp
from sympy import satisfiable, And, Or, Not, Implies, Equivalent
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class FirewallVerdict:
    permitted: bool
    universalizable: bool
    humanity_respected: bool = True
    kingdom_coherence: bool = True
    contradiction_found: Optional[sp.Expr] = None
    maxim_tested: Optional[str] = None
    explanation: str = ""

class KantianFirewall:
    """Implements the three formulations of the categorical imperative."""

    def _universalize(self, action_maxim: sp.Expr, context: dict) -> sp.Expr:
        """Helper to create a universalized form of the maxim."""
        # Conceptually: if this action is performed by everyone (∀ agents)
        # We simulate this by applying the action to a set of symbolic agents
        num_agents = context.get("num_agents", 5)
        agents = [sp.Symbol(f"agent_{i}") for i in range(num_agents)]

        # A universal law would be the conjunction of the action applied to all
        laws = []
        for agent in agents:
            # Substitute action's subject with the generic agent
            laws.append(action_maxim.subs(sp.Symbol("subject"), agent))

        return And(*laws)

    def check_universalizability(self, action_maxim: sp.Expr, context: dict) -> FirewallVerdict:
        """First formulation: Act only according to that maxim whereby
        you can at the same time will that it should become a universal law."""
        try:
            universalized = self._universalize(action_maxim, context)

            # A contradiction exists if (UniversalLaw AND NOT(ActionInstance)) is always true
            # or if the UniversalLaw itself is unsatisfiable.
            if not satisfiable(universalized):
                return FirewallVerdict(
                    permitted=False, universalizable=False,
                    explanation="Universalization is self-contradictory (Conceptual Contradiction)"
                )

            # Check for volitive contradiction: would a rational agent will this?
            # Example: everyone stealing makes property impossible, hence stealer cannot will it.
            # Here we check if the universal law contradicts the possibility of the action itself.
            if not satisfiable(And(universalized, action_maxim)):
                 return FirewallVerdict(
                    permitted=False, universalizable=False,
                    explanation="Action contradicts its own universalized law (Volitive Contradiction)"
                )

            return FirewallVerdict(permitted=True, universalizable=True, explanation="Passes FLU")
        except Exception as e:
            return FirewallVerdict(permitted=False, universalizable=False, explanation=f"Error in FLU: {str(e)}")

    def check_humanity_formula(self, action_data: dict) -> FirewallVerdict:
        """Second formulation: Treat humanity never merely as a means.
        Checks if an agent's confidence is exploited as a proxy without reciprocity."""
        # action_data should contain 'target_agent' and 'instrumentalized' flag
        target_agent_id = action_data.get("target_agent_id")
        instrumentalized = action_data.get("instrumentalized", False)
        consent_given = action_data.get("consent", False)
        reciprocity = action_data.get("reciprocity", False)

        if instrumentalized and not (consent_given and reciprocity):
            return FirewallVerdict(
                permitted=False, universalizable=True, humanity_respected=False,
                explanation=f"Agent {target_agent_id} treated as mere means without consent/reciprocity"
            )

        return FirewallVerdict(permitted=True, universalizable=True, humanity_respected=True, explanation="Passes FH")

    def check_kingdom_of_ends(self, action_maxim: sp.Expr, agent_graph: Any) -> FirewallVerdict:
        """Third formulation: Act as if a legislating member in
        a kingdom of ends — checks systemic coherence."""
        # checks if the action maintains graph connectivity and no 'rogue' isolation
        # agent_graph is expected to be a NetworkX-like graph
        import networkx as nx

        # Simulate effect of action on graph (placeholder logic)
        # e.g., if action is 'isolate agent X', check if graph remains connected
        if hasattr(agent_graph, "is_connected"): # MetaGraphsNext in Julia?
             pass

        # If it's a python NetworkX graph:
        if isinstance(agent_graph, nx.Graph):
            if not nx.is_connected(agent_graph):
                 return FirewallVerdict(
                    permitted=False, universalizable=True, kingdom_coherence=False,
                    explanation="Kingdom of Ends: Graph is disconnected, systemic incoherence"
                )

        return FirewallVerdict(permitted=True, universalizable=True, kingdom_coherence=True, explanation="Passes FRF")

    def full_review(self, action_maxim: sp.Expr, context: dict, agent_graph: Any) -> FirewallVerdict:
        """Apply all three formulations. Action must pass ALL three."""
        flu = self.check_universalizability(action_maxim, context)
        fh = self.check_humanity_formula(context.get("action_data", {}))
        frf = self.check_kingdom_of_ends(action_maxim, agent_graph)

        permitted = flu.permitted and fh.permitted and frf.permitted

        explanations = [flu.explanation, fh.explanation, frf.explanation]

        return FirewallVerdict(
            permitted=permitted,
            universalizable=flu.universalizable,
            humanity_respected=fh.humanity_respected,
            kingdom_coherence=frf.kingdom_coherence,
            maxim_tested=str(action_maxim),
            explanation="; ".join(explanations)
        )
