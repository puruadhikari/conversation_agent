import streamlit as st
import json

# --- SET PAGE CONFIG FIRST! ---
st.set_page_config(page_title="AI Article Refiner", layout="wide")

# --- Modern Professional CSS Styling ---
st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp h1, .stApp .stTitle { color: #1a237e; letter-spacing: 1px; }
    h2, .stApp .stHeader { color: #283593; margin-bottom: 0.5rem; }
    .stApp .stCaption { color: #607d8b; }
    .stApp .stMarkdown p { color: #333; font-size: 1.07rem;}
    .stApp .stTextArea textarea { border-radius: 0.6rem; border: 1.2px solid #bdbdbd; background: #fafbfc; }
    .stApp .stTabs [data-baseweb="tab"] { background: #f5f7fa; border-radius: 0.4rem 0.4rem 0 0; margin-right: 0.2rem; font-weight: 600;}
    .stApp .stTabs [aria-selected="true"] { background: #1976d2 !important; color: #fff !important; }
    .stApp .stExpander { border-radius: 1rem !important; background: #f5f7fa !important; box-shadow: 0 1px 8px rgba(30,64,175,0.04); }
    .stApp .stButton > button { border-radius: 0.5rem; font-weight: 600; padding: 0.5rem 1.5rem;}
    .stApp .stDivider { margin: 2rem 0 1rem 0; }
    .final-article-box { border: 1px solid #81c784; background: #f1f8e9; border-radius: 1rem; padding: 2rem 2rem 1rem 2rem; margin-top: 1.5rem; box-shadow: 0 2px 8px #dcedc8; }
    .final-article-box h3 { color: #388e3c; margin-top: 1.5em; margin-bottom: 0.3em; }
    .final-article-box p { margin-bottom: 0.7em; }
    .stApp { background: linear-gradient(150deg,#e3ecff 0%, #f9f9fb 100%); }
    p[style*="text-align: center"] { font-size: 1.08rem; color: #8692a6 !important; }
</style>
""", unsafe_allow_html=True)

# --- Configuration & Constants ---
APP_TITLE = "AI Article Refiner"
FOOTER_TEXT = "Powered by Streamlit & AI"
SAMPLE_JSON_OUTPUT = {
  "article_data": [
    {
      "section_id": "sec_intro_01",
      "section_name": "Introduction: The Challenge of Climate Change",
      "section_content_variation_1": "Global climate change presents an unparalleled challenge to modern society, demanding immediate and comprehensive solutions. This paper explores...",
      "section_content_variation_2": "The escalating crisis of climate change requires urgent attention. In this document, we will examine the primary drivers and potential mitigations...",
      "section_content_variation_3": "Understanding the multifaceted nature of climate change is crucial. This article delves into its ecological, economic, and social impacts, proposing a framework for..."
    },
    {
      "section_id": "sec_method_02",
      "section_name": "Methodology: Data Collection and Analysis",
      "section_content_variation_1": "Our research methodology involved collecting data from peer-reviewed journals published between 2018 and 2023. Statistical analysis was performed using SPSS.",
      "section_content_variation_2": "To investigate this phenomenon, we adopted a mixed-methods approach, combining quantitative survey data with qualitative interviews. Data was sourced from...",
      "section_content_variation_3": "The study's methodological framework is grounded in empirical data acquisition from diverse sources. We employed advanced analytical techniques to ensure robustness of findings."
    },
    {
      "section_id": "sec_analysis_03",
      "section_name": "Analysis: Key Findings",
      "section_content_variation_1": "The primary finding of this study is a significant correlation between variable X and outcome Y. This suggests that interventions targeting X could be effective.",
      "section_content_variation_2": "Our analysis revealed three key themes emerging from the data. Firstly, participants consistently reported... Secondly, quantitative data showed... Finally...",
      "section_content_variation_3": "A detailed examination of the results indicates a complex interplay of factors. While no single cause was identified, the evidence points towards Z as a major contributor."
    },
    {
      "section_id": "sec_conclusion_04",
      "section_name": "Conclusion and Future Outlook",
      "section_content_variation_1": "In conclusion, the findings underscore the importance of policy intervention. Future research should focus on longitudinal studies to track these trends over time.",
      "section_content_variation_2": "To summarize, our analysis reveals significant trends that warrant further investigation. We recommend that subsequent studies explore the impact of X on Y in different contexts.",
      "section_content_variation_3": "The evidence presented leads to the conclusion that proactive measures are essential. The path forward involves collaborative efforts across sectors and continued monitoring of outcomes."
    }
  ]
}

def initialize_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "input"
    if "article_text" not in st.session_state:
        st.session_state.article_text = ""
    if "article_data" not in st.session_state:
        st.session_state.article_data = None
    if "selected_variations" not in st.session_state:
        st.session_state.selected_variations = {}
    if "edited_texts_cache" not in st.session_state:
        st.session_state.edited_texts_cache = {}
    if "compiled_article" not in st.session_state:
        st.session_state.compiled_article = ""

def reset_app_state():
    st.session_state.page = "input"
    st.session_state.article_text = ""
    st.session_state.article_data = None
    st.session_state.selected_variations = {}
    st.session_state.edited_texts_cache = {}
    st.session_state.compiled_article = ""

def process_article_with_llm(article_content: str):
    if not article_content.strip():
        return None
    return SAMPLE_JSON_OUTPUT

def display_header():
    st.title(APP_TITLE)
    st.caption("Refine your articles by selecting and editing the best variation for each section.")
    st.divider()

def display_footer():
    st.divider()
    st.markdown(f"<p style='text-align: center; color: grey;'>{FOOTER_TEXT}</p>", unsafe_allow_html=True)

def display_input_screen():
    st.header("1. Input Your Article")
    article_text_input = st.text_area(
        "Paste your full article text here:",
        height=300,
        key="article_input_main_widget",
        value=st.session_state.get("article_text", "")
    )
    st.session_state.article_text = article_text_input
    if st.button("Process Article", type="primary", key="process_article_button"):
        if st.session_state.article_text.strip():
            with st.spinner("Processing article and generating sections..."):
                processed_data = process_article_with_llm(st.session_state.article_text)
            if processed_data and "article_data" in processed_data:
                st.session_state.article_data = processed_data["article_data"]
                st.session_state.selected_variations = {}
                st.session_state.edited_texts_cache = {}
                for section in st.session_state.article_data:
                    sec_id = section["section_id"]
                    st.session_state.edited_texts_cache[sec_id] = section["section_content_variation_1"]
                    st.session_state.selected_variations[sec_id] = section["section_content_variation_1"]
                st.session_state.page = "selection"
                st.rerun()
            else:
                st.error("Could not process the article. The simulated LLM did not return valid data.")
        else:
            st.warning("Please paste your article content above before processing.")

def display_selection_screen():
    st.header("2. Review and Edit Section Variations")

    if not st.session_state.article_data:
        st.error("No article data found. Please go back and process an article.")
        if st.button("Go to Input Page"):
            st.session_state.page = "input"
            st.rerun()
        return

    for i, section in enumerate(st.session_state.article_data):
        section_id = section["section_id"]
        section_name = section["section_name"]
        variations = [
            section["section_content_variation_1"],
            section["section_content_variation_2"],
            section["section_content_variation_3"]
        ]
        variation_labels = [f"Variation 1", f"Variation 2", f"Variation 3"]
        with st.expander(f"**{i+1}. {section_name}**", expanded=True):
            # Use tabs for each variation
            tab_objects = st.tabs(variation_labels)
            for idx, tab in enumerate(tab_objects):
                with tab:
                    key = f"{section_id}_tab_{idx}"
                    if section_id not in st.session_state.edited_texts_cache:
                        st.session_state.edited_texts_cache[section_id] = variations[0]
                    if st.session_state.edited_texts_cache.get(section_id, "") == "":
                        st.session_state.edited_texts_cache[section_id] = variations[0]
                    initial_value = (
                        st.session_state.edited_texts_cache[section_id]
                        if st.session_state.selected_variations.get(section_id, "") == variations[idx]
                        else variations[idx]
                    )
                    text = st.text_area(
                        "Edit the variation as you wish:",
                        value=initial_value,
                        height=160,
                        key=key
                    )
                    if st.button("Select This Variation", key=f"{section_id}_select_{idx}"):
                        st.session_state.selected_variations[section_id] = variations[idx]
                        st.session_state.edited_texts_cache[section_id] = text
                        st.success(f"Selected and saved Variation {idx+1} for this section.")

            # Show the currently selected (and possibly edited) variation below
            st.markdown("---")
            sel_content = st.session_state.edited_texts_cache.get(section_id, variations[0])
            st.markdown(f"**Currently selected/edited variation:**\n\n> {sel_content}")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Compile Final Article", type="primary", key="compile_button", use_container_width=True):
            compiled_html_parts = []
            for section_data in st.session_state.article_data:
                section_name = section_data["section_name"]
                section_id = section_data["section_id"]
                selected_content = st.session_state.edited_texts_cache.get(section_id)
                if selected_content:
                    # Safe basic HTML formatting; could be extended as needed
                    compiled_html_parts.append(f"<h3>{section_name}</h3>\n<p>{selected_content}</p>")
            st.session_state.compiled_article = "\n\n".join(compiled_html_parts)
            st.session_state.page = "final"
            st.rerun()
    with col2:
        if st.button("Back to Input", key="back_to_input_sel_button", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()

def display_final_screen():
    st.header("3. Your Compiled Article")
    if not st.session_state.compiled_article:
        st.warning("No article compiled yet. Please select variations and click 'Compile Final Article'.")
        if st.button("Go to Selection Page"):
            st.session_state.page = "selection"
            st.rerun()
        return
    # Show as rendered HTML with a styled container
    st.markdown('<div class="final-article-box">' + st.session_state.compiled_article + "</div>", unsafe_allow_html=True)
    st.caption("Your article is ready to copy or export.")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start New Article (Reset)", key="start_over_button", use_container_width=True):
            reset_app_state()
            st.rerun()
    with col2:
        if st.button("Back to Selections", key="back_to_selections_button", use_container_width=True):
            st.session_state.page = "selection"
            st.rerun()

def main():
    initialize_session_state()
    display_header()
    if st.session_state.page == "input":
        display_input_screen()
    elif st.session_state.page == "selection":
        display_selection_screen()
    elif st.session_state.page == "final":
        display_final_screen()
    display_footer()

if __name__ == "__main__":
    main()
