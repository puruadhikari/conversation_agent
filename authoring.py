import streamlit as st
import pandas as pd

# Configure Streamlit page settings
st.set_page_config(
    page_title="Content Analysis Suite",
    page_icon="📄",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Feature", ["Document Similarity", "Authoring Assistance"])

# Helper function for simulated API response
def get_similarity_response():
    return {
        "matchingArticles": [
            {"ID": "ARTCL-001", "URL": "http://example.com/article-1", "Similarity (%)": 85.4, "Reason": "High overlap in key topics (sustainable energy solutions)."},
            {"ID": "ARTCL-002", "URL": "http://example.com/article-2", "Similarity (%)": 78.2, "Reason": "Similar structure and citations on AI ethics."},
            {"ID": "ARTCL-005", "URL": "http://example.com/article-3", "Similarity (%)": 72.9, "Reason": "Common focus on data privacy regulations."}
        ],
        "nonMatchingArticles": [
            {"ID": "ARTCL-003", "URL": "http://example.com/article-4", "Similarity (%)": 45.7, "Reason": "Topic mismatch: ancient history vs AI ethics."}
        ]
    }

# Page: Document Similarity
if page == "Document Similarity":
    st.title("🔍 Article Similarity Checker")

    st.markdown("Enter an article URL or paste the article text to find similar articles.")

    input_type = st.radio("Select input type:", ["URL", "Text"], horizontal=True)

    if input_type == "URL":
        user_input = st.text_input("Article URL", placeholder="https://www.example.com/article")
    else:
        user_input = st.text_area("Article Text", height=200, placeholder="Paste the text of your article here.")

    if st.button("Check Similarity", type="primary"):
        if not user_input.strip():
            st.warning("Please provide a valid URL or text to proceed.")
        else:
            response = get_similarity_response()
            matching, non_matching = response["matchingArticles"], response["nonMatchingArticles"]

            st.divider()

            if matching:
                st.subheader("✅ Highly Similar Articles")
                df_matching = pd.DataFrame(matching)
                st.dataframe(df_matching, use_container_width=True)
            else:
                st.info("No highly similar articles found.")

            if non_matching:
                st.subheader("⚠️ Less Similar Articles")
                df_non_matching = pd.DataFrame(non_matching)
                st.dataframe(df_non_matching, use_container_width=True)

# Page: Authoring Assistance
elif page == "Authoring Assistance":
    st.title("✍️ Assisted Authoring")

    st.markdown("This tool supports content creation and editing with advanced features.")

    st.warning("🚧 Feature Under Development 🚧", icon="🛠️")

    st.subheader("Upcoming Features")
    st.markdown("""
    - **Content Similarity Check:** Analyze similar content across systems.
    - **AI-assisted Writing:** Collaborative content creation with AI recommendations.
    - **Grammar and Style Enhancement:** Advanced grammar and style checks.
    - **Formatting Utilities:** Effortlessly structure and format articles.
    """)

# Footer
st.divider()
st.markdown(
    """<div style='text-align: center; padding: 0.5rem;'>
        <small>© GSG | Global Servicing Group | Content Analysis Suite v1.0</small>
    </div>""",
    unsafe_allow_html=True
)
