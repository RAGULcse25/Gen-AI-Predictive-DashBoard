import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS to transform the Streamlit app into a premium, Power BI-style dark dashboard.
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0B0F19 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #F8FAFC !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #06090F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    div.stBlock {
        background-color: rgba(21, 28, 44, 0.6);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    
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
    
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_sidebar(logo_url=None, logo_title="AI Dashboard"):
    """
    Renders a side navigation menu.
    """
    with st.sidebar:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px; padding: 10px 0;">
            <div style="background-color: #00C04F; color: white; padding: 8px 12px; border-radius: 8px; font-weight: 700; font-size: 20px;">
                AI
            </div>
            <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: white;">Predictive Analytics</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color: #64748B; font-weight: 600; font-size: 12px; text-transform: uppercase; margin-bottom: 10px;'>Main Menu</p>", unsafe_allow_html=True)
        
        menu_items = [
            ("Overview", True),
            ("Data Exploration", False),
            ("Predictive ML", False),
            ("AI Insights", False),
            ("Settings", False)
        ]
        
        for name, active in menu_items:
            style = "background-color: rgba(0, 192, 79, 0.15); border-left: 4px solid #00C04F; color: white;" if active else "color: #94A3B8;"
            st.markdown(f"""
            <div style="padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; font-weight: 600; font-size: 15px; cursor: pointer; {style}">
                {name}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05)'><br>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #64748B; font-weight: 600; font-size: 12px; text-transform: uppercase; margin-bottom: 10px;'>API Configuration</p>", unsafe_allow_html=True)
        
        api_key = st.text_input("Gemini API Key", type="password", help="Enter your Gemini API key to enable GenAI Insights.")
        
        return api_key


def render_kpi_row(kpis):
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


def render_insight_card(title, desc, rec):
    """
    Renders a premium neon-green styled AI insight card.
    """
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">
            <span>Info</span> {title}
        </div>
        <div class="insight-desc">
            {desc}
        </div>
        <div class="insight-rec">
            <strong>Recommendation:</strong> {rec}
        </div>
    </div>
    """, unsafe_allow_html=True)
