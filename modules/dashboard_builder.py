import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS to transform the Streamlit app into a premium, Power BI-style dark dashboard.
    """
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Main body styling */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0B0F19 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #F8FAFC !important;
    }
    
    /* Header/Sidebar background styling */
    [data-testid="stSidebar"] {
        background-color: #06090F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Card containers styling */
    div.stBlock {
        background-color: rgba(21, 28, 44, 0.6);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    
    /* KPI Card styling */
    .kpi-card-custom {
        background: linear-gradient(135deg, #151C2C 0%, #0E131F 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .kpi-card-custom:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.15);
    }
    .kpi-content {
        display: flex;
        flex-direction: column;
    }
    .kpi-val {
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 4px;
    }
    .kpi-lbl {
        font-size: 13px;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.75px;
    }
    .kpi-ico {
        font-size: 34px;
        padding: 10px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Green Insight Card styling */
    .insight-card {
        background: linear-gradient(135deg, rgba(0, 192, 79, 0.08) 0%, rgba(0, 192, 79, 0.02) 100%);
        border: 1px solid rgba(0, 192, 79, 0.25);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
    }
    .insight-title {
        color: #00C04F;
        font-size: 18px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .insight-desc {
        color: #E2E8F0;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    .insight-rec {
        color: #94A3B8;
        font-size: 13px;
        font-style: italic;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 8px;
    }
    
    /* Title styling */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* Hide Default Streamlit Menu/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_sidebar(logo_url: str = None, logo_title: str = "AI Dashboard"):
    """
    Renders a side navigation menu with functional buttons.
    """
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px; padding: 10px 0;">
            <div style="background-color: #00C04F; color: white; padding: 8px 12px; border-radius: 8px; font-weight: 700; font-size: 20px;">
                AI
            </div>
            <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: white;">Predictive Analytics</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color: #64748B; font-weight: 600; font-size: 12px; margin-bottom: 10px;'>MAIN MENU</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 0.1])
        with col1:
            if st.button("Overview", use_container_width=True, key="btn_overview"):
                st.session_state.page = "overview"
            if st.button("Data Exploration", use_container_width=True, key="btn_explore"):
                st.session_state.page = "explore"
            if st.button("Predictive ML", use_container_width=True, key="btn_ml"):
                st.session_state.page = "ml"
            if st.button("AI Insights", use_container_width=True, key="btn_insights"):
                st.session_state.page = "insights"
            if st.button("Settings", use_container_width=True, key="btn_settings"):
                st.session_state.page = "settings"
        
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05)'><br>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #64748B; font-weight: 600; font-size: 12px;'>API CONFIGURATION</p>", unsafe_allow_html=True)
        
        api_key = st.text_input("Gemini API Key", type="password", help="Enter your Gemini API key to enable GenAI Insights.")
        
        return api_key

def render_kpi_row(kpis: list):
    """
    Renders a row of KPI cards using Streamlit columns.
    """
    cols = st.columns(len(kpis))
    for i, kpi in enumerate(kpis):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card-custom">
                <div class="kpi-content">
                    <span class="kpi-lbl">{kpi['label']}</span>
                    <span class="kpi-val" style="color: {kpi['color']}">{kpi['value']}</span>
                </div>
                <div class="kpi-ico" style="background-color: {kpi['color']}15; color: {kpi['color']}">
                    {kpi['icon']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_insight_card(title: str, desc: str, rec: str):
    """
    Renders a premium neon-green styled AI insight card.
    """
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">
            <span>💡</span> {title}
        </div>
        <div class="insight-desc">
            {desc}
        </div>
        <div class="insight-rec">
            <strong>Recommendation:</strong> {rec}
        </div>
    </div>
    """, unsafe_allow_html=True)
