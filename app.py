import streamlit as st
import requests
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SQLMIND — AI Data Copilot",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(6, 182, 212, 0.12),
                transparent 25%
            ),
            #08090d;
        color: #f5f5f5;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: #0d0f15;
        border-right: 1px solid rgba(255,255,255,0.07);
        width: 260px !important;
        min-width: 260px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 260 px !important
    }

    .brand {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        color: #a78bfa;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .hero-title {
        font-size: 3.8rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 1rem;

        background: linear-gradient(
            90deg,
            #ffffff 0%,
            #c4b5fd 45%,
            #67e8f9 100%
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #9ca3af;
        max-width: 720px;
        line-height: 1.7;
        margin-bottom: 2rem;
    }

    .pipeline-title {
        color: #71717a;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .pipeline {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 1rem 0 2rem 0;
        flex-wrap: wrap;
    }


    .pipeline-arrow {
        color: #6366f1;
        font-size: 1rem;
    }

    .section-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #71717a;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0.7rem;
    }

    textarea {
        background: #0d0f15 !important;
        color: #f5f5f5 !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 16px !important;
        caret-color: #a78bfa !important;
    }

    textarea::placeholder {
        color: #52525b !important;
    }

    textarea:focus {
        background: #0d0f15 !important;
        border: 1px solid rgba(139,92,246,0.8) !important;
        box-shadow:
            0 0 0 1px rgba(139,92,246,0.25),
            0 0 30px rgba(139,92,246,0.08) !important;
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(167,139,250,0.25);
        background: rgba(124,58,237,0.12);
        color: #e9d5ff;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(167,139,250,0.55);
        background: rgba(124,58,237,0.22);
        transform: translateY(-1px);
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    hr {
        border-color: rgba(255,255,255,0.07) !important;
    }

    /* ============================================================
   TEXT VISIBILITY FIX
   ============================================================ */

/* General text */
.stApp,
.stApp p,
.stApp label,
.stApp span {
    color: #e5e7eb;
}

/* Sidebar text */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #d4d4d8 !important;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] h6 {
    color: #f4f4f5 !important;
}

/* Database Explorer expander text */
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    color: #e4e4e7 !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #e4e4e7 !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary span {
    color: #e4e4e7 !important;
}

/* Column names inside expanders */
section[data-testid="stSidebar"] [data-testid="stExpander"] p {
    color: #a1a1aa !important;
}

/* Sidebar captions */
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #a1a1aa !important;
}

/* Sidebar divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #a1a1aa !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #f4f4f5 !important;
}

/* Main markdown text */
.main p,
.main span,
.main label {
    color: #d4d4d8;
}

/* Buttons */
.stButton > button {
    color: #f4f4f5 !important;
}

/* Text area */
textarea {
    color: #f4f4f5 !important;
}

/* Text area placeholder */
textarea::placeholder {
    color: #71717a !important;
}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "question" not in st.session_state:
    st.session_state.question = ""


# ============================================================
# API CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">◈ SQLMIND</div>

        <div style="
            color:#9ca3af;
            font-size:0.82rem;
            line-height:1.6;
            margin-bottom:1.5rem;
        ">
            AI-powered natural language interface for SQL databases.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # DATABASE EXPLORER
    # --------------------------------------------------------

    st.markdown("### 🗄️ Database Explorer")

    schemas = {
        "customers": [
            "customer_id",
            "name",
            "city"
        ],
        "orders": [
            "order_id",
            "customer_id",
            "order_date",
            "total_amount"
        ],
        "products": [
            "product_id",
            "product_name",
            "category",
            "price"
        ],
        "order_items": [
            "order_id",
            "product_id",
            "quantity",
            "unit_price"
        ],
        "employees": [
            "employee_id",
            "name",
            "department",
            "salary"
        ]
    }

    for table, columns in schemas.items():

        with st.expander(
            table,
            expanded=False
        ):

            for column in columns:
                st.caption(f"• {column}")

    # --------------------------------------------------------
    # BACKEND STATUS
    # --------------------------------------------------------

    st.divider()

    st.markdown("### 🔌 Backend")

    try:

        health_response = requests.get(
            f"{API_URL}/",
            timeout=3
        )

        if health_response.status_code == 200:

            st.success("● FastAPI Connected")

        else:

            st.error("FastAPI unavailable")

    except requests.exceptions.RequestException:

        st.error("● FastAPI Offline")

    # --------------------------------------------------------
    # STACK
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            color:#52525b;
            font-size:0.7rem;
            margin-top:1.5rem;
            line-height:1.7;
        ">
            Backend · FastAPI<br>
            Database · SQLite<br>
            AI Engine · Gemini
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HERO
# ============================================================

