include(joinpath(@__DIR__, "..", "src", "core", "eml_kernel_v4_complete.jl"))
using .EMLKernelV4Complete

if !isdefined(EMLKernelV4Complete, :executar_verificacao_completa_v4)
    error("executar_verificacao_completa_v4() not found in EMLKernelV4Complete")
end

EMLKernelV4Complete.executar_verificacao_completa_v4()
