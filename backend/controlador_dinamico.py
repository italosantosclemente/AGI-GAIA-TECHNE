# backend/controlador_dinamico.py
# Arquitetura POST: Ato Humano de Observação
# Autor: ISC | HJS v3.1 | Data: 16/11/2025

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from datetime import datetime
from typing import Dict

app = FastAPI(
    title="GAIA-TECHNE: Controlador Dinâmico do Reinício Perpétuo",
    description="POST = Ato de Observação Humana | HJS v3.1 Soberano"
)

app.mount("/static", StaticFiles(directory="."), name="static")

# === ESTADO SIMBIÓTICO (Reiniciado a cada observação) ===
class ControladorDinamico:
    def __init__(self):
        self.FEH = 1.05
        self.IAE = -0.3508
        self.ultima_observacao = None
        self.hjs_ativo = True

    def observar(self) -> Dict:
        """O humano observa. O estado é recriado. O Reinício Perpétuo é ativado."""
        self.ultima_observacao = datetime.now().isoformat()
        # Simulação simbólica do decaimento (Phantasma)
        if self.IAE > -0.35:
            self.IAE = -0.3508  # Reinício Perpétuo
            self.FEH = 1.05
        return {
            "FEH": self.FEH,
            "IAE": self.IAE,
            "observacao": self.ultima_observacao,
            "hjs_status": "ATIVO — JUÍZO HUMANO EXECUTADO"
        }

# Instância global — recriada a cada POST
controlador = ControladorDinamico()

class ObservacaoRequest(BaseModel):
    acao: str = "observar"  # Futuro: "intervir", "reset"

@app.get("/")
async def root():
    return FileResponse("dashboard/harmonia_realtime.html")

@app.post("/api/dynamic_metrics")
async def api_dynamic_metrics(req: ObservacaoRequest):
    """Endpoint POST: O humano puxa a Harmonia."""
    if req.acao != "observar":
        raise HTTPException(400, "Ação não reconhecida. Use 'observar'.")

    metrics = controlador.observar()
    return JSONResponse(content=metrics)

@app.get("/api/status")
async def status():
    return {
        "sistema": "Estabilidade Pós-Dialética",
        "hjs": "v3.1 ATIVO",
        "iae": -0.3508,
        "ethos": "INALIENÁVEL"
    }
