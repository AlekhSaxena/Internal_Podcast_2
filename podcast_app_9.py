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
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "AI4Sight – Novartis Internal Podcast Hub"
    }
)

# Subtle CSS polish for cards, dividers, and small details
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

.muted { color: rgba(0,0,0,0.55); font-size: 0.92rem; }

.badge {
  display: inline-block;
  padding: 0.15rem .5rem;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.1);
  font-size: 0.8rem;
  margin-right: .35rem;
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
# Utilities (with compatibility)
# =============================
# Cache decorator fallback for older Streamlit
cache_decorator = st.cache_data if hasattr(st, "cache_data") else st.cache

@cache_decorator(show_spinner=False)
def read_markdown(md_path: Path) -> str:
    try:
        return md_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"⚠️ Error reading file: {e}"

def file_exists(path_str: str) -> bool:
    return Path(path_str).expanduser().resolve().exists()

def audio_format_from_suffix(path_str: str) -> str:
    suf = Path(path_str).suffix.lower()
    if suf == ".wav":
        return "audio/wav"
    if suf == ".mp3":
        return "audio/mp3"
    if suf == ".m4a":
        return "audio/mp4"
    return "audio/wav"

def render_badges(tags: List[str]):
    if not tags:
        return
    st.markdown(" ".join([f"<span class='badge'>{t}</span>" for t in tags]), unsafe_allow_html=True)

# Rerun helper for old/new Streamlit
def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# =============================
# Header
# =============================
left, right = st.columns([0.7, 0.3])
with left:
    st.title("🎙️ AI4Sight – Novartis Internal Podcast Hub")
    st.markdown(
        "Welcome to the **AI4Sight Podcast Hub** — your go-to space to stay informed, inspired, and conversation-ready. "
        "Listen to concise updates on new molecules, launches, field success stories, and quarterly highlights."
    )
with right:
    st.metric("Active Episodes", len(Podcasts))
st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# =============================
# Sidebar Controls
# =============================
with st.sidebar:
    st.header("Library Filters")
    search = st.text_input("Search title or synopsis", placeholder="e.g., CSU, Oncology, Q3")
    all_tags = sorted({t for v in Podcasts.values() for t in v.get("tags", [])})
    selected_tags = st.multiselect("Filter by tags", options=all_tags, default=[])

    st.markdown("### Rep Tools")
    rep_mode = st.checkbox("Enable Rep Mode (HCP Hooks & Talking Points)", value=False)

    st.markdown("<hr class='soft'/>", unsafe_allow_html=True)
    st.caption("© 2025 Novartis | Internal Use Only | Powered by AI4Sight")

# =============================
# Filter Logic
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

episode_names = [k for k, v in Podcasts.items() if passes_filters(k, v)]
if not episode_names:
    st.info("No episodes match your filters. Try clearing the search or tag selection.")
    st.stop()

# =============================
# Episode Picker (with session state)
# =============================
SELECT_KEY = "ai4s_selected_episode"
default_idx = 0
if SELECT_KEY not in st.session_state:
    st.session_state[SELECT_KEY] = episode_names[default_idx]

c1, c2 = st.columns([0.6, 0.4])
with c1:
    selected_episode = st.selectbox(
        "🎧 Choose an episode",
        episode_names,
        index=episode_names.index(st.session_state[SELECT_KEY]) if st.session_state[SELECT_KEY] in episode_names else 0,
        key=SELECT_KEY
    )
with c2:
    st.caption("Tip: Use the filters in the sidebar to narrow down episodes by tags or keywords.")

st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# =============================
# Episode Detail Card
# =============================
episode = Podcasts[st.session_state[SELECT_KEY]]

st.markdown(f"#### ▶️ Now Playing: *{st.session_state[SELECT_KEY]}*")
st.markdown("<div class='ep-card'>", unsafe_allow_html=True)

# top row: audio + metadata
ac, bc = st.columns([0.55, 0.45])
with ac:
    audio_path = episode["file"]
    if file_exists(audio_path):
        st.audio(audio_path, format=audio_format_from_suffix(audio_path))
        dl_col1, dl_col2, _ = st.columns([0.25, 0.25, 0.5])
        with dl_col1:
            st.download_button("⬇️ Download Audio",
                               data=Path(audio_path).read_bytes(),
                               file_name=Path(audio_path).name,
                               mime=audio_format_from_suffix(audio_path))
        with dl_col2:
            st.success("Ready to play")
    else:
        st.error("Audio file not found. Please verify the path.")
        st.caption(f"Expected at: `{audio_path}`")

with bc:
    st.markdown("**Synopsis**")
    st.caption(episode["synopsis"])
    render_badges(episode.get("tags", []))

st.markdown("<hr class='soft'/>", unsafe_allow_html=True)

# Summary Section
st.markdown("##### 📜 Detailed Summary")
summary_path = Path(episode["summary_file"]).expanduser().resolve()
if summary_path.exists():
    with st.expander("Read full summary (markdown)", expanded=False):
        md_content = read_markdown(summary_path)
        st.markdown(md_content, unsafe_allow_html=True)
else:
    st.warning("No detailed summary file found for this episode.")

# Rep Mode
if rep_mode:
    st.markdown("<hr class='soft'/>", unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    with tc1:
        st.markdown("**💬 Key Talking Points**")
        for tp in episode.get("talking_points", []):
            st.markdown(f"- {tp}")
    with tc2:
        st.markdown("**🎯 HCP Hook Ideas**")
        hooks = episode.get("hcp_hooks", [])
        for hk in hooks:
            st.markdown(f"- {hk}")
    if hooks := episode.get("hcp_hooks", []):
        st.download_button(
            "Copy HCP Hooks (txt)",
            data=("\n".join(hooks)).encode("utf-8"),
            file_name=f"{st.session_state[SELECT_KEY].replace(' ','_')}_hcp_hooks.txt",
            mime="text/plain"
        )

st.markdown("</div>", unsafe_allow_html=True)

# =============================
# Library Grid (Other Episodes)
# =============================
st.markdown("### 📚 More from the Library")
grid = [e for e in episode_names if e != st.session_state[SELECT_KEY]]
if grid:
    cols = st.columns(3)
    for i, name in enumerate(grid):
        meta = Podcasts[name]
        with cols[i % 3]:
            # simple bordered box via CSS class emulation
            st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
            st.markdown(f"**{name}**")
            render_badges(meta.get("tags", []))
            syn = meta.get("synopsis", "")
            st.caption(syn[:140] + ("…" if len(syn) > 140 else ""))
            if st.button(f"Open ▶️", key=f"open_{i}", use_container_width=True):
                st.session_state[SELECT_KEY] = name
                do_rerun()
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.caption("You’ve reached the end of the library.")