top_left, top_right = st.columns(
    [3, 2],
    gap="large"
)


# ============================================================
# LEFT HERO
# ============================================================

with top_left:

    st.markdown(
        '<div class="brand">◈ AI DATA COPILOT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-title">
            Talk to your<br>
            database.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Ask questions in plain English. SQLMIND understands your intent,
            generates SQL, validates it, and retrieves your data through a
            secure API pipeline.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT HERO
# ============================================================

with top_right:

    st.markdown("### ⚡ AI Engine")

    st.success("● System Online")

    st.markdown(
        "Your natural-language queries are processed through "
        "the SQL validation pipeline."
    )

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:

        st.metric(
            "AI",
            "Gemini"
        )

        st.metric(
            "Database",
            "SQLite"
        )

    with metric_col2:

        st.metric(
            "API",
            "FastAPI"
        )

        st.metric(
            "Safety",
            "Active"
        )


# ============================================================
# PIPELINE
# ============================================================

# ============================================================
# PIPELINE
# ============================================================

st.markdown("##### AI PROCESSING PIPELINE")

pipeline_cols = st.columns([1.3, 0.25, 1.3, 0.25, 1.3, 0.25, 1.3, 0.25, 1.3])

pipeline_items = [
    ("💬", "Question"),
    ("✦", "Gemini"),
    ("⚙", "SQL"),
    ("✓", "Validation"),
    ("🗄️", "SQLite")
]

for i, (icon, label) in enumerate(pipeline_items):

    with pipeline_cols[i * 2]:
        st.markdown(f"**{icon} {label}**")

    if i < len(pipeline_items) - 1:
        with pipeline_cols[i * 2 + 1]:
            st.markdown("→")


# ============================================================
# QUERY INPUT
# ============================================================

st.markdown(
    '<div class="section-label">Ask your database</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "",
    value=st.session_state.question,
    placeholder="Ask anything about your database...",
    height=115,
    label_visibility="collapsed"
)


# ============================================================
# EXAMPLE PROMPTS
# ============================================================

# ============================================================
# EXAMPLE PROMPTS
# ============================================================

st.caption("QUICK START")

example_cols = st.columns(4)

examples = [
    "Show me all customers",
    "Customers from Mumbai",
    "Top customers by spending",
    "How many employees?"
]

for i, example in enumerate(examples):

    with example_cols[i]:

        if st.button(
            example,
            key=f"example_{i}",
            use_container_width=True
        ):
            st.session_state.question = example
            st.rerun()


# ============================================================
# GENERATE BUTTON
# ============================================================

st.write("")

generate_col1, generate_col2 = st.columns(
    [5, 1]
)

with generate_col1:

    st.markdown(
        """
        <div style="
            color:#52525b;
            font-size:0.72rem;
            padding-top:0.65rem;
        ">
            Press <b style="color:#71717a;">Generate</b>
            to send your question to the AI pipeline.
        </div>
        """,
        unsafe_allow_html=True
    )

with generate_col2:

    generate_clicked = st.button(
        "✨ Generate",
        type="primary",
        use_container_width=True
    )


# ============================================================
# SEND REQUEST TO FASTAPI
# ============================================================

if generate_clicked:

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        st.session_state.question = question

        with st.spinner("AI is thinking..."):

            try:

                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": question.strip()
                    },
                    timeout=120
                )

                if response.status_code != 200:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            response.text
                        )

                    except Exception:

                        error_message = response.text

                    st.error(
                        f"Backend error: {error_message}"
                    )

                else:

                    st.session_state.last_response = (
                        response.json()
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "⚠️ Cannot connect to FastAPI. "
                    "Make sure the backend is running on "
                    "http://127.0.0.1:8000"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ The request timed out. "
                    "The AI service may be temporarily busy."
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"Network error: {error}"
                )


