import streamlit as st

# ============================================================
# FOODGUARD AI DESIGN SYSTEM & BRAND TOKENS
# ============================================================

GREEN = "#159A72"
GREEN_DARK = "#0E7657"
GREEN_LIGHT = "#22B588"
GREEN_SOFT = "#DDF3E8"
GREEN_MINT = "#EBF8F2"
BG = "#F4F8F4"
TEXT = "#173B32"
MUTED = "#657770"
BORDER = "#DCEBE3"
CARD_BG = "#FFFFFF"


def inject_css():
    """
    Injects FoodGuard AI's unified design system CSS.
    NOTE: Using a plain triple-quoted string (NOT an f-string) to prevent
    CSS variables such as --fg-bg: #F4F8F4; from being evaluated as Python expressions.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

        /* ============================================================
           1. ROOT DESIGN TOKENS
           ============================================================ */
        :root {
            --fg-primary: #159A72;
            --fg-dark: #0E7657;
            --fg-light: #22B588;
            --fg-soft: #DDF3E8;
            --fg-mint: #EBF8F2;
            --fg-bg: #F4F8F4;
            --fg-text: #173B32;
            --fg-muted: #657770;
            --fg-border: #DCEBE3;
            --fg-border-light: #EBF3EF;
            --fg-card-bg: #FFFFFF;
            --fg-radius-sm: 8px;
            --fg-radius-md: 14px;
            --fg-radius-lg: 18px;
            --fg-radius-pill: 9999px;
            --fg-shadow-sm: 0 2px 8px rgba(21, 154, 114, 0.05);
            --fg-shadow: 0 4px 18px -2px rgba(21, 154, 114, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.03);
            --fg-shadow-hover: 0 8px 26px -4px rgba(21, 154, 114, 0.14), 0 3px 8px -2px rgba(0, 0, 0, 0.04);
            --font-display: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* ============================================================
           2. GLOBAL RESETS & BACKGROUND
           ============================================================ */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: var(--font-body) !important;
            color: #173B32 !important;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden !important;
        }

        /* Subtle organic botanical and nutrition background */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main {
            background-color: #F4F8F4 !important;
            background-image:
                radial-gradient(circle at 10% 15%, rgba(221, 243, 232, 0.65) 0%, transparent 45%),
                radial-gradient(circle at 90% 85%, rgba(221, 243, 232, 0.55) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(244, 248, 244, 0.8) 0%, transparent 100%),
                url("data:image/svg+xml,%3Csvg width='90' height='90' viewBox='0 0 90 90' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23159A72' fill-opacity='0.035' fill-rule='evenodd'%3E%3Cpath d='M45 10c-6 0-11 5-11 11 0 8 11 15 11 15s11-7 11-15c0-6-5-11-11-11zm0 18c-2-2-6-6-6-8 0-3 3-6 6-6s6 3 6 6c0 2-4 6-6 8zM12 55c-5 0-9 4-9 9 0 6 9 12 9 12s9-6 9-12c0-5-4-9-9-9zm0 15c-2-2-5-5-5-6 0-2 2-4 5-4s5 2 5 4c0 1-3 4-5 6zM78 55c-5 0-9 4-9 9 0 6 9 12 9 12s9-6 9-12c0-5-4-9-9-9zm0 15c-2-2-5-5-5-6 0-2 2-4 5-4s5 2 5 4c0 1-3 4-5 6zM45 68c-3 0-6 2-6 5 0 4 6 8 6 8s6-4 6-8c0-3-3-5-6-5z'/%3E%3Ccircle cx='22' cy='22' r='1.5'/%3E%3Ccircle cx='68' cy='22' r='1.5'/%3E%3Ccircle cx='22' cy='68' r='1.5'/%3E%3Ccircle cx='68' cy='68' r='1.5'/%3E%3C/g%3E%3C/svg%3E") !important;
            background-attachment: fixed !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
            height: 2rem !important;
        }

        #MainMenu, footer {
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .block-container,
        [data-testid="stMainBlockContainer"],
        div.block-container {
            max-width: 820px !important;
            padding: 0.8rem 1.25rem 4rem !important;
            margin: 0 auto !important;
        }

        /* ============================================================
           3. TYPOGRAPHY & TEXT CONTRAST (PREVENTS WHITE-ON-LIGHT)
           ============================================================ */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-display) !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        p, li, span, small, label, td, th {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stMarkdownContainer"] li,
        .stApp [data-testid="stMarkdownContainer"] span {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            line-height: 1.6;
        }

        .stApp [data-testid="stCaptionContainer"],
        .stApp [data-testid="stCaptionContainer"] *,
        .stCaption,
        .muted {
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            font-size: 0.84rem !important;
        }

        /* Section Headings */
        .section-heading {
            font-family: var(--font-display);
            font-size: 1.45rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            margin-top: 0.4rem;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }

        .section-description {
            font-size: 0.88rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            margin-bottom: 1.2rem;
            line-height: 1.5;
        }

        .section-title {
            font-family: var(--font-display);
            font-size: 1.15rem;
            font-weight: 700;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            margin: 1.3rem 0 0.75rem 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* ============================================================
           4. TOP HEADER BAR
           ============================================================ */
        .fg-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: var(--fg-radius-lg);
            padding: 0.85rem 1.25rem;
            margin-bottom: 1.25rem;
            box-shadow: var(--fg-shadow);
        }

        .fg-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .fg-logo {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(21, 154, 114, 0.24);
            flex-shrink: 0;
        }

        .fg-logo svg {
            stroke: #FFFFFF !important;
        }

        .fg-brand-info {
            display: flex;
            flex-direction: column;
        }

        .fg-brand-name {
            font-family: var(--font-display);
            font-size: 1.3rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }

        .fg-brand-badge {
            display: inline-block;
            background: #DDF3E8;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            font-size: 0.72rem;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
            margin-left: 4px;
            vertical-align: middle;
            border: 1px solid #BFE3D3;
        }

        .fg-brand-sub {
            font-size: 0.78rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            font-weight: 500;
            margin-top: 2px;
        }

        .fg-header-right {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .fg-live-badge {
            background: #EBF8F2;
            border: 1px solid #BFE3D3;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            font-size: 0.74rem;
            font-weight: 700;
            border-radius: var(--fg-radius-pill);
            padding: 5px 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .fg-pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #159A72;
            box-shadow: 0 0 0 2px rgba(21, 154, 114, 0.25);
            display: inline-block;
        }

        .fg-profile-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #DDF3E8;
            color: #0E7657 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1.5px solid #BFE3D3;
        }

        .fg-profile-avatar svg {
            stroke: #0E7657 !important;
        }

        /* ============================================================
           5. NAVIGATION / STREAMLIT TABS
           ============================================================ */
        div[data-testid="stTabs"] {
            margin-top: 0.2rem;
            margin-bottom: 1.5rem;
        }

        div[data-testid="stTabs"] [role="tablist"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: 16px !important;
            padding: 5px !important;
            gap: 6px !important;
            box-shadow: var(--fg-shadow-sm) !important;
            overflow-x: auto !important;
            scrollbar-width: none !important;
            display: flex !important;
        }

        div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
            display: none !important;
        }

        div[data-testid="stTabs"] button[role="tab"] {
            border-radius: 12px !important;
            padding: 8px 14px !important;
            font-family: var(--font-body) !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            white-space: nowrap !important;
            margin: 0 !important;
        }

        div[data-testid="stTabs"] button[role="tab"]:hover {
            background: #DDF3E8 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
        }

        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(21, 154, 114, 0.28) !important;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
        div[data-testid="stTabs"] [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ============================================================
           6. CARD COMPONENTS & CONTAINERS
           ============================================================ */
        .fg-card {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: var(--fg-radius-md) !important;
            padding: 1.25rem !important;
            margin-bottom: 1rem !important;
            box-shadow: var(--fg-shadow) !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .fg-card:hover {
            box-shadow: var(--fg-shadow-hover) !important;
        }

        .fg-card * {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .fg-card .muted,
        .fg-card small {
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
        }

        /* ============================================================
           7. SCAN FOOD PAGE COMPONENTS
           ============================================================ */
        .scan-hero {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5FBF8 100%);
            border: 1px solid #DCEBE3;
            border-radius: var(--fg-radius-md);
            padding: 1.15rem 1.35rem;
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 1.25rem;
            box-shadow: var(--fg-shadow-sm);
        }

        .scan-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: #DDF3E8;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.35rem;
            font-weight: bold;
            flex-shrink: 0;
            border: 1px solid #BFE3D3;
        }

        .scan-hero-title {
            font-family: var(--font-display);
            font-size: 1.15rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .scan-hero-text {
            font-size: 0.84rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            margin-top: 3px;
        }

        .preview-label {
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            margin-bottom: 6px;
        }

        .scan-loading {
            background: #FFFFFF;
            border: 1.5px solid #159A72;
            border-radius: var(--fg-radius-md);
            padding: 1.2rem;
            display: flex;
            align-items: center;
            gap: 14px;
            box-shadow: var(--fg-shadow);
            margin: 1rem 0;
        }

        .magnifier {
            font-size: 1.8rem;
            animation: spin 1.8s infinite linear;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            50% { transform: rotate(45deg); }
            100% { transform: rotate(0deg); }
        }

        .food-result-card {
            background: #FFFFFF;
            border: 1.5px solid #BFE3D3;
            border-radius: var(--fg-radius-lg);
            padding: 1.35rem 1.4rem;
            margin: 1.2rem 0;
            box-shadow: var(--fg-shadow);
        }

        .food-result-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
        }

        .food-result-icon {
            font-size: 2.2rem;
            background: #EBF8F2;
            width: 54px;
            height: 54px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #DCEBE3;
            flex-shrink: 0;
        }

        .eyebrow {
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.8px;
            color: #159A72 !important;
            -webkit-text-fill-color: #159A72 !important;
            text-transform: uppercase;
        }

        .food-result-name {
            font-family: var(--font-display);
            font-size: 1.6rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            margin-top: 2px;
            line-height: 1.2;
        }

        .confidence-pill {
            font-size: 0.82rem;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: var(--fg-radius-pill);
            white-space: nowrap;
        }

        .confidence-good {
            background: #DDF3E8;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            border: 1px solid #BFE3D3;
        }

        .confidence-low {
            background: #FEF3C7;
            color: #92400E !important;
            -webkit-text-fill-color: #92400E !important;
            border: 1px solid #FDE68A;
        }

        .portion-title {
            font-family: var(--font-display);
            font-size: 1.05rem;
            font-weight: 700;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            margin: 1.2rem 0 0.5rem 0;
        }

        .portion-summary {
            background: #F4FAF7;
            border: 1px solid #DCEBE3;
            border-radius: 12px;
            padding: 12px 16px;
            margin: 12px 0;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }

        .portion-summary span {
            font-size: 0.78rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        .portion-summary strong {
            font-family: var(--font-display);
            font-size: 1.35rem;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .nutrition-card {
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: var(--fg-radius-md);
            padding: 1rem 1.15rem;
            display: flex;
            flex-direction: column;
            gap: 4px;
            box-shadow: var(--fg-shadow-sm);
            margin-bottom: 0.75rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .nutrition-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--fg-shadow);
        }

        .nutrition-icon {
            font-size: 1.4rem;
            margin-bottom: 2px;
        }

        .nutrition-label {
            font-size: 0.76rem;
            font-weight: 700;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .nutrition-value {
            font-family: var(--font-display);
            font-size: 1.35rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .food-advice {
            background: #EBF8F2;
            border: 1px solid #BFE3D3;
            border-radius: var(--fg-radius-md);
            padding: 1.1rem 1.25rem;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin: 1.1rem 0;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .advice-icon {
            font-size: 1.35rem;
            flex-shrink: 0;
            margin-top: 1px;
        }

        /* ============================================================
           8. PACKAGED FOOD PAGE COMPONENTS
           ============================================================ */
        .package-title {
            font-family: var(--font-display);
            font-size: 1.45rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }

        .package-subtitle {
            font-size: 0.88rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            margin-bottom: 1.25rem;
            line-height: 1.5;
        }

        .product-name-card {
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%);
            border-radius: var(--fg-radius-md);
            padding: 1.25rem 1.4rem;
            margin: 1.2rem 0;
            box-shadow: 0 6px 22px rgba(14, 118, 87, 0.25);
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        .product-name-label {
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 1px;
            color: #DDF3E8 !important;
            -webkit-text-fill-color: #DDF3E8 !important;
            text-transform: uppercase;
        }

        .product-name {
            font-family: var(--font-display);
            font-size: 1.65rem;
            font-weight: 800;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            margin-top: 4px;
            line-height: 1.2;
        }

        .package-info-card {
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: var(--fg-radius-md);
            padding: 1.15rem;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            line-height: 1.6;
            font-size: 0.9rem;
            box-shadow: var(--fg-shadow-sm);
        }

        .package-empty {
            background: #FFFFFF;
            border: 2px dashed #BFE3D3;
            border-radius: var(--fg-radius-lg);
            padding: 2.2rem 1.5rem;
            text-align: center;
            color: #173B32 !important;
            margin: 1.2rem 0;
            box-shadow: var(--fg-shadow-sm);
        }

        .package-empty-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .package-ready {
            background: #DDF3E8;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            border: 1px solid #BFE3D3;
            border-radius: 10px;
            padding: 8px 16px;
            font-weight: 700;
            font-size: 0.85rem;
            margin: 12px 0;
            display: inline-block;
        }

        .scan-status {
            background: #EBF8F2;
            border: 1px solid #BFE3D3;
            border-radius: 12px;
            padding: 11px 16px;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            font-weight: 600;
            font-size: 0.88rem;
            margin: 10px 0;
        }

        .scan-complete {
            background: #DDF3E8 !important;
            font-weight: 700 !important;
        }

        /* ============================================================
           9. STREAMLIT FORM CONTROLS & INPUTS (PERFECT CONTRAST)
           ============================================================ */
        /* Text input, Number input, Text area */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea {
            background: #FFFFFF !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            border: 1.5px solid #DCEBE3 !important;
            border-radius: 12px !important;
            padding: 0.65rem 0.95rem !important;
            font-family: var(--font-body) !important;
            font-size: 0.95rem !important;
            box-shadow: none !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: #159A72 !important;
            box-shadow: 0 0 0 3px rgba(21, 154, 114, 0.16) !important;
            outline: none !important;
        }

        /* Input Labels */
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            margin-bottom: 0.35rem !important;
        }

        /* Stepper buttons */
        [data-testid="stNumberInput"] button {
            background: #FFFFFF !important;
            border-color: #DCEBE3 !important;
            color: #159A72 !important;
            -webkit-text-fill-color: #159A72 !important;
        }

        [data-testid="stNumberInput"] button:hover {
            background: #EBF8F2 !important;
            color: #0E7657 !important;
        }

        /* Selectboxes */
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            border: 1.5px solid #DCEBE3 !important;
            border-radius: 12px !important;
            padding: 0.25rem 0.5rem !important;
            font-family: var(--font-body) !important;
        }

        [data-testid="stSelectbox"] [data-baseweb="select"] svg {
            fill: #159A72 !important;
        }

        body [data-baseweb="popover"],
        body [data-baseweb="menu"],
        body [role="listbox"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: 12px !important;
            box-shadow: var(--fg-shadow-hover) !important;
        }

        body [role="option"] {
            background: #FFFFFF !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-family: var(--font-body) !important;
            padding: 10px 14px !important;
        }

        body [role="option"]:hover {
            background: #EBF8F2 !important;
            color: #0E7657 !important;
        }

        body [role="option"][aria-selected="true"] {
            background: #DDF3E8 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            font-weight: 700 !important;
        }

        /* Radio Buttons */
        [data-testid="stRadio"] [role="radiogroup"] {
            gap: 12px !important;
        }

        [data-testid="stRadio"] label {
            background: #FFFFFF !important;
            border: 1.5px solid #DCEBE3 !important;
            border-radius: 12px !important;
            padding: 8px 16px !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 600 !important;
            box-shadow: var(--fg-shadow-sm) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stRadio"] label:hover {
            border-color: #159A72 !important;
            background: #F4FAF7 !important;
        }

        /* Date Input */
        [data-testid="stDateInput"] input {
            background: #FFFFFF !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            border: 1.5px solid #DCEBE3 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }

        [data-testid="stDateInput"] button svg {
            fill: #159A72 !important;
        }

        body [data-baseweb="calendar"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: 14px !important;
            box-shadow: var(--fg-shadow-hover) !important;
        }

        /* ============================================================
           10. BUTTONS (PRIMARY & SECONDARY)
           ============================================================ */
        .stButton > button,
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-secondary"] {
            font-family: var(--font-body) !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            padding: 0.65rem 1.35rem !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            letter-spacing: 0.01em !important;
        }

        /* Primary Button: Vibrant FoodGuard Green Gradient */
        .stButton > button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        .stButton > button[kind="primary"]:focus {
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(21, 154, 114, 0.28) !important;
        }

        .stButton > button[kind="primary"] *,
        button[data-testid="stBaseButton-primary"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        .stButton > button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover {
            transform: translateY(-1.5px) !important;
            box-shadow: 0 6px 20px rgba(21, 154, 114, 0.36) !important;
        }

        /* Secondary Button */
        .stButton > button[kind="secondary"],
        button[data-testid="stBaseButton-secondary"] {
            background: #FFFFFF !important;
            color: #159A72 !important;
            -webkit-text-fill-color: #159A72 !important;
            border: 1.5px solid #DCEBE3 !important;
            box-shadow: var(--fg-shadow-sm) !important;
        }

        .stButton > button[kind="secondary"]:hover,
        button[data-testid="stBaseButton-secondary"]:hover {
            background: #F4FAF7 !important;
            border-color: #159A72 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
        }

        /* Link Buttons (YouTube guided workouts) */
        a[data-testid="stLinkButton"] {
            background: #FFFFFF !important;
            color: #159A72 !important;
            -webkit-text-fill-color: #159A72 !important;
            border: 1.5px solid #BFE3D3 !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            box-shadow: var(--fg-shadow-sm) !important;
            transition: all 0.2s ease !important;
        }

        a[data-testid="stLinkButton"]:hover {
            background: #EBF8F2 !important;
            border-color: #159A72 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
        }

        /* ============================================================
           11. FILE UPLOADER & CAMERA INPUT
           ============================================================ */
        [data-testid="stFileUploader"] {
            background: #FFFFFF !important;
            border: 2px dashed #BFE3D3 !important;
            border-radius: var(--fg-radius-lg) !important;
            padding: 16px !important;
            box-shadow: var(--fg-shadow-sm) !important;
            transition: border-color 0.2s ease !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #159A72 !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: #F8FCFA !important;
            border: 1px dashed #DCEBE3 !important;
            border-radius: var(--fg-radius-md) !important;
            padding: 24px !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 600 !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] small {
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background: #159A72 !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }

        [data-testid="stFileUploaderDropzone"] button * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* Uploaded file chip */
        [data-testid="stFileUploaderFile"] {
            background: #EBF8F2 !important;
            border: 1px solid #BFE3D3 !important;
            border-radius: 12px !important;
            padding: 8px 14px !important;
            margin-top: 10px !important;
        }

        [data-testid="stFileUploaderFile"] span,
        [data-testid="stFileUploaderFile"] small,
        [data-testid="stFileUploaderFile"] p {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 600 !important;
        }

        [data-testid="stCameraInput"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: var(--fg-radius-lg) !important;
            padding: 14px !important;
            box-shadow: var(--fg-shadow-sm) !important;
        }

        [data-testid="stCameraInput"] button {
            background: linear-gradient(135deg, #159A72, #0E7657) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* ============================================================
           12. METRICS & KPI CARDS (DAILY DIARY & HEALTH SNAPSHOT)
           ============================================================ */
        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: var(--fg-radius-md) !important;
            padding: 1rem 1.15rem !important;
            box-shadow: var(--fg-shadow-sm) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--fg-shadow) !important;
        }

        [data-testid="stMetricLabel"] * {
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        [data-testid="stMetricValue"] * {
            font-family: var(--font-display) !important;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-size: 1.45rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
        }

        /* ============================================================
           13. DATA TABLES & DATAFRAMES (READABLE & DISTINCT)
           ============================================================ */
        [data-testid="stDataFrame"],
        .stDataFrame,
        div[data-testid="stTable"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: var(--fg-radius-md) !important;
            overflow: hidden !important;
            box-shadow: var(--fg-shadow-sm) !important;
            margin: 1rem 0 !important;
        }

        table {
            width: 100% !important;
            border-collapse: collapse !important;
            font-family: var(--font-body) !important;
        }

        th {
            background: #DDF3E8 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            font-weight: 700 !important;
            font-size: 0.85rem !important;
            text-align: left !important;
            padding: 11px 16px !important;
            border-bottom: 1.5px solid #BFE3D3 !important;
            letter-spacing: 0.02em !important;
        }

        td {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            padding: 10px 16px !important;
            font-size: 0.9rem !important;
            border-bottom: 1px solid #EDF4F0 !important;
        }

        tr:nth-child(even) td {
            background: #F8FCFA !important;
        }

        tr:hover td {
            background: #EBF8F2 !important;
        }

        /* Streamlit Canvas / Glide-data-grid */
        [data-testid="stDataFrame"] canvas {
            border-radius: var(--fg-radius-md) !important;
        }

        /* ============================================================
           14. ALERTS / CALLOUTS (STATUS BANNERS)
           ============================================================ */
        .stAlert {
            border-radius: var(--fg-radius-md) !important;
            padding: 12px 18px !important;
            font-family: var(--font-body) !important;
            font-size: 0.9rem !important;
            line-height: 1.55 !important;
            border-width: 1px !important;
            box-shadow: var(--fg-shadow-sm) !important;
        }

        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
            font-weight: 500 !important;
        }

        /* Success */
        div[data-baseweb="notification"][kind="positive"],
        div[data-testid="stNotification"][kind="success"] {
            background: #DDF3E8 !important;
            border-color: #159A72 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
        }

        /* Info */
        div[data-baseweb="notification"][kind="info"],
        div[data-testid="stNotification"][kind="info"] {
            background: #EBF8F2 !important;
            border-color: #BFE3D3 !important;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
        }

        /* Warning */
        div[data-baseweb="notification"][kind="warning"],
        div[data-testid="stNotification"][kind="warning"] {
            background: #FFFBEB !important;
            border-color: #FDE68A !important;
            color: #92400E !important;
            -webkit-text-fill-color: #92400E !important;
        }

        /* Error */
        div[data-baseweb="notification"][kind="negative"],
        div[data-testid="stNotification"][kind="error"] {
            background: #FEF2F2 !important;
            border-color: #FECACA !important;
            color: #991B1B !important;
            -webkit-text-fill-color: #991B1B !important;
        }

        /* Progress Bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #159A72 0%, #22B588 100%) !important;
            border-radius: var(--fg-radius-pill) !important;
        }

        .stProgress > div > div > div {
            background: #DDF3E8 !important;
            border-radius: var(--fg-radius-pill) !important;
            height: 8px !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #DCEBE3 !important;
            border-radius: var(--fg-radius-md) !important;
            box-shadow: var(--fg-shadow-sm) !important;
            overflow: hidden !important;
            margin: 0.8rem 0 !important;
        }

        [data-testid="stExpander"] summary {
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            padding: 12px 16px !important;
        }

        [data-testid="stExpander"] summary:hover {
            color: #159A72 !important;
            -webkit-text-fill-color: #159A72 !important;
        }

        /* ============================================================
           15. PRESERVED UI HELPER ELEMENTS (WELCOME, CALORIES, MEAL)
           ============================================================ */
        .fg-welcome {
            background: linear-gradient(135deg, #159A72 0%, #0E7657 100%);
            border-radius: var(--fg-radius-lg);
            padding: 1.6rem 1.8rem;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            margin-bottom: 1.4rem;
            box-shadow: 0 8px 24px rgba(14, 118, 87, 0.22);
        }

        .fg-welcome h1 {
            font-size: 1.55rem;
            font-weight: 800;
            margin: 0 0 6px 0;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        .fg-welcome p {
            font-size: 0.9rem;
            color: #DDF3E8 !important;
            -webkit-text-fill-color: #DDF3E8 !important;
            margin: 0;
            line-height: 1.5;
        }

        .fg-calorie {
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: var(--fg-radius-md);
            padding: 1.25rem;
            box-shadow: var(--fg-shadow);
            margin-bottom: 1rem;
        }

        .fg-calorie-label {
            font-size: 0.76rem;
            font-weight: 800;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            letter-spacing: 0.8px;
        }

        .fg-calorie-number {
            font-family: var(--font-display);
            font-size: 2rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            margin: 4px 0;
        }

        .fg-calorie-number .fg-unit {
            font-size: 1rem;
            font-weight: 600;
            color: #657770 !important;
        }

        .fg-calorie-goal {
            font-size: 0.84rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            margin-bottom: 8px;
        }

        .fg-progress {
            background: #DDF3E8;
            border-radius: 10px;
            height: 9px;
            overflow: hidden;
            margin: 10px 0 14px 0;
        }

        .fg-progress span {
            display: block;
            height: 100%;
            background: linear-gradient(90deg, #159A72 0%, #22B588 100%);
            border-radius: 10px;
        }

        .fg-mini {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            text-align: center;
            border-top: 1px solid #EDF4F0;
            padding-top: 10px;
        }

        .fg-mini b {
            font-size: 1.05rem;
            font-weight: 800;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
            display: block;
        }

        .fg-mini span {
            font-size: 0.74rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            text-transform: uppercase;
        }

        .fg-action {
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: var(--fg-radius-md);
            padding: 1.1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: var(--fg-shadow-sm);
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }

        .fg-action:hover {
            border-color: #159A72;
            transform: translateY(-2px);
            box-shadow: var(--fg-shadow);
        }

        .fg-action-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: #DDF3E8;
            color: #0E7657 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .fg-action-title {
            font-weight: 700;
            font-size: 0.95rem;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .fg-action-sub {
            font-size: 0.78rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
        }

        .fg-meal {
            background: #FFFFFF;
            border: 1px solid #DCEBE3;
            border-radius: 12px;
            padding: 0.85rem 1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.6rem;
            box-shadow: var(--fg-shadow-sm);
        }

        .fg-meal-icon {
            color: #159A72 !important;
        }

        .fg-meal-main {
            flex: 1;
            font-weight: 700;
            font-size: 0.92rem;
            color: #173B32 !important;
            -webkit-text-fill-color: #173B32 !important;
        }

        .fg-meal-time {
            display: block;
            font-size: 0.74rem;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            font-weight: 500;
        }

        .fg-meal-kcal {
            font-family: var(--font-display);
            font-weight: 800;
            color: #0E7657 !important;
            -webkit-text-fill-color: #0E7657 !important;
            font-size: 0.95rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #657770 !important;
            -webkit-text-fill-color: #657770 !important;
            font-size: 0.78rem;
            font-weight: 600;
            margin-top: 2.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid #DCEBE3;
        }

        /* ============================================================
           16. MOBILE RESPONSIVENESS (< 768px & < 520px)
           ============================================================ */
        @media (max-width: 768px) {
            .block-container {
                padding: 0.6rem 0.85rem 3.5rem !important;
            }

            .fg-topbar {
                padding: 0.75rem 1rem;
                border-radius: var(--fg-radius-md);
            }

            .fg-brand-name {
                font-size: 1.15rem;
            }

            .fg-live-badge {
                font-size: 0.7rem;
                padding: 4px 9px;
            }

            div[data-testid="stTabs"] button[role="tab"] {
                font-size: 0.8rem !important;
                padding: 7px 11px !important;
            }

            .section-heading {
                font-size: 1.3rem;
            }

            .food-result-name {
                font-size: 1.35rem;
            }
        }

        @media (max-width: 520px) {
            .block-container {
                padding: 0.5rem 0.65rem 3rem !important;
            }

            .fg-topbar {
                padding: 0.65rem 0.85rem;
            }

            .fg-logo {
                width: 38px;
                height: 38px;
            }

            .fg-brand-name {
                font-size: 1.05rem;
            }

            .fg-brand-sub {
                display: none;
            }

            div[data-testid="stTabs"] [role="tablist"] {
                gap: 4px !important;
                padding: 4px !important;
            }

            div[data-testid="stTabs"] button[role="tab"] {
                font-size: 0.74rem !important;
                padding: 6px 9px !important;
            }

            .food-result-top {
                flex-direction: column;
                align-items: flex-start;
            }

            .confidence-pill {
                align-self: flex-start;
            }

            .product-name {
                font-size: 1.35rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SVG ICONS (INLINE, LIGHTWEIGHT & HIGH-PERFORMANCE)
# ============================================================

def svg_icon(name, size=21):
    icons = {
        "leaf": '<path d="M20 4C11 4 4 8 4 18c10 0 14-6 16-14Z"/><path d="M4 18c4-5 8-7 13-9"/>',
        "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-4 3.2-6 7-6s6.2 2 7 6"/>',
        "camera": '<path d="M4 7h4l1.5-2h5L16 7h4v11H4Z"/><circle cx="12" cy="12.5" r="3.2"/>',
        "edit": '<path d="M4 20h4L19 9l-4-4L4 16v4Z"/><path d="m13.5 6.5 4 4"/>',
        "utensils": '<path d="M7 3v8M4 3v5a3 3 0 0 0 6 0V3M7 11v10M16 3v18M16 3c2 2 3 4 3 6 0 2-1.2 3-3 3"/>',
        "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
        "sparkle": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z"/>',
    }
    path = icons.get(name, icons["leaf"])
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
    )


# ============================================================
# COMPONENT BUILDERS (PRESERVED FUNCTION SIGNATURES)
# ============================================================

def app_header():
    leaf_svg = svg_icon("leaf", 22)
    user_svg = svg_icon("user", 18)
    html = (
        '<div class="fg-topbar">'
        '  <div class="fg-brand">'
        '    <div class="fg-logo">' + leaf_svg + '</div>'
        '    <div class="fg-brand-info">'
        '      <div class="fg-brand-name">FoodGuard <span class="fg-brand-badge">AI</span></div>'
        '      <div class="fg-brand-sub">Smart Food &amp; Nutrition Assistant</div>'
        '    </div>'
        '  </div>'
        '  <div class="fg-header-right">'
        '    <div class="fg-live-badge"><span class="fg-pulse-dot"></span> AI Active</div>'
        '    <div class="fg-profile-avatar">' + user_svg + '</div>'
        '  </div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def welcome():
    html = (
        '<div class="fg-welcome">'
        '<h1>Eat smarter. Feel better. 🌿</h1>'
        '<p>Track your meals with AI-powered food recognition and real-time nutrition intelligence.</p>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section_header(title, description=None):
    html = f'<div class="section-heading">{title}</div>'
    if description:
        html += f'<div class="section-description">{description}</div>'
    st.markdown(html, unsafe_allow_html=True)


def calorie_card():
    st.markdown(
        '<div class="fg-calorie">'
        "<div class=\"fg-calorie-label\">TODAY'S CALORIES</div>"
        '<div class="fg-calorie-number">1,248 <span class="fg-unit">kcal</span></div>'
        '<div class="fg-calorie-goal">Daily Target: 2,000 kcal</div>'
        '<div class="fg-progress"><span style="width: 62.4%;"></span></div>'
        '<div class="fg-mini">'
        '<div><b>48g</b><span>Protein</span></div>'
        '<div><b>142g</b><span>Carbs</span></div>'
        '<div><b>38g</b><span>Fat</span></div>'
        '</div></div>',
        unsafe_allow_html=True
    )


def quick_action(title, subtitle, icon):
    icon_svg = svg_icon(icon, 20)
    st.markdown(
        f'<div class="fg-action">'
        f'<div class="fg-action-icon">{icon_svg}</div>'
        f'<div>'
        f'<div class="fg-action-title">{title}</div>'
        f'<div class="fg-action-sub">{subtitle}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def meal_row(name, time, calories):
    icon_svg = svg_icon("utensils", 18)
    st.markdown(
        f'<div class="fg-meal">'
        f'<div class="fg-meal-icon">{icon_svg}</div>'
        f'<div class="fg-meal-main">{name}'
        f'<span class="fg-meal-time">{time}</span></div>'
        f'<div class="fg-meal-kcal">{calories} kcal</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def card_start():
    st.markdown('<div class="fg-card">', unsafe_allow_html=True)


def card_end():
    st.markdown('</div>', unsafe_allow_html=True)
