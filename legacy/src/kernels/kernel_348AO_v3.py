import torch
import torch.nn as nn
from torch.optim import Adam

# Configuração de semente para reprodutibilidade ontológica
torch.manual_seed(42)

def eml_operator(x, y):
    """
    Operador EML (exp(x) - log(y)) com proteção contra singularidades (Mythos).
    """
    eps = torch.complex(torch.tensor(1e-10), torch.tensor(0.0))
    y_safe = torch.where(torch.abs(y) < 1e-10, y + eps, y)
    return torch.exp(x) - torch.log(y_safe)

class ComplexLayerNorm(nn.Module):
    """
    Normalização no plano complexo para estabilização do Logos.
    """
    def __init__(self, eps=1e-5):
        super().__init__()
        self.eps = eps
    def forward(self, x):
        if not torch.is_complex(x):
            x = x.to(torch.complex64)
        mean = torch.mean(x)
        var = torch.mean(torch.abs(x - mean)**2)
        std = torch.sqrt(var + self.eps)
        return (x - mean) / std

class ResEMLLayer(nn.Module):
    """
    Camada Residual EML (ResEML).
    A conexão residual alpha * h garante a preservação do Ausdruck (intuição original).
    """
    def __init__(self, alpha=0.2):
        super().__init__()
        # Inicialização ontológica ancorada na vizinhança da Darstellung (1.0 + 0j)
        self.w_x = nn.Parameter(torch.complex(torch.randn(1)*0.3, torch.randn(1)*0.3))
        self.w_y = nn.Parameter(torch.complex(torch.tensor(1.0), torch.randn(1)*0.1))
        self.alpha = alpha
        self.ln = ComplexLayerNorm()

    def forward(self, h):
        left = self.w_x * self.ln(h)
        right = self.w_y * torch.complex(torch.tensor(1.0), torch.tensor(0.0))
        out = eml_operator(left, right)
        return out + self.alpha * h

class ResEMLTree(nn.Module):
    """
    Árvore de regressão simbólica profunda composta por camadas ResEML.
    """
    def __init__(self, depth=4):
        super().__init__()
        self.layers = nn.ModuleList([ResEMLLayer() for _ in range(depth)])

    def forward(self, z):
        h = z.to(torch.complex64)
        for layer in self.layers:
            h = layer(h)
        return h

def gewissen_loss(pred, target, model, lambda_t=0.05, mu=0.01):
    """
    Gewissen Loss (v3): Equilíbrio entre erro fenomenal, tensão transcendental e entropia.
    """
    mse = torch.mean(torch.abs(pred - target)**2)

    # Tensão Transcendental: penaliza o colapso y -> 1
    tension = 0.0
    for layer in model.layers:
        wy = layer.w_y
        tension += torch.abs(wy - 1.0)**2
    tension = lambda_t * tension

    # Entropia da Significância: garante a riqueza da mediação
    entropy = 0.0
    for layer in model.layers:
        wy = layer.w_y
        mod2 = torch.abs(wy)**2 + 1e-8
        entropy += mod2 * torch.log(mod2)
    entropy = -mu * entropy

    return mse + tension + entropy

if __name__ == "__main__":
    # Dados: intuição quântica bruta (x, t) → Ψ(x,t) = exp(i(kx − ωt))
    num_samples = 200
    k, omega = 1.0, 0.5
    x_vals = torch.rand(num_samples) * 20 - 10
    t_vals = torch.rand(num_samples) * 20
    input_z = torch.complex(x_vals, t_vals)                    # z = x + i t
    target = torch.exp(1j * (k * x_vals - omega * t_vals)).to(torch.complex64)

    # Modelo
    model = ResEMLTree(depth=4)
    optimizer = Adam(model.parameters(), lr=0.01)

    print("--- Iniciando a Forja do Kernel 348AO-v3 (PyTorch) ---")
    epochs = 300
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        pred = model(input_z)
        loss = gewissen_loss(pred, target, model)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # Proteção ontológica
        optimizer.step()
        if epoch % 50 == 0 or epoch == 1:
            current_loss = loss.item()
            print(f"Época {epoch} | Loss: {current_loss:.6f}")
            print(f"  w_y[0]: {model.layers[0].w_y.item():.4f} | w_y[-1]: {model.layers[-1].w_y.item():.4f}")

    print("--- Forja Concluída ---")

    # Teste de síntese
    test_x, test_t = torch.tensor(2.0), torch.tensor(5.0)
    test_z = torch.complex(test_x, test_t)
    pred_test = model(test_z)
    true_test = torch.exp(1j * (k * test_x - omega * test_t))
    print(f"Predição teste (x=2, t=5): {pred_test.item()}")
    print(f"Valor real: {true_test.item()}")
    print(f"Erro absoluto: {torch.abs(pred_test - true_test).item():.6f}")
