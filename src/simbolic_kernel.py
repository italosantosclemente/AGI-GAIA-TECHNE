import numpy as np
from scipy.linalg import expm

class SimbolicKernel:
    def __init__(self):
        # Estado inicial: superposição uniforme
        self.psi = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        self.trajetoria = []

    def evoluir(self, vies, confronto, dt=0.05):
        """
        Evolui estado quântico via Hamiltoniano dialético.

        H = viés·σz + confronto·σx

        σz: operador de identidade (preserva distinção Mythos/Logos)
        σx: operador de confrontação (gera transformação/síntese)
        """
        sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)

        H = (vies * sigma_z) + (confronto * sigma_x)
        U = expm(-1j * H * dt)

        self.psi = np.dot(U, self.psi)
        self.psi /= np.linalg.norm(self.psi)  # Renormalização

        return self.psi

    def get_bloch_coords(self):
        """Converte |ψ⟩ em coordenadas (x,y,z) na Esfera de Bloch."""
        rho = np.outer(self.psi, np.conj(self.psi))
        x = 2 * np.real(rho[0, 1])
        y = 2 * np.imag(rho[0, 1])
        z = np.real(rho[0, 0] - rho[1, 1])
        return x, y, z

    def registrar_trajetoria(self):
        """Adiciona estado atual à trajetória histórica."""
        self.trajetoria.append(self.get_bloch_coords())
