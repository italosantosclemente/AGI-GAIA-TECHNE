"""automato_resolver.py — Resolving the automaton problem via intersubjective emergence."""

import networkx as nx
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Any
import sympy as sp
import random

@dataclass
class AutomatonAgent:
    agent_id: str
    rules: List[Any]           # List of transition rules (callables)
    state: Dict[str, sp.Expr]   # Symbolic state variables
    symbolic_form: str          # "mythos" | "logos" | "ethos"
    confidence: float = 0.5

@dataclass
class EmergentSolution:
    solution: sp.Expr
    confidence: float
    contributing_agents: Set[str]
    verification_trace: List[str]
    admitted_failure: bool = False

def _agent_reasoning_step(agent: AutomatonAgent, problem: sp.Expr, neighbors_states: List[Dict[str, sp.Expr]]) -> EmergentSolution:
    """Independent reasoning step for a single agent."""
    # Simplified reasoning logic: agent tries to simplify or mutate the problem based on its form
    current_solution = problem
    trace = [f"Agent {agent.agent_id} started with form {agent.symbolic_form}"]

    # 1. Influência dos vizinhos (Auseinandersetzung local)
    for neighbor_state in neighbors_states:
        # If a neighbor has a state that overlaps with the problem, use it
        overlap = set(agent.state.keys()) & set(neighbor_state.keys())
        for var in overlap:
            # Simple substitution as a "influence"
            current_solution = current_solution.subs(sp.Symbol(var), neighbor_state[var])
            trace.append(f"Intersubjective update from neighbor via variable {var}")

    # 2. Aplicação de regras internas
    try:
        if agent.symbolic_form == "logos":
            current_solution = sp.simplify(current_solution)
            trace.append("Applied logical simplification")
        elif agent.symbolic_form == "mythos":
            # Mythos focuses on expansion and pattern recognition (simulated by expansion)
            current_solution = sp.expand(current_solution)
            trace.append("Applied mythical expansion")
        elif agent.symbolic_form == "ethos":
            # Ethos applies constraints (simulated by checking if expression is non-negative)
            # This is a bit arbitrary for a generic expression, but represents "valuation"
            if hasattr(current_solution, 'is_positive') and current_solution.is_positive:
                trace.append("Ethical valuation: Positive")
            else:
                trace.append("Ethical valuation: Neutral/Negative")

    except Exception as e:
        return EmergentSolution(problem, 0.0, {agent.agent_id}, [str(e)], True)

    return EmergentSolution(current_solution, agent.confidence, {agent.agent_id}, trace)

class AutomatoResolver:
    def __init__(self, topology: str = "watts_strogatz", n_agents: int = 20):
        if topology == "watts_strogatz":
            self.graph = nx.watts_strogatz_graph(n_agents, 4, 0.3)
        else:
            self.graph = nx.complete_graph(n_agents)

        self.agents: Dict[str, AutomatonAgent] = {}
        self._executor = ProcessPoolExecutor()

        # Initialize default agents
        forms = ["mythos", "logos", "ethos"]
        for i in range(n_agents):
            agent_id = str(i)
            self.agents[agent_id] = AutomatonAgent(
                agent_id=agent_id,
                rules=[],
                state={"x": sp.Symbol(f"x_{i}")},
                symbolic_form=random.choice(forms)
            )

    def resolve(self, problem: sp.Expr, mode: str = "auseinandersetzung") -> List[EmergentSolution]:
        """Parallel resolution with configurable convergence mode."""
        futures = {}
        for agent_id, agent in self.agents.items():
            neighbors_ids = list(self.graph.neighbors(int(agent_id)))
            neighbors_states = [self.agents[str(nid)].state for nid in neighbors_ids]

            future = self._executor.submit(
                _agent_reasoning_step, agent, problem, neighbors_states
            )
            futures[future] = agent_id

        solutions = []
        for future in as_completed(futures):
            try:
                result = future.result(timeout=30.0)
                solutions.append(result)
            except Exception as e:
                solutions.append(EmergentSolution(problem, 0.0, set(), [f"Error: {str(e)}"], True))

        if mode == "aufhebung":
            return [self._synthesize_convergent(solutions)]
        return self._maintain_tension(solutions)

    def _synthesize_convergent(self, solutions: List[EmergentSolution]) -> EmergentSolution:
        """Aufhebung mode: find the most common or 'simplest' solution."""
        # Weighted voting by confidence
        votes = {}
        for sol in solutions:
            if sol.admitted_failure: continue
            s_str = str(sol.solution)
            votes[s_str] = votes.get(s_str, 0) + sol.confidence

        if not votes:
            return solutions[0] # Return any if all failed

        best_sol_str = max(votes, key=votes.get)
        # Find one original solution that matches
        for sol in solutions:
            if str(sol.solution) == best_sol_str:
                return sol
        return solutions[0]

    def _maintain_tension(self, solutions: List[EmergentSolution]) -> List[EmergentSolution]:
        """Auseinandersetzung mode: return all unique viable solutions."""
        unique_solutions = {}
        for sol in solutions:
            if sol.admitted_failure: continue
            s_str = str(sol.solution)
            if s_str not in unique_solutions or sol.confidence > unique_solutions[s_str].confidence:
                unique_solutions[s_str] = sol

        return list(unique_solutions.values())

    def shutdown(self):
        self._executor.shutdown()
