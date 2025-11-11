import streamlit as st
from pathlib import Path
from typing import Dict, Any, List

# =============================
# App Configuration & Styling
# =============================
st.set_page_config(
    page_title="AI4Sight Podcast Hub",
    page_icon="🎧",
    layout="wide",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.ep-card {
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 14px;
  padding: 1rem 1.2rem;
  background: var(--background-color);
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

hr.soft { border: none; border-top: 1px solid rgba(0,0,0,0.08); margin: 1rem 0; }

.badge {
  display: inline-block;
  padding: 0.15rem .5rem;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.1);
  font-size: 0.8rem;
  margin-right: .35rem;
}

.link-ref {
  font-size: 0.9rem;
  color: #0066cc;
  text-decoration: none;
}
.link-ref:hover {
  text-decoration: underline;
}
.streamlit-expanderHeader { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# =============================
# Data Model
# =============================
Podcasts: Dict[str, Dict[str, Any]] = {
    "Rhapsido® Approval Update": {
        "file": "audio/remi.wav",
        "summary_file": "summary/remi.md",
        "synopsis": (
            "Rhapsido® (Remibrutinib) has received FDA approval for treating chronic spontaneous urticaria (CSU). "
            "It offers a novel, oral BTK inhibitor approach, providing rapid and sustained control without lab monitoring."
        ),
        "tags": ["CSU", "Immunology", "Launch"],
        "source_link": "https://www.novartis.com/news/media-releases/novartis-receives-fda-approval-rhapsido-remibrutinib-only-oral-targeted-btki-treatment-chronic-spontaneous-urticaria-csu",
        "talking_points": [
            "Targets BTK to prevent histamine release – a unique oral therapy for CSU.",
            "Demonstrated well-controlled disease in as fast as 2 weeks.",
            "Strong safety profile and no lab monitoring required.",
        ],
        "hcp_hooks": [
            "Doctor, have you explored how BTK inhibition could redefine CSU management?",
            "Would your patients benefit from an oral, lab-free CSU therapy with rapid control?",
        ],
    },
    "Remibrutinib Summary": {
        "file": "audio/remi_short.wav",
        "summary_file": "summary/remi_short.md",
        "synopsis": "A concise recap of Remibrutinib’s mechanism, efficacy timeline, and safety highlights in CSU.",
        "tags": ["CSU", "Mechanism", "Oral BTKi"],
        "source_link": "https://www.novartis.com/news/media-releases/novartis-receives-fda-approval-rhapsido-remibrutinib-only-oral-targeted-btki-treatment-chronic-spontaneous-urticaria-csu",
        "talking_points": [
            "Fast onset of symptom relief with oral dosing.",
            "Improved patient convenience with simplified monitoring.",
        ],
        "hcp_hooks": [
            "What’s your view on patient adherence when switching to oral CSU therapies?",
        ],
    },
    "Scembix": {
        "file": "audio/scemblix.wav",
        "summary_file": "summary/scemblix.md",
        "synopsis": (
            "Scemblix introduces next-generation precision for chronic myeloid leukemia (CML) "
            "with improved tolerability and targeted action."
        ),
        "tags": ["CML", "Oncology", "Next-Gen"],
        "source_link": "https://us.scemblix.com/",
        "talking_points": [
            "Designed to overcome resistance seen in earlier CML therapies.",
            "Enhanced safety profile enabling broader patient suitability.",
        ],
        "hcp_hooks": [
            "Doctor, how do you decide when to move beyond first-line CML therapy?",
        ],
    },
    "Coartem": {
        "file": "audio/coartem.wav",
        "summary_file": "summary/coartem.md",
        "synopsis": (
            "A reflection on Coartem’s legacy in global malaria control and Novartis’s ongoing commitment "
            "to access and innovation in infectious disease management."
        ),
        "tags": ["Malaria", "Access", "Public Health"],
        "source_link": "https://www.novartis.com/news/media-releases/novartis-receives-approval-first-malaria-medicine-newborn-babies-and-young-infants",
        "talking_points": [
            "Decades-long impact on malaria mortality reduction.",
            "Key role in public health partnerships across Africa and Asia.",
        ],
        "hcp_hooks": [
            "How can public-private collaboration sustain malaria-free progress?",
        ],
    },
    "Novartis Q3'25 Financial updates": {
        "file": "audio/Quaterly_Report.wav",
        "summary_file": "summary/quarterly_report.md",
        "synopsis": (
            "Overview of Novartis’ third-quarter 2025 financial performance — revenue growth, pipeline acceleration, "
            "and innovation momentum across Immunology and Oncology portfolios."
        ),
        "tags": ["Financials", "Q3 2025", "Corporate"],
        "source_link": "https://www.novartis.com/news",
        "talking_points": [
            "Robust pipeline momentum in Immunology and Oncology.",
            "Strong adoption trends across Leqvio® and Kisqali® markets.",
        ],
        "hcp_hooks": [
            "What therapeutic areas excite you the most in Novartis’s innovation roadmap?",
        ],
    },
}

# =============================
# Utilities
# =============================
cache_decorator = st.cache_data if hasattr(st, "cache_data") else st.cache

@cache_decorator(show_spinner=False)
def read_markdown(md_path: Path) -> str:
    try:
        return md_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"⚠️ Error reading file: {e}"

def file_exists(path_str: str) -> bool:
    return Path(path_str).expanduser().resolve().exists()

def render_badges(tags: List[str]):
    if tags:
        st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in tags]), unsafe_allow_html=True)