# ============================================================
# DISPLAY API RESPONSE
# ============================================================

data = st.session_state.last_response


if data:

    st.divider()

    status = data.get("status")
    intent = data.get("intent")
    corrected_question = data.get("corrected_question")
    sql = data.get("sql")
    results = data.get("results")
    message = data.get("message")
    clarification = data.get("clarification_question")


    # --------------------------------------------------------
    # CORRECTED QUESTION
    # --------------------------------------------------------

    if (
        corrected_question
        and corrected_question.strip()
        != data.get("question", "").strip()
    ):

        st.info(
            f"✎ **Corrected question:** "
            f"{corrected_question}"
        )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status_col1, status_col2 = st.columns(
        [1, 5]
    )

    with status_col1:

        if intent:
            st.markdown(
                f"`{intent}`"
            )

    with status_col2:

        if status == "success":

            st.success(
                "✓ Query executed successfully"
            )

        elif status == "clarification_required":

            st.warning(
                "⚠ Clarification required"
            )

        elif status == "confirmation_required":

            st.warning(
                "⚠ Confirmation required"
            )

        elif status == "unsafe_operation":

            st.error(
                "🛡 Operation blocked"
            )

        elif status in [
            "validation_failed",
            "semantic_validation_failed",
            "execution_failed"
        ]:

            st.error(
                "✕ Query processing failed"
            )


    # --------------------------------------------------------
    # CLARIFICATION
    # --------------------------------------------------------

    if status == "clarification_required":

        st.markdown(
            '<div class="section-label">'
            'AI needs more information'
            '</div>',
            unsafe_allow_html=True
        )

        st.warning(
            clarification
            or
            "Please clarify your question."
        )


    # --------------------------------------------------------
    # GENERATED SQL
    # --------------------------------------------------------

    if sql:

        st.markdown(
            '<div class="section-label">'
            'Generated SQL'
            '</div>',
            unsafe_allow_html=True
        )

        st.code(
            sql,
            language="sql"
        )


    # --------------------------------------------------------
    # MESSAGE
    # --------------------------------------------------------

    if message:

        if status == "success":

            st.success(message)

        elif status in [
            "validation_failed",
            "semantic_validation_failed",
            "execution_failed",
            "unsafe_operation"
        ]:

            st.error(message)

        else:

            st.info(message)


    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if (
        status == "success"
        and results is not None
    ):

        st.markdown(
            '<div class="section-label">'
            'Query Results'
            '</div>',
            unsafe_allow_html=True
        )

        if results:

            df = pd.DataFrame(results)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"{len(df)} row(s) returned"
            )

        else:

            st.info(
                "The query executed successfully "
                "but returned no rows."
            )


    # --------------------------------------------------------
    # WRITE OPERATION
    # --------------------------------------------------------

    if status == "confirmation_required":

        st.markdown(
            '<div class="section-label">'
            'Database Modification'
            '</div>',
            unsafe_allow_html=True
        )

        st.warning(
            "⚠️ This operation will modify your database. "
            "Review the generated SQL before executing it."
        )

        st.info(
            "The API currently generates and validates "
            "write operations but does not expose a "
            "write-execution endpoint yet."
        )


    # --------------------------------------------------------
    # UNSAFE OPERATION
    # --------------------------------------------------------

    if status == "unsafe_operation":

        st.error(
            "🛡️ Operation blocked by the safety layer."
        )

        st.caption(
            "The generated operation did not satisfy "
            "the project's database safety rules."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:4rem;
        padding-top:1.5rem;
        border-top:1px solid rgba(255,255,255,0.06);
        color:#52525b;
        font-size:0.72rem;
    ">
        SQLMIND · Natural Language → SQL ·
        FastAPI + Gemini + SQLite
    </div>
    """,
    unsafe_allow_html=True
)