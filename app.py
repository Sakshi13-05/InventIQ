import streamlit as st
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

from sir_extractor import extract_sir


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="InventIQ",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD CSS
# =========================================================

css_path = Path(__file__).parent / "styles.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(
    "<style>" + css + "</style>",
    unsafe_allow_html=True
)


# =========================================================
# MODEL
# =========================================================

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand-title">InventIQ</div>'
        '<div class="brand-subtitle">Global IP Navigator</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-line"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-label">SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status-box">'
        '<span class="status-dot"></span>'
        '<span>Global Registry: Active</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">METHODOLOGY</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="method-box">'
        '<div class="method-title">SIR Decomposition</div>'
        '<div class="method-text">Subject · Action · Boundary</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">ANALYSIS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-step">'
        '<span class="step-circle">1</span>'
        '<span>Describe Invention</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-step">'
        '<span class="step-circle">2</span>'
        '<span>Extract Invention DNA</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-step">'
        '<span class="step-circle">3</span>'
        '<span>Analyze Prior Art</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-bottom"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-note">'
        '<strong>Prototype</strong><br>'
        'Conceptual similarity only. '
        'Not a legal determination of patentability '
        'or infringement.'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-title">InventIQ</div>'
    '<div class="hero-subtitle">'
    'Concept-Driven Logic Mapping for the Modern Creator'
    '</div>'
    '<div class="hero-description">'
    'Identify conceptual overlap between your invention '
    'and existing prior-art concepts.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# STEP 1
# =========================================================

st.markdown(
    '<div class="section-title">'
    '<span class="step-tag">STEP 1</span>'
    'Describe Your Invention'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Describe your invention in your own words. '
    'No patent-specific language is required.'
    '</div>',
    unsafe_allow_html=True
)

u_claim = st.text_area(
    "Invention description",
    placeholder=(
        "Example: A device that uses high-frequency sound "
        "to keep insects away from stored grain."
    ),
    height=130,
    label_visibility="collapsed"
)

analyze = st.button(
    "Analyze Prior-Art Overlap",
    type="primary"
)


# =========================================================
# RUN ANALYSIS
# =========================================================

