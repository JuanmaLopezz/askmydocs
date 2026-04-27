import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AskMyDocs", page_icon="📄", layout="wide")
st.title("📄 AskMyDocs")
st.caption("Sube documentos y hazles preguntas en lenguaje natural")

col_left, col_right = st.columns([1, 2])

# ── LEFT: upload + document list ──────────────────────────────────────────────
with col_left:
    st.subheader("Documentos")

    uploaded = st.file_uploader(
        "Subir documento",
        type=["pdf", "docx", "xlsx", "txt"],
        help="Máx 50 MB. Formatos: PDF, Word, Excel, TXT",
    )
    if uploaded and st.button("Indexar", type="primary"):
        with st.spinner("Indexando..."):
            try:
                resp = requests.post(
                    f"{API_URL}/documents/upload",
                    files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                    timeout=120,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(f"✅ {data['filename']} — {data['chunks']} chunks")
                    st.rerun()
                else:
                    st.error(f"Error {resp.status_code}: {resp.json().get('detail', resp.text)}")
            except Exception as e:
                st.error(f"Error conectando con la API: {e}")

    st.divider()
    st.markdown("**Indexados**")

    try:
        docs_resp = requests.get(f"{API_URL}/documents/", timeout=10)
        docs = docs_resp.json() if docs_resp.status_code == 200 else []
    except Exception:
        docs = []
        st.warning("API no disponible")

    if not docs:
        st.info("Sin documentos indexados")
    else:
        for doc in docs:
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{doc['filename']}**  \n`{doc['chunks']} chunks`")
            if c2.button("🗑", key=f"del_{doc['id']}", help="Eliminar"):
                try:
                    r = requests.delete(f"{API_URL}/documents/{doc['id']}", timeout=10)
                    if r.status_code == 200:
                        st.success("Eliminado")
                        st.rerun()
                    else:
                        st.error(r.json().get("detail", "Error"))
                except Exception as e:
                    st.error(str(e))

# ── RIGHT: query ──────────────────────────────────────────────────────────────
with col_right:
    st.subheader("Consulta")

    question = st.text_area(
        "Pregunta",
        placeholder="¿Cuál es el importe total de la factura del mes de marzo?",
        height=100,
    )
    top_k = st.slider("Fuentes a consultar", 2, 10, 4, help="Cuántos fragmentos de los documentos se analizan para generar la respuesta. Más fuentes = respuesta más completa pero más lenta.")

    if st.button("Preguntar", type="primary", disabled=not question.strip()):
        if not docs:
            st.warning("Sube al menos un documento antes de preguntar.")
        else:
            with st.spinner("Consultando..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/query/",
                        json={"question": question, "top_k": top_k},
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        result = resp.json()
                        st.markdown("### Respuesta")
                        st.markdown(result["answer"])

                        if result.get("sources"):
                            st.markdown("### Fuentes")
                            for src in result["sources"]:
                                page_info = f" — p.{src['page']}" if src.get("page") else ""
                                with st.expander(f"📎 {src['document']}{page_info}"):
                                    st.markdown(f"> {src['chunk']}")
                    else:
                        st.error(f"Error {resp.status_code}: {resp.json().get('detail', resp.text)}")
                except Exception as e:
                    st.error(f"Error conectando con la API: {e}")
