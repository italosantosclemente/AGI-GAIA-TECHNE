module PythonBridge

using PythonCall

export run_firewall_review, run_symbolic_verification

# We assume v7.0/python/src is in the PYTHONPATH or we use the relative path
# For the orchestrator, we might need to add the path to sys.path

function __init__()
    # Add project root to python path to find our modules
    pyimport("sys").path.append(pwd())
end

function run_firewall_review(maxim_str, context_dict, graph_ptr)
    pyimport("sys").path.append(joinpath(pwd(), "v7.0/python"))
    fw = pyimport("v7_core.firewall_agi.firewall_agi")
    firewall = fw.KantianFirewall()
    sp = pyimport("sympy")
    maxim = sp.sympify(maxim_str)

    # Verdict is a FirewallVerdict dataclass instance
    verdict = firewall.full_review(maxim, context_dict, graph_ptr)
    return verdict
end

function run_symbolic_verification(claim_str, property_str, constraints_dict)
    pyimport("sys").path.append(joinpath(pwd(), "v7.0/python"))
    dtv = pyimport("v7_core.deep_think_verifier.deep_think_verifier")
    verifier = dtv.DeepThinkVerifier()
    task = dtv.VerificationTask(
        task_id = "julia_task_$(rand(1000:9999))",
        claim = claim_str,
        property_to_verify = property_str,
        domain_constraints = constraints_dict
    )

    results = verifier.verify_parallel([task])
    return results[task.task_id]
end

end # module
