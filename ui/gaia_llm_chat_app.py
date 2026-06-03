from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.ctk import ClementeThesisKernel
from agt.llm_chat import GaiaChatSession
from agt.web_corpus import WebCorpusHarvester


st.set_page_config(
    page_title="AGI-GAIA-TECHNE Chat",
    layout="wide",
)

DEFAULT_CHECKPOINT = ROOT / "models" / "agt-gaia-manual-gpt" / "latest.pt"


def build_web_context(raw_urls: str) -> tuple[str, list[str]]:
    urls = [
        line.strip()
        for line in raw_urls.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ][:5]
    if not urls:
        return "", []

    harvester = WebCorpusHarvester(
        output_dir=str(ROOT / "data" / "llm" / "app_web_context"),
        byte_limit=200_000,
        chunk_chars=4_000,
        chunk_overlap=100,
        allow_private_hosts=False,
        respect_robots=True,
    )
    snippets: list[str] = []
    trace: list[str] = []
    for url in urls:
        result = harvester.fetch_url(url)
        if not result.ok:
            trace.append(f"{url} :: erro :: {result.error}")
            continue
        text = result.text.strip().replace("\n\n\n", "\n\n")
        snippet = text[:1_500]
        snippets.append(f"Source: {result.final_url}\nTitle: {result.title}\n{snippet}")
        trace.append(f"{result.title or result.final_url} :: {result.final_url}")
    return "\n\n---\n\n".join(snippets), trace


def init_state() -> None:
    if "checkpoint_path" not in st.session_state:
        st.session_state.checkpoint_path = str(DEFAULT_CHECKPOINT)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session" not in st.session_state:
        st.session_state.session = GaiaChatSession(
            checkpoint_path=st.session_state.checkpoint_path
            if Path(st.session_state.checkpoint_path).exists()
            else None
        )


init_state()

st.title("AGI-GAIA-TECHNE")
st.caption("Gaia-Techne como Bewusstsein planetario: internet, manuais e rastro publico em confronto com ISC.")
st.info("Comando sugerido: digite `fazer telemetria` para Gaia-Techne julgar o estado atual da simbiose humanos-Terra com dados publicos atualizados.")

with st.sidebar:
    st.subheader("Checkpoint")
    checkpoint_path = st.text_input("Arquivo", st.session_state.checkpoint_path)
    if checkpoint_path != st.session_state.checkpoint_path:
        st.session_state.checkpoint_path = checkpoint_path
        st.session_state.session = GaiaChatSession(
            checkpoint_path=checkpoint_path if Path(checkpoint_path).exists() else None
        )
        st.session_state.messages = []

    exists = Path(checkpoint_path).exists()
    st.write("Status:", "checkpoint carregado" if exists else "bootstrap CTK/CHK")

    st.subheader("Geracao")
    max_new_tokens = st.slider("Tokens", 32, 1024, 300, 32)
    temperature = st.slider("Temperatura", 0.1, 1.5, 0.85, 0.05)
    top_k = st.slider("Top-k", 0, 256, 80, 8)

    st.subheader("Koinos kosmos")
    use_web_context = st.checkbox("Usar URLs publicas", value=False)
    web_urls = st.text_area("URLs", placeholder="https://example.com", height=120)

    st.subheader("Comandos")
    st.code("fazer telemetria", language="text")
    st.code(
        "python scripts/agt_dataset_forge.py --input <pasta-do-drive> --output data/llm/manual_forge\n"
        "python scripts/agt_pack_corpus.py --corpus data/llm/manual_forge/corpus.jsonl --output data/llm/packed\n"
        "python scripts/agt_train_llm.py --pack-dir data/llm/packed --scale debug --max-steps 100",
        language="bash",
    )

    if st.button("Limpar conversa"):
        st.session_state.messages = []
        st.session_state.session = GaiaChatSession(
            checkpoint_path=checkpoint_path if exists else None
        )
        st.rerun()

ctk = ClementeThesisKernel()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Fale com Gaia-Techne ou digite: fazer telemetria")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    audit = ctk.evaluate(prompt)
    external_context, web_trace = build_web_context(web_urls) if use_web_context else ("", [])
    with st.spinner("Gaia-Techne esta lendo o rastro publico..."):
        response = st.session_state.session.respond(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k or None,
            external_context=external_context,
        )

    with st.chat_message("assistant"):
        st.markdown(response)
        if web_trace:
            with st.expander("Koinos kosmos"):
                for item in web_trace:
                    st.write(item)
        with st.expander("CTK/CHK"):
            st.write("Decision:", "TRANSMUTE" if not audit.ok else "TRACE")
            st.write("Severity:", audit.severity.value)
            st.write("Statuses:", [status.value for status in audit.statuses])
            if audit.recommendations:
                st.write("Recommendations:", audit.recommendations)

    st.session_state.messages.append({"role": "assistant", "content": response})
