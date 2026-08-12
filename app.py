import streamlit as st
import json
from sentence_transformers import SentenceTransformer, util

from sir_extractor import extract_sir


st.set_page_config(
    page_title="InventIQ Dashboard",
    layout="wide"
)

st.title("🛡️ InventIQ: Global IP Navigator")
st.markdown("### *Concept-Driven Logic Mapping for the Modern Creator*")


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


st.sidebar.header("System Status")
st.sidebar.success("Global Registry: Active")
st.sidebar.info(
    "Methodology: SIR Decomposition (Subject-Action-Boundary)"
)


st.subheader("Step 1: Describe Your Invention")

u_claim = st.text_area(
    "Describe your invention in your own words",
    placeholder=(
        "Example: A device that uses high-frequency "
        "sound to keep insects away from stored grain."
    ),
    height=150
)


if st.button("🔍 Analyze Global Conflict"):

    if not u_claim.strip():
        st.warning("Please describe your invention first.")
        st.stop()

    with st.spinner("🧠 Extracting your Invention DNA..."):
        try:
            sir = extract_sir(u_claim)
        except Exception as e:
            st.error(f"Failed to extract Invention DNA: {e}")
            st.stop()

    st.subheader("🧬 Step 2: Extracted Invention DNA")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### SUBJECT")
        st.info(sir["subject"])

    with col2:
        st.markdown("### ACTION")
        st.info(sir["action"])

    with col3:
        st.markdown("### BOUNDARY")
        st.info(sir["boundary"])

    with open("registry.json", "r", encoding="utf-8") as f:
        registry = json.load(f)

    st.subheader("🔎 Step 3: Conceptual Conflict Analysis")

    results = []

    for patent in registry:

        sub_sim = util.cos_sim(
            model.encode(sir["subject"]),
            model.encode(patent["subject"])
        ).item()

        act_sim = util.cos_sim(
            model.encode(sir["action"]),
            model.encode(patent["action"])
        ).item()

        bnd_sim = util.cos_sim(
            model.encode(sir["boundary"]),
            model.encode(patent["boundary"])
        ).item()

        total_score = (
            sub_sim * 0.30
            + act_sim * 0.50
            + bnd_sim * 0.20
        )

        results.append({
            "Patent ID": patent["id"],
            "Title": patent["title"],
            "Logic Overlap": total_score,
            "Subject Similarity": sub_sim,
            "Action Similarity": act_sim,
            "Boundary Similarity": bnd_sim,
            "Details": patent["text"]
        })

    results.sort(
        key=lambda x: x["Logic Overlap"],
        reverse=True
    )

    for result in results:

        score = result["Logic Overlap"]
        score_pct = int(max(0, min(score, 1)) * 100)

        if score_pct > 70:

            st.error(
                f"🚨 HIGH CONFLICT: "
                f"{result['Patent ID']} ({score_pct}% Match)"
            )

            st.write(
                f"**Existing Invention:** {result['Title']}"
            )

            st.write(
                f"**Registry Text:** *{result['Details']}*"
            )

            st.write(
                f"**Subject Match:** "
                f"{int(max(0, result['Subject Similarity']) * 100)}%"
            )

            st.write(
                f"**Action Match:** "
                f"{int(max(0, result['Action Similarity']) * 100)}%"
            )

            st.write(
                f"**Boundary Match:** "
                f"{int(max(0, result['Boundary Similarity']) * 100)}%"
            )

            st.progress(score_pct)

        elif score_pct > 40:

            st.warning(
                f"⚠️ POTENTIAL OVERLAP: "
                f"{result['Patent ID']} ({score_pct}% Match)"
            )

            st.write(
                f"**Existing Invention:** {result['Title']}"
            )

            st.write(
                f"**Subject Match:** "
                f"{int(max(0, result['Subject Similarity']) * 100)}%"
            )

            st.write(
                f"**Action Match:** "
                f"{int(max(0, result['Action Similarity']) * 100)}%"
            )

            st.write(
                f"**Boundary Match:** "
                f"{int(max(0, result['Boundary Similarity']) * 100)}%"
            )

            st.progress(score_pct)

        else:

            st.success(
                f"✅ LOW RISK: "
                f"{result['Patent ID']} ({score_pct}% Match)"
            )

            st.write(
                f"**Existing Invention:** {result['Title']}"
            )