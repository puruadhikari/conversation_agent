import streamlit as st

def local_css():
    custom_css = """
    html, body {
        margin: 0;
        padding: 0;
        background-color: #ffffff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Streamlit default container override */
    .block-container {
        padding: 0.5rem 1rem 1rem 1rem; /* top, horizontal, bottom */
    }
    /* Header – span full viewport width (flush left & right) */
    .custom-header {
        background-color: #016fd0;
        color: white;
        /* pull header out of the block‑container padding */
        margin: -0.5rem -1rem 0 -1rem; /* negate top & horizontal gutters */
        padding: 1rem 1.75rem;          /* keep internal breathing room */
        font-size: 1.25rem;
        border-bottom: 3px solid #005aa7;
    }
    /* Main Content */
    .main-content {
        padding: 0.5rem 1.75rem;        /* matches header inner padding */
    }
    /* Text Input */
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
    /* Button */
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
    /* Search Results */
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
    """
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Semantic Cache Demo", layout="wide")
    st.set_page_config(
        page_title="Semantic Cache Demo",
        page_icon="https://www.americanexpress.com/favicon.ico"
    )

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
            "Search", placeholder="e.g., 'Benefits of Gold card?", label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("Search")

    if search_button and search_query:
        st.markdown('<div class="search-result-container">', unsafe_allow_html=True)
        st.subheader(f"Top 3 Results for '{search_query}'")

        results = [
            {
                "title": "Q3 2024 Financial Performance Review",
                "snippet": "Covering our Q3 2024 performance in a comprehensive yet actionable fashion, this review walks the reader from a top-line, quarter-over-quarter revenue climb driven by resilient subscription renewals, through margin dynamics shaped by disciplined cost controls, to a deep dive into departmental variance—highlighting how Engineering absorbed increased R&D spend, how Sales benefited from a shorter deal cycle in EMEA, and how G&A trimmed discretionary expenses—before crystallising the headline numbers into three concise ratios that track progress against the annual plan, clarifying why free cash flow grew faster than headline profit, what risk factors may pressure Q4, and which corrective actions leadership has already budgeted, all in language geared toward board directors who need a single, data-rich narrative they can reference during the October strategy session and who value a candid, numbers-first lens on both wins and warning signs, ensuring the document is not merely retrospective but forward-looking, linking financial outcomes to product roadmap milestones, talent retention indicators, and macroeconomic scenarios so that decisions on investment, hiring, and pricing are grounded in measurable insight; moreover, scenario sensitivity tables translate potential currency fluctuations into tangible earnings-per-share impacts.",
                "score": "0.91"
            },
            {
                "title": "Marketing Strategy for Project Phoenix",
                "snippet": "This end-to-end marketing blueprint for Project Phoenix opens by clearly defining a segmented, five-persona target audience, each mapped to explicit pain points our next-generation workflow-automation suite resolves, then layers these personas onto an integrated funnel that fuses brand-awareness thought-leadership, mid-funnel comparison guides, and bottom-funnel demos into a cohesive journey measured through six lagging and leading KPIs—including cost-per-marketing-qualified-lead, product-qualified-lead conversion rate, trial-to-subscribe velocity, and share-of-voice within the analyst community—while assigning ownership across Growth, Content, and Field teams via a RACI chart that eliminates grey areas; strategic levers such as AI-assisted account scoring, partner-led webinars, and influencer dark-social loops are justified with benchmark data to project channel ROI over four campaign sprints, after which a dynamic budget-reallocation model shifts spend toward the best-performing cohorts in real time, ensuring incremental dollars land where marginal lift is greatest; finally, risk-mitigation tactics—for GDPR compliance, brand safety, and market-entry timing—are paired with clearly defined exit and pivot criteria so executives can pull the plug or double down quickly without sacrificing learning velocity or sunk-cost discipline, and monthly executive dashboards with quarterly retrospective workshops complete the loop, turning raw campaign signals into strategy-shaping intelligence for the next release cycle.",
                "score": "0.82"
            },
            {
                "title": "Employee Onboarding and IT Policy Guide",
                "snippet": "Serving as both a welcoming handshake and a compliance safeguard, this employee-onboarding and IT-policy playbook escorts new hires from pre-start credential provisioning to their first thirty-day performance check-in through a single, narrative thread that blends culture, security, and productivity mandates into an easily navigable sequence; it begins with a clear, step-by-step orientation roadmap covering workstation setup, multi-factor authentication activation, and encrypted-device policies, then layers in human-resources essentials—benefit elections, code-of-conduct acknowledgements, and diversity commitments—before transitioning into role-specific enablement modules curated by department managers, each with embedded micro-learning videos and sandbox tasks to reinforce knowledge retention; automated checkpoints track completion and feed real-time dashboards for managers, while escalation rules trigger friendly nudges if deadlines slip, maintaining both regulatory posture and employee confidence; appended reference sections translate complex ISO 27001 controls and data-handling standards into practical ‘do-and-don’t’ lists, reducing cognitive load; finally, a feedback loop via anonymous pulse surveys captures sentiment and surfaces iterative improvements so the guide stays living, breathing, and aligned with evolving threat landscapes, remote-work norms, and talent-experience expectations, ensuring compliance never feels like bureaucracy at the expense of belonging.",
                "score": "0.74"
            }
        ]

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
    elif search_button:
        st.warning("Please enter a search term.")

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