if analyze:

    if not u_claim.strip():

        st.warning("Please describe your invention first.")
        st.stop()


    # =====================================================
    # SIR EXTRACTION
    # =====================================================

    with st.spinner("Extracting invention DNA..."):

        try:
            sir = extract_sir(u_claim)

        except Exception as e:

            st.error(
                f"Failed to extract Invention DNA: {e}"
            )

            st.stop()


    # =====================================================
    # STEP 2
    # =====================================================

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        '<span class="step-tag">STEP 2</span>'
        'Extracted Invention DNA'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Your invention has been decomposed into three '
        'functional concepts.'
        '</div>',
        unsafe_allow_html=True
    )


    dna1, dna2, dna3 = st.columns(3, gap="medium")


    with dna1:

        st.markdown(
            '<div class="dna-card">'
            '<div class="dna-label">SUBJECT</div>'
            '<div class="dna-value">'
            + sir["subject"] +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with dna2:

        st.markdown(
            '<div class="dna-card">'
            '<div class="dna-label">ACTION</div>'
            '<div class="dna-value">'
            + sir["action"] +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with dna3:

        st.markdown(
            '<div class="dna-card">'
            '<div class="dna-label">BOUNDARY</div>'
            '<div class="dna-value">'
            + sir["boundary"] +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # LOAD REGISTRY
    # =====================================================

    with open(
        "registry.json",
        "r",
        encoding="utf-8"
    ) as f:

        registry = json.load(f)


    # =====================================================
    # STEP 3
    # =====================================================

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        '<span class="step-tag">STEP 3</span>'
        'Conceptual Prior-Art Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Semantic similarity is calculated across '
        'Subject, Action and Boundary.'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # CALCULATE RESULTS
    # =====================================================

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


        results.append(
            {
                "Patent ID": patent["id"],
                "Title": patent["title"],
                "Logic Overlap": total_score,
                "Subject Similarity": sub_sim,
                "Action Similarity": act_sim,
                "Boundary Similarity": bnd_sim,
                "Details": patent["text"]
            }
        )


    results.sort(
        key=lambda x: x["Logic Overlap"],
        reverse=True
    )


    # =====================================================
    # TOP RESULT
    # =====================================================

    if results:

        top = results[0]

        score_pct = int(
            max(0, min(top["Logic Overlap"], 1)) * 100
        )

        subject_pct = int(
            max(0, min(top["Subject Similarity"], 1)) * 100
        )

        action_pct = int(
            max(0, min(top["Action Similarity"], 1)) * 100
        )

        boundary_pct = int(
            max(0, min(top["Boundary Similarity"], 1)) * 100
        )


        matching_patent = next(
            (
                patent
                for patent in registry
                if patent["id"] == top["Patent ID"]
            ),
            None
        )


        # =================================================
        # TOP MATCH HEADER
        # =================================================

        st.markdown(
            '<div class="top-match-heading">'
            'Top Conceptual Match'
            '</div>',
            unsafe_allow_html=True
        )


        if score_pct > 70:

            status_class = "high"
            status_text = "HIGH CONCEPTUAL OVERLAP"

        elif score_pct > 40:

            status_class = "medium"
            status_text = "POTENTIAL CONCEPTUAL OVERLAP"

        else:

            status_class = "low"
            status_text = "LOW CONCEPTUAL OVERLAP"


        st.markdown(
            '<div class="match-card">'
            '<div class="match-status ' + status_class + '">'
            + status_text +
            '</div>'
            '<div class="match-content">'
            '<div>'
            '<div class="match-id">'
            + top["Patent ID"] +
            '</div>'
            '<div class="match-title">'
            + top["Title"] +
            '</div>'
            '</div>'
            '<div class="match-score">'
            + str(score_pct) +
            '% Match'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # RESULTS GRID
        # =================================================

        left_col, right_col = st.columns(
            [1.45, 1],
            gap="large"
        )


        # =================================================
        # LEFT
        # =================================================

        with left_col:

            st.markdown(
                '<div class="result-heading">'
                'Similarity Breakdown'
                '</div>',
                unsafe_allow_html=True
            )


            m1, m2, m3 = st.columns(3)


            with m1:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-label">SUBJECT</div>'
                    '<div class="metric-number">'
                    + str(subject_pct) +
                    '%</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


            with m2:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-label">ACTION</div>'
                    '<div class="metric-number">'
                    + str(action_pct) +
                    '%</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


            with m3:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-label">BOUNDARY</div>'
                    '<div class="metric-number">'
                    + str(boundary_pct) +
                    '%</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


            # ---------------------------------------------
            # COMPARISON
            # ---------------------------------------------

            st.markdown(
                '<div class="result-heading comparison-heading">'
                'Concept Comparison'
                '</div>',
                unsafe_allow_html=True
            )


            compare1, compare2 = st.columns(2)


            with compare1:

                st.markdown(
                    '<div class="comparison-card">'
                    '<div class="comparison-title">'
                    'Your Invention'
                    '</div>'
                    '<div class="comparison-label">Subject</div>'
                    '<div class="comparison-text">'
                    + sir["subject"] +
                    '</div>'
                    '<div class="comparison-label">Action</div>'
                    '<div class="comparison-text">'
                    + sir["action"] +
                    '</div>'
                    '<div class="comparison-label">Boundary</div>'
                    '<div class="comparison-text">'
                    + sir["boundary"] +
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


            with compare2:

                if matching_patent:

                    st.markdown(
                        '<div class="comparison-card existing-card">'
                        '<div class="comparison-title existing">'
                        'Existing Invention'
                        '</div>'
                        '<div class="comparison-label">Subject</div>'
                        '<div class="comparison-text">'
                        + matching_patent["subject"] +
                        '</div>'
                        '<div class="comparison-label">Action</div>'
                        '<div class="comparison-text">'
                        + matching_patent["action"] +
                        '</div>'
                        '<div class="comparison-label">Boundary</div>'
                        '<div class="comparison-text">'
                        + matching_patent["boundary"] +
                        '</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )


        # =================================================
        # RIGHT
        # =================================================

        with right_col:

            st.markdown(
                '<div class="result-heading">'
                'Why This Score?'
                '</div>',
                unsafe_allow_html=True
            )


            weighted_subject = (
                top["Subject Similarity"] * 0.30
            )

            weighted_action = (
                top["Action Similarity"] * 0.50
            )

            weighted_boundary = (
                top["Boundary Similarity"] * 0.20
            )


            contributions = {
                "Subject": weighted_subject,
                "Action": weighted_action,
                "Boundary": weighted_boundary
            }


            strongest = max(
                contributions,
                key=contributions.get
            )


            if strongest == "Action":

                explanation = (
                    f"Action similarity is {action_pct}%. "
                    "Because Action carries 50% of the "
                    "overall score, functional similarity "
                    "has the greatest influence."
                )

            elif strongest == "Subject":

                explanation = (
                    f"Subject similarity is {subject_pct}%. "
                    "Subject contributes 30% of the "
                    "overall score."
                )

            else:

                explanation = (
                    f"Boundary similarity is {boundary_pct}%. "
                    "Boundary contributes 20% of the "
                    "overall score."
                )


            st.markdown(
                '<div class="explanation-card">'
                '<div class="explanation-title">'
                'What is driving the match?'
                '</div>'
                '<div class="explanation-text">'
                + explanation +
                '</div>'
                '<div class="explanation-line"></div>'
                '<div class="overall-label">'
                'Overall Logic Overlap'
                '</div>'
                '<div class="overall-score">'
                + str(score_pct) +
                '%'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )


            st.progress(score_pct)


        # =================================================
        # DISCLAIMER
        # =================================================

        st.markdown(
            '<div class="disclaimer">'
            'Conceptual similarity within the prototype '
            'dataset. This is not a legal determination '
            'of patent infringement or patentability.'
            '</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # OTHER RESULTS
        # =================================================

        if len(results) > 1:

            st.markdown(
                '<div class="other-heading">'
                'Other Similar Results'
                '</div>',
                unsafe_allow_html=True
            )


            for index, result in enumerate(
                results[1:],
                start=2
            ):

                other_score = int(
                    max(
                        0,
                        min(
                            result["Logic Overlap"],
                            1
                        )
                    ) * 100
                )


                st.markdown(
                    '<div class="other-result">'
                    '<div>'
                    '<span class="other-rank">'
                    '#' + str(index) +
                    '</span>'
                    '<span class="other-id">'
                    + result["Patent ID"] +
                    '</span>'
                    '<span class="other-title">'
                    + result["Title"] +
                    '</span>'
                    '</div>'
                    '<div class="other-score">'
                    + str(other_score) +
                    '%'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


    else:

        st.info(
            "No matching inventions were found."
        )