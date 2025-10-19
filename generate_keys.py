# generate_keys.py: Geração Segura de Chaves SOBERANO (Dilithium)
import os
from dilithium import Dilithium

if __name__ == "__main__":
    if not os.path.exists("keys"):
        os.makedirs("keys")

    # Gera um novo par de chaves Dilithium
    public_key, private_key = Dilithium.generate_keys()

    # Salva as chaves (CUIDADO com o armazenamento em produção!)
    with open("keys/soberano_public.key", "wb") as f:
        f.write(public_key)
    with open("keys/soberano_private.key", "wb") as f:
        f.write(private_key)

    print("Novo par de chaves SOBERANO (Dilithium) gerado em 'keys/'.")
