import streamlit as st
import pandas as pd

# Configure page layout to use the full width
st.set_page_config(layout="wide", page_title="Content Analysis Suite", page_icon="📄")

# --- Sidebar for navigation ---
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to:",
    ["Document Similarity", "Authoring Assistance"],
    key="navigation_selection"
)


def similarity_api_response():
    global response_payload
    # Example response JSON (simulated for demonstration)
    response_payload = {
        "response": {
            "matchingArticles": [
                {
                    "articleID": "ARTCL-001",
                    "articleURL": "http://example.com/matching-article-1",
                    "matchingPercentage": 85.4,
                    "reasonForMatching": "High overlap in key topics and terminology. Both discuss 'sustainable energy solutions'."
                },
                {
                    "articleID": "ARTCL-002",
                    "articleURL": "http://example.com/matching-article-2",
                    "matchingPercentage": 78.2,
                    "reasonForMatching": "Similar content structure, references similar studies on 'AI ethics'."
                },
                {
                    "articleID": "ARTCL-005",
                    "articleURL": "http://example.com/matching-article-3",
                    "matchingPercentage": 72.9,
                    "reasonForMatching": "Focuses on 'data privacy regulations', shares common citations."
                }
            ],
            "noMatchingArticles": [
                {
                    "articleID": "ARTCL-003",
                    "articleURL": "http://example.com/non-matching-article-1",
                    "matchingPercentage": 45.7,
                    "reasonForNotMatching": "Different topic focus: 'ancient history' vs. input 'AI ethics'."
                }
            ]
        }
    }
    # --- End of simulated API call section ---


# --- Document Similarity Page ---
if selection == "Document Similarity":
    # Main title for Document Similarity, styled with Amex blue
    st.markdown("<h1 style='color: #006FCF; text-align: left;'>Article Similarity Checker</h1>", unsafe_allow_html=True)

    st.markdown("Enter an article URL or paste the text directly to find similar articles from our database.")

    # Input type selection
    input_method_col1, input_method_col2 = st.columns([1, 3])
    with input_method_col1:
        is_url = st.checkbox("Input is URL", value=True, key="is_url_checkbox")

    # Depending on checkbox, show appropriate input field
    if is_url:
        value = st.text_input("Enter Article URL:", placeholder="e.g., https://www.example.com/article",
                              key="article_url_input")
    else:
        value = st.text_area("Enter Article Text:", height=200, placeholder="Paste your article text here...",
                             key="article_text_input")

    # Button to trigger similarity check
    if st.button("Check Similarity", key="check_similarity_button"):
        if not value.strip():
            st.warning("Please enter an article URL or text.")
        else:
            # Construct request JSON (though not displayed, it might be needed for an actual API call)
            request_payload = {
                "request": {
                    "type": "URL" if is_url else "Text",
                    "value": value,
                    "isURL": is_url,
                    "isText": not is_url
                }
            }

            # --- This is where you would typically make an API call ---
            # For demonstration, using the simulated response:
            # st.info("Simulating API call... Please replace this with your actual API integration.") # Removed this line

            similarity_api_response()

            st.markdown("---")  # Visual separator
            # Removed Request Details section
            # st.subheader("Request Details")
            # st.json(request_payload)
            # st.markdown("---") # Visual separator

            # Extract matching and non-matching articles
            matching_articles = response_payload["response"].get("matchingArticles", [])
            non_matching_articles = response_payload["response"].get("noMatchingArticles", [])

            # Display matching articles in a table
            if matching_articles:
                st.subheader("Highly Similar Articles Found")
                df_match = pd.DataFrame(matching_articles)
                df_match = df_match.rename(columns={
                    "articleID": "Article ID",
                    "articleURL": "Article URL",
                    "matchingPercentage": "Similarity (%)",
                    "reasonForMatching": "Basis of Similarity"
                })
                st.dataframe(df_match)
            else:
                st.info("No highly similar articles found based on the provided input.")

            # Display non-matching (or less similar) articles if any
            if non_matching_articles:
                st.subheader("Less Similar Articles / Potential Distinctions")
                df_non = pd.DataFrame(non_matching_articles)
                df_non = df_non.rename(columns={
                    "articleID": "Article ID",
                    "articleURL": "Article URL",
                    "matchingPercentage": "Similarity (%)",
                    "reasonForNotMatching": "Reason for Lower Similarity"
                })
                st.dataframe(df_non)
            elif not matching_articles:
                pass
            else:
                st.success("All other analyzed articles were below the distinct similarity threshold.")


# --- Authoring Assistance Page ---
elif selection == "Authoring Assistance":
    # Main title for Authoring Assistance, styled with Amex blue
    st.markdown("<h1 style='color: #006FCF; text-align: left;'>Assisted Authoring</h1>",
                unsafe_allow_html=True)

    st.markdown(
        "This section is designed to provide tools and insights to assist with content creation, editing, and formatting. Explore the features below to streamline your writing process.")

    st.info("🚧 This section is currently under development. More features coming soon! 🚧", icon="🛠️")

    # Placeholder for future features
    st.subheader("Upcoming Features:")
    st.markdown("""
    - **Check similar content :** Find similar content across systems.
    - **Assisted Authoring:** AI working with Authors to create a document with Author's feedback.
    - **Grammar and Style Checker:** Advanced checks beyond basic spell-checking.
    - **Content Formatting Utilities:** Tools to easily structure and format your articles.
    """)

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 1rem;">
        <small>@ GSG | Global Servicing Group| Content Analysis Suite v1.0</small>
    </div>
    """, unsafe_allow_html=True
)
