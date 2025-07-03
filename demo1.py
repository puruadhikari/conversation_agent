import streamlit as st

def local_css():
    """
    Applies custom CSS styling to the Streamlit app.
    All styles, including for the table, are consolidated here.
    """
    custom_css = """
    html, body {
        margin: 0;
        padding: 0;
        background-color: #ffffff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .block-container {
        padding: 0.5rem 1rem 1rem 1rem;
    }
    .custom-header {
        background-color: #016fd0;
        color: white;
        margin: -0.5rem -1rem 0 -1rem;
        padding: 1rem 1.75rem;
        font-size: 1.25rem;
        border-bottom: 3px solid #005aa7;
    }
    .main-content {
        padding: 0.5rem 1.75rem;
    }
    div[data-testid="stTextInput"] input {
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        height: 42px;
        width: 100%;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #016fd0;
        box-shadow: 0 0 5px rgba(1, 111, 208, 0.5);
    }
    div[data-testid="stButton"] > button {
        background-color: #016fd0;
        color: white !important;
        border-radius: 4px;
        padding: 0.75rem;
        font-size: 1rem;
        border: none;
        height: 42px;
        width: 100%;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #005aa7;
    }
    .search-result-container {
        margin-top: 1.5rem;
        border-top: 2px solid #eeeeee;
        padding-top: 1rem;
    }
    .search-result {
        background-color: #f7f9fc;
        border: 1px solid #e0e6ef;
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .search-result h3 {
        color: #016fd0;
        margin-top: 0;
    }
    .search-result a {
        color: #016fd0;
        text-decoration: none;
        font-weight: bold;
    }
    .search-result a:hover {
        text-decoration: underline;
    }

    /* --- STYLES FOR THE RESULTS TABLE --- */
    .styled-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.95em;
        font-family: 'Helvetica Neue', sans-serif;
        width: 100%;
        table-layout: fixed;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
    }
    .styled-table thead tr {
        background-color: #016fd0;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th, .styled-table td {
        padding: 12px 15px;
        border: 1px solid #e0e6ef;
        vertical-align: top;
        word-wrap: break-word;
    }
    .styled-table th:nth-child(1), .styled-table td:nth-child(1) {
        width: 25%;
    }
    .styled-table th:nth-child(2), .styled-table td:nth-child(2) {
        width: 60%;
    }
    .styled-table th:nth-child(3), .styled-table td:nth-child(3) {
        width: 15%;
    }
    .styled-table tbody tr {
        background-color: #f7f9fc;
    }
    .styled-table tbody tr:hover {
        background-color: #eaf2fa;
    }
    """
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Semantic Cache Demo", layout="wide")

    local_css()

    st.markdown(
        '<div class="custom-header">AMERICAN EXPRESS | '
        '<span style="font-weight: normal; font-size: 1rem;">Semantic Cache Demo</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    st.markdown(
        "<h1 style='font-weight: normal; margin-top: 0;'>CHC Semantic Cache</h1>",
        unsafe_allow_html=True
    )
    st.write("Enter a query below to find for similar questions from cache.")

    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "Search", placeholder="e.g., 'Benefits of Gold card?'", label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("Search")

    if search_button and search_query:
        st.markdown('<div class="search-result-container">', unsafe_allow_html=True)
        st.subheader(f"Top 3 Results for '{search_query}'")

        # Mock data for demonstration
        results = [
            {
                "title": "Q3 2024 Financial Performance Review",
                "snippet": "Covering our Q3 2024 performance, this document provides an in-depth analysis of revenue streams, cost-saving measures, and future financial projections.",
                "score": "0.91"
            },
            {
                "title": "Marketing Strategy for Project Phoenix",
                "snippet": "This end-to-end marketing blueprint outlines the target audience, key messaging, and channel strategy for the upcoming launch of Project Phoenix.",
                "score": "0.82"
            },
            {
                "title": "Employee Onboarding and IT Policy Guide",
                "snippet": "Serving as both a welcoming handshake and a crucial resource, this guide covers everything a new hire needs to know about our IT policies and procedures.",
                "score": "0.74"
            }
        ]

        # Display results in the card-like format
        for result in results:
            st.markdown(
                f"""
                <div class="search-result">
                    <h3>{result['title']}</h3>
                    <p>{result['snippet']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # Add a checkbox to toggle the table view
        show_table = st.checkbox("Show Table Format")

        if show_table:
            st.markdown("### Tabular View of Results")

            # --- FIX: Build the HTML for the table rows ---
            rows_html = ""
            for result in results:
                rows_html += (
                    f"<tr>"
                    f"<td>{result['title']}</td>"
                    f"<td>{result['snippet']}</td>"
                    f"<td>{result['score']}</td>"
                    f"</tr>"
                )

            # --- FIX: Combine all parts into the final table HTML ---
            # The <style> tag is removed from here and placed in the local_css function
            table_html = f"""
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Snippet</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            """
            
            # Render the final HTML table
            st.markdown(table_html, unsafe_allow_html=True)

    elif search_button:
        st.warning("Please enter a search term.")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
