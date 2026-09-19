import os
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

    /* ========================================================
       GLOBAL APP
       ======================================================== */

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
        overflow-x: hidden;
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


    /* ========================================================
       FLOATING BACKGROUND GLOWS
       ======================================================== */

    .stApp::before {
        content: "";
        position: fixed;
        width: 420px;
        height: 420px;
        border-radius: 50%;
        background: rgba(124, 58, 237, 0.06);
        filter: blur(90px);
        top: 10%;
        left: -180px;
        pointer-events: none;
        animation: floatGlow 9s ease-in-out infinite;
        z-index: 0;
    }

    .stApp::after {
        content: "";
        position: fixed;
        width: 360px;
        height: 360px;
        border-radius: 50%;
        background: rgba(6, 182, 212, 0.05);
        filter: blur(90px);
        bottom: 5%;
        right: -160px;
        pointer-events: none;
        animation: floatGlowReverse 11s ease-in-out infinite;
        z-index: 0;
    }

    @keyframes floatGlow {

        0%, 100% {
            transform: translate(0px, 0px);
        }

        50% {
            transform: translate(45px, 30px);
        }
    }

    @keyframes floatGlowReverse {

        0%, 100% {
            transform: translate(0px, 0px);
        }

        50% {
            transform: translate(-35px, -25px);
        }
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #0d0f15 !important;
        border-right: 1px solid rgba(255,255,255,0.07);
        width: 260px !important;
        min-width: 260px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 260px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }


    /* ========================================================
       SIDEBAR TEXT
       ======================================================== */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #d4d4d8 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6 {
        color: #f4f4f5 !important;
    }


    /* ========================================================
       SIDEBAR EXPANDERS
       ======================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stExpander"] {
        color: #e4e4e7 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stExpander"] summary {
        color: #e4e4e7 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stExpander"] summary span {
        color: #e4e4e7 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stExpander"] p {
        color: #a1a1aa !important;
    }

    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {
        color: #a1a1aa !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12) !important;
    }


    /* ========================================================
       SIDEBAR BRAND
       ======================================================== */

    .sidebar-brand {
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }

    .sidebar-brand-symbol {
        display: inline-block;
        color: #a78bfa;
        animation: symbolPulse 3s ease-in-out infinite;
    }

    @keyframes symbolPulse {

        0%, 100% {
            opacity: 0.65;
            transform: scale(1);
        }

        50% {
            opacity: 1;
            transform: scale(1.08);
        }
    }


    /* ========================================================
       BRAND
       ======================================================== */

    .brand {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        color: #a78bfa;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        animation: brandPulse 3s ease-in-out infinite;
    }

    @keyframes brandPulse {

        0%, 100% {
            opacity: 0.7;
        }

        50% {
            opacity: 1;
        }
    }


    /* ========================================================
       HERO
       ======================================================== */

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

        animation: heroReveal 0.9s ease-out both;
    }

    @keyframes heroReveal {

        from {
            opacity: 0;
            transform: translateY(18px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    /* ========================================================
       TYPEWRITER
       ======================================================== */

    .typewriter {
        display: inline-block;
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #a78bfa;
        width: 0;

        animation:
            typing 2.4s steps(23, end) forwards,
            cursorBlink 0.8s step-end infinite;

        animation-delay: 0.35s;
    }

    @keyframes typing {

        from {
            width: 0;
        }

        to {
            width: 23ch;
        }
    }

    @keyframes cursorBlink {

        0%, 50% {
            border-color: #a78bfa;
        }

        51%, 100% {
            border-color: transparent;
        }
    }


    /* ========================================================
       HERO SUBTITLE
       ======================================================== */

    .hero-subtitle {
        font-size: 1.05rem;
        color: #9ca3af;
        max-width: 720px;
        line-height: 1.7;
        margin-bottom: 2rem;

        animation:
            subtitleReveal 1s ease-out 1.4s both;
    }

    @keyframes subtitleReveal {

        from {
            opacity: 0;
            transform: translateY(8px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    /* ========================================================
       AI ENGINE
       ======================================================== */

    .ai-engine-title {
        animation: cardReveal 0.8s ease-out 0.3s both;
    }

    @keyframes cardReveal {

        from {
            opacity: 0;
            transform: translateY(12px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    /* ========================================================
       ONLINE STATUS
       ======================================================== */

    .online-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #d4d4d8;
        font-size: 0.9rem;
    }

    .online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #34d399;

        box-shadow:
            0 0 0 0 rgba(52,211,153,0.6);

        animation:
            onlinePulse 2s infinite;
    }

    @keyframes onlinePulse {

        0% {
            box-shadow:
                0 0 0 0 rgba(52,211,153,0.55);
        }

        70% {
            box-shadow:
                0 0 0 8px rgba(52,211,153,0);
        }

        100% {
            box-shadow:
                0 0 0 0 rgba(52,211,153,0);
        }
    }


    /* ========================================================
       SECTION LABELS
       ======================================================== */

    .section-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #a1a1aa;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0.7rem;
    }


    /* ========================================================
       QUERY TEXT AREA
       ======================================================== */

    textarea {
        background: #0d0f15 !important;
        color: #f5f5f5 !important;

        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 16px !important;

        caret-color: #a78bfa !important;

        transition:
            border-color 0.3s ease,
            box-shadow 0.3s ease,
            transform 0.2s ease !important;

        animation:
            queryGlow 5s ease-in-out infinite;
    }

    textarea::placeholder {
        color: #71717a !important;
    }

    textarea:focus {
        background: #0d0f15 !important;

        border: 1px solid rgba(139,92,246,0.8) !important;

        box-shadow:
            0 0 0 1px rgba(139,92,246,0.25),
            0 0 30px rgba(139,92,246,0.08) !important;

        transform: translateY(-1px);

        animation: none;
    }

    @keyframes queryGlow {

        0%, 100% {
            box-shadow:
                0 0 0 rgba(139,92,246,0);
        }

        50% {
            box-shadow:
                0 0 22px rgba(139,92,246,0.05);
        }
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 12px;

        border: 1px solid rgba(167,139,250,0.25);

        background:
            rgba(124,58,237,0.12);

        color: #f4f4f5 !important;

        font-weight: 600;

        transition:
            all 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(167,139,250,0.65);

        background:
            rgba(124,58,237,0.22);

        transform:
            translateY(-2px);

        box-shadow:
            0 8px 24px rgba(124,58,237,0.12);
    }

    .stButton > button:active {
        transform:
            translateY(0px) scale(0.98);
    }


    /* ========================================================
       GENERATE BUTTON
       ======================================================== */

    button[kind="primary"] {

        box-shadow:
            0 0 0 rgba(139,92,246,0);

        animation:
            generateGlow 3s ease-in-out infinite;
    }

    button[kind="primary"]:hover {

        box-shadow:
            0 0 25px rgba(139,92,246,0.25);
    }

    @keyframes generateGlow {

        0%, 100% {
            box-shadow:
                0 0 0 rgba(139,92,246,0);
        }

        50% {
            box-shadow:
                0 0 18px rgba(139,92,246,0.12);
        }
    }


    /* ========================================================
       PIPELINE
       ======================================================== */

    .pipeline-title {
        animation:
            pipelineReveal 0.8s ease-out 1.2s both;
    }

    @keyframes pipelineReveal {

        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }

    .pipeline-node {
        text-align: center;

        padding:
            0.45rem 0.2rem;

        border:
            1px solid rgba(255,255,255,0.06);

        border-radius:
            10px;

        background:
            rgba(255,255,255,0.015);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            background 0.25s ease,
            box-shadow 0.25s ease;

        animation:
            pipelineFlow 4s ease-in-out infinite;
    }

    .pipeline-node:hover {
        transform:
            translateY(-3px);

        border-color:
            rgba(167,139,250,0.5);

        background:
            rgba(124,58,237,0.10);

        box-shadow:
            0 0 22px rgba(139,92,246,0.15);
    }

    @keyframes pipelineFlow {

        0%, 100% {
            border-color:
                rgba(255,255,255,0.06);

            box-shadow:
                0 0 0 rgba(139,92,246,0);
        }

        20% {
            border-color:
                rgba(167,139,250,0.65);

            box-shadow:
                0 0 20px rgba(139,92,246,0.16);
        }

        40% {
            border-color:
                rgba(255,255,255,0.06);

            box-shadow:
                0 0 0 rgba(139,92,246,0);
        }
    }

    .pipeline-arrow {
        text-align: center;

        color: #71717a;

        font-size: 1rem;

        animation:
            arrowFlow 4s ease-in-out infinite;
    }

    @keyframes arrowFlow {

        0%, 15% {
            opacity: 0.25;
            transform: translateX(0);
        }

        25% {
            opacity: 1;
            color: #a78bfa;
            transform: translateX(3px);
        }

        40%, 100% {
            opacity: 0.3;
            transform: translateX(0);
        }
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }


    /* ========================================================
       RESPONSE REVEAL
       ======================================================== */

    [data-testid="stDataFrame"],
    pre,
    [data-testid="stAlert"] {

        animation:
            resultReveal 0.5s ease-out both;
    }

    @keyframes resultReveal {

        from {
            opacity: 0;
            transform: translateY(8px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color:
            rgba(255,255,255,0.07) !important;
    }


    /* ========================================================
       GLOBAL TEXT VISIBILITY
       ======================================================== */

    .stApp,
    .stApp p,
    .stApp label {
        color: #e5e7eb;
    }

    .main p,
    .main span,
    .main label {
        color: #d4d4d8;
    }

    [data-testid="stMetricLabel"] {
        color: #a1a1aa !important;
    }

    [data-testid="stMetricValue"] {
        color: #f4f4f5 !important;
    }

    textarea {
        color: #f4f4f5 !important;
    }

    textarea::placeholder {
        color: #71717a !important;
    }


    /* ========================================================
       REDUCED MOTION
       ======================================================== */

    @media (prefers-reduced-motion: reduce) {

        *,
        *::before,
        *::after {

            animation-duration:
                0.01ms !important;

            animation-iteration-count:
                1 !important;

            transition-duration:
                0.01ms !important;
        }
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

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # SQLMIND BRANDING
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="sidebar-brand-symbol">◈</span> SQLMIND
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
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

                st.caption(
                    f"• {column}"
                )


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

            st.markdown(
                """
                <div class="online-status">
                    <span class="online-dot"></span>
                    FastAPI Connected
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.error(
                "FastAPI unavailable"
            )

    except requests.exceptions.RequestException:

        st.error(
            "● FastAPI Offline"
        )


    # --------------------------------------------------------
    # SIDEBAR TECH STACK
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            color:#a1a1aa;
            font-size:0.85rem;
            margin-top:1.5rem;
            line-height:1.9;
            letter-spacing:0.01em;
        ">
            Backend · FastAPI<br>
            Database · SQLite<br>
            AI Engine · Qwen 2.5 3B · Ollama
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


# ------------------------------------------------------------
# HERO LEFT
# ------------------------------------------------------------

with top_left:

    # --------------------------------------------------------
    # AI DATA COPILOT
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="brand">
            ◈ AI DATA COPILOT
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ANIMATED HERO TITLE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hero-title">
            <span class="typewriter">
                Talk to your database.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # HERO SUBTITLE
    # --------------------------------------------------------

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


# ------------------------------------------------------------
# AI ENGINE CARD
# ------------------------------------------------------------

with top_right:

    st.markdown(
        '<div class="ai-engine-title">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### ⚡ AI Engine"
    )

    st.markdown(
        """
        <div class="online-status">
            <span class="online-dot"></span>
            System Online
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "Your natural-language queries are processed through "
        "the SQL validation pipeline."
    )

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:

        st.metric(
            "AI",
            "Qwen 2.5 3B"
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

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# AI PROCESSING PIPELINE
# ============================================================

st.markdown(
    '<div class="pipeline-title">',
    unsafe_allow_html=True
)

st.markdown(
    "##### AI PROCESSING PIPELINE"
)

pipeline_cols = st.columns(
    [
        1.3,
        0.25,
        1.3,
        0.25,
        1.3,
        0.25,
        1.3,
        0.25,
        1.3
    ]
)

pipeline_items = [
    ("💬", "Question"),
    ("✦", "Qwen 2.5 3B"),
    ("⚙", "SQL"),
    ("✓", "Validation"),
    ("🗄️", "SQLite")
]

for i, (icon, label) in enumerate(
    pipeline_items
):

    with pipeline_cols[i * 2]:

        st.markdown(
            f"""
            <div class="pipeline-node">
                {icon} {label}
            </div>
            """,
            unsafe_allow_html=True
        )

    if i < len(pipeline_items) - 1:

        with pipeline_cols[i * 2 + 1]:

            st.markdown(
                """
                <div class="pipeline-arrow">
                    →
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# QUERY INPUT
# ============================================================

st.markdown(
    """
    <div style="
        font-size:2.5rem;
        font-weight:900;
        letter-spacing:-0.03em;
        line-height:1.1;
        margin-top:0.3rem;
        margin-bottom:0.2rem;
        color:#ffffff;
    ">
        ◈ SQLMIND
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-label" style="margin-top:0;">'
    'Ask your database'
    '</div>',
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

st.caption(
    "QUICK START"
)

example_cols = st.columns(4)

examples = [
    "Show me all customers",
    "Customers from Mumbai",
    "Show the top customers by spending",
    "How many employees are there?"
]

for i, example in enumerate(
    examples
):

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
            color:#a1a1aa;
            font-size:0.85rem;
            padding-top:0.65rem;
            line-height:1.5;
        ">
            Press <b style="color:#d4d4d8;">Generate</b>
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

        with st.spinner(
            "AI is thinking..."
        ):

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

    status = data.get(
        "status"
    )

    intent = data.get(
        "intent"
    )

    corrected_question = data.get(
        "corrected_question"
    )

    sql = data.get(
        "sql"
    )

    results = data.get(
        "results"
    )

    message = data.get(
        "message"
    )

    clarification = data.get(
        "clarification_question"
    )


    # --------------------------------------------------------
    # CORRECTED QUESTION
    # --------------------------------------------------------

    if (
        corrected_question
        and corrected_question.strip()
        != data.get(
            "question",
            ""
        ).strip()
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

            st.success(
                message
            )

        elif status in [
            "validation_failed",
            "semantic_validation_failed",
            "execution_failed",
            "unsafe_operation"
        ]:

            st.error(
                message
            )

        else:

            st.info(
                message
            )


    # --------------------------------------------------------
    # QUERY RESULTS
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

            df = pd.DataFrame(
                results
            )

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
        FastAPI + Qwen 2.5 3B + SQLite
    </div>
    """,
    unsafe_allow_html=True
)