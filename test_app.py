import streamlit as st

st.write("Testing module imports...")

try:
    from modules.data_loader import load_dataset
    st.write("✓ data_loader imported successfully")
except Exception as e:
    st.error(f"✗ data_loader: {e}")

try:
    from modules.data_cleaner import clean_data_for_viz
    st.write("✓ data_cleaner imported successfully")
except Exception as e:
    st.error(f"✗ data_cleaner: {e}")

try:
    from modules.eda_engine import get_kpis
    st.write("✓ eda_engine imported successfully")
except Exception as e:
    st.error(f"✗ eda_engine: {e}")

try:
    from modules.ml_engine import run_automl_prediction_loop
    st.write("✓ ml_engine imported successfully")
except Exception as e:
    st.error(f"✗ ml_engine: {e}")

try:
    from modules.genai_insights import get_genai_insights
    st.write("✓ genai_insights imported successfully")
except Exception as e:
    st.error(f"✗ genai_insights: {e}")

try:
    from modules.dashboard_builder import apply_custom_css
    st.write("✓ dashboard_builder imported successfully")
except Exception as e:
    st.error(f"✗ dashboard_builder: {e}")

st.write("All imports tested!")