def render_source_link(url: str, label: str = "🌐 View Source"):
    """Properly styled clickable link that opens in new tab."""
    if url:
        st.markdown(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="link-ref">{label}</a>',
            unsafe_allow_html=True,
        )

# =============================
# Header
# =============================
st.title("🎙️ AI4Sight – Novartis Internal Podcast Hub")
st.markdown(
    "Welcome to the **AI4Sight Podcast Hub** — your go-to space to stay informed, inspired, and conversation-ready. "
    "Listen to concise updates on new molecules, launches, field success stories, and quarterly highlights."
)
st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# =============================
# Sidebar
# =============================
with st.sidebar:
    st.header("Library Filters")
    search = st.text_input("Search episodes", placeholder="e.g., CSU, Oncology, Q3")
    tags = sorted({t for v in Podcasts.values() for t in v.get("tags", [])})
    selected_tags = st.multiselect("Filter by tags", options=tags, default=[])
    rep_mode = st.checkbox("Enable Rep Mode (HCP Hooks & Talking Points)", value=False)
    st.markdown("<hr class='soft'/>", unsafe_allow_html=True)
    st.caption("© 2025 Novartis | Internal Use Only | Powered by AI4Sight")

# =============================
# Filter Episodes
# =============================
def passes_filters(name: str, meta: Dict[str, Any]) -> bool:
    text = (name + " " + meta.get("synopsis", "")).lower()
    if search and search.lower() not in text:
        return False
    if selected_tags:
        tags = set(meta.get("tags", []))
        if not tags.intersection(set(selected_tags)):
            return False
    return True

episodes = [k for k, v in Podcasts.items() if passes_filters(k, v)]
if not episodes:
    st.info("No episodes match your filters. Try clearing filters.")
    st.stop()

# =============================
# Episode Selector
# =============================
selected = st.selectbox("🎧 Choose an episode:", episodes)
episode = Podcasts[selected]
st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# =============================
# Episode Player + Details
# =============================
st.markdown(f"### ▶️ Now Playing: *{selected}*")
st.markdown("<div class='ep-card'>", unsafe_allow_html=True)

# Audio Player
if file_exists(episode["file"]):
    st.audio(episode["file"])
else:
    st.error("Audio file not found.")

# Synopsis + Source
st.markdown("#### 🧾 Synopsis")
st.caption(episode["synopsis"])
render_badges(episode.get("tags", []))
render_source_link(episode.get("source_link"))

# Summary Section
summary_path = Path(episode["summary_file"])
st.markdown("#### 📜 Detailed Summary")
if summary_path.exists():
    with st.expander("Read Full Summary"):
        st.markdown(read_markdown(summary_path), unsafe_allow_html=True)
else:
    st.warning("No summary file found for this episode.")

# Rep Mode
if rep_mode:
    st.markdown("<hr class='soft'/>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**💬 Key Talking Points**")
        for t in episode.get("talking_points", []):
            st.markdown(f"- {t}")
    with c2:
        st.markdown("**🎯 HCP Hook Ideas**")
        for h in episode.get("hcp_hooks", []):
            st.markdown(f"- {h}")

st.markdown("</div>", unsafe_allow_html=True)

