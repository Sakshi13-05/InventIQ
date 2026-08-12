import streamlit as st
import json
from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load the "Brain"
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# UI Setup
st.set_page_config(page_title="InventIQ Dashboard", layout="wide")
st.title("🛡️ InventIQ: Global IP Navigator")
st.markdown("### *Concept-Driven Logic Mapping for the Modern Creator*")

# Sidebar for the "Vision"
st.sidebar.header("System Status")
st.sidebar.success("Global Registry: Active")
st.sidebar.info("Methodology: SIR Decomposition (Subject-Action-Boundary)")

# 1. User Input Section
st.subheader("Step 1: Describe your Invention DNA")
col1, col2, col3 = st.columns(3)
with col1:
    u_sub = st.text_input("What is it? (Subject)", placeholder="e.g. A sound-making gadget")
with col2:
    u_act = st.text_input("What does it do? (Action)", placeholder="e.g. Scares away pests")
with col3:
    u_bnd = st.text_input("Where is it used? (Boundary)", placeholder="e.g. On a farm")

# 2. The Logic Engine
if st.button("Analyze Global Conflict"):
    if not u_sub or not u_act:
        st.warning("Please fill in the core logic components.")
    else:
        with st.spinner("Extracting DNA and searching global registries..."):
            with open('registry.json', 'r') as f:
                registry = json.load(f)
            
            results = []
            for patent in registry:
                # Compare each DNA block separately to avoid being fooled by "word play"
                sub_sim = util.cos_sim(model.encode(u_sub), model.encode(patent['subject'])).item()
                act_sim = util.cos_sim(model.encode(u_act), model.encode(patent['action'])).item()
                bnd_sim = util.cos_sim(model.encode(u_bnd), model.encode(patent['boundary'])).item()
                
                # Weighted Score (Action is usually the most important in IP law)
                total_score = (sub_sim * 0.3) + (act_sim * 0.5) + (bnd_sim * 0.2)
                
                results.append({
                    "Patent ID": patent['id'],
                    "Title": patent['title'],
                    "Logic Overlap": total_score,
                    "Details": patent['text']
                })
            
            # Sort by highest overlap
            df = pd.DataFrame(results).sort_values(by="Logic Overlap", ascending=False)
            
            # 3. Visual Presentation
            st.subheader("Step 2: Conflict Heatmap")
            
            for index, row in df.iterrows():
                score_pct = int(row['Logic Overlap'] * 100)
                if score_pct > 70:
                    st.error(f"🚨 HIGH CONFLICT: {row['Patent ID']} ({score_pct}% Match)")
                    st.write(f"**Existing Invention:** {row['Title']}")
                    st.write(f"**Registry Text:** *{row['Details']}*")
                    st.progress(row['Logic Overlap'])
                elif score_pct > 40:
                    st.warning(f"⚠️ POTENTIAL OVERLAP: {row['Patent ID']} ({score_pct}% Match)")
                    st.progress(row['Logic Overlap'])
                else:
                    st.success(f"✅ LOW RISK: {row['Patent ID']} ({score_pct}% Match)")