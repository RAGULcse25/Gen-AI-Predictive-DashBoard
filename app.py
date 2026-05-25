import streamlit as st
import pandas as pd
import os

# Import modules
from modules.data_loader import load_dataset, inspect_dataset
from modules.data_cleaner import clean_data_for_viz, prepare_data_for_ml
from modules.eda_engine import get_kpis, generate_trend_chart, generate_category_pie, generate_rankings_bar, generate_heatmap
from modules.ml_engine import run_automl_prediction_loop
from modules.genai_insights import get_genai_insights
from modules.dashboard_builder import apply_custom_css, render_sidebar, render_kpi_row, render_insight_card

# Set page config
st.set_page_config(
    page_title="GenAI Predictive Dashboard",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "df" not in st.session_state:
    st.session_state.df = None
if "target_column" not in st.session_state:
    st.session_state.target_column = None
if "ml_results" not in st.session_state:
    st.session_state.ml_results = {}

# Apply custom styling
apply_custom_css()

# Render sidebar and get API key
gemini_api_key = render_sidebar()

# Main title header
st.markdown("""
<div style="margin-bottom: 25px;">
    <h1 style="margin: 0; font-size: 32px; font-weight: 700; color: #F8FAFC;">
        📊 AI-Powered Predictive Analytics Dashboard
    </h1>
    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 16px;">
        Upload any dataset to auto-clean, visualize key metrics, train machine learning models, and generate GenAI business insights.
    </p>
</div>
""", unsafe_allow_html=True)

# PAGE: Dataset Upload & Source Selection
st.markdown("### 📂 1. Dataset Source")
col_upload, col_source = st.columns([2, 1])

uploaded_file = None

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel dataset", 
        type=["csv", "xlsx", "xls"],
        help="Upload raw data to automatically run analytics pipeline."
    )

with col_source:
    st.markdown("<p style='font-size:14px; margin-bottom:10px; font-weight:600; color:#94A3B8;'>Demo Datasets</p>", unsafe_allow_html=True)
    use_demo = st.checkbox("Use Blinkit Grocery Dataset (Local Excel)", value=True if st.session_state.df is None else False)

# Handle file ingestion
if uploaded_file is not None:
    try:
        df = load_dataset(uploaded_file.read(), uploaded_file.name)
        st.session_state.df = df
        st.success(f"Successfully loaded {uploaded_file.name}!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
elif use_demo:
    demo_path = "Tableau BlinkIT Grocery Project U16955293080 (4).xlsx"
    if os.path.exists(demo_path):
        try:
            df = pd.read_excel(demo_path, sheet_name="Tableau BlinkIT Grocery Project")
            st.session_state.df = df
            st.info("Loaded demo dataset: Blinkit Grocery Sales")
        except Exception as e:
            st.error(f"Error loading demo dataset: {e}")
    else:
        st.warning("Blinkit demo file not found in workspace path.")

# Proceed if data is successfully loaded
if st.session_state.df is not None:
    df = st.session_state.df
    
    # 2. Inspect and Auto-understand Target
    metadata = inspect_dataset(df, "dataset")
    
    st.markdown("### 🎯 2. Target Variable Selection")
    col_target_sel, col_meta = st.columns([1, 2])
    
    with col_target_sel:
        target_column = st.selectbox(
            "Select target column for ML predictions",
            options=metadata["all_columns"],
            index=metadata["all_columns"].index(metadata["guessed_target"]) if metadata["guessed_target"] in metadata["all_columns"] else 0,
            help="Select the column you want the AI model to predict.",
            key="target_column_selector"
        )
        st.session_state.target_column = target_column
        
    with col_meta:
        st.markdown(f"""
        <div style="background-color: rgba(255,255,255,0.03); border-radius: 8px; padding: 12px 18px; border: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #94A3B8; font-size: 13px;">Auto-detected Attributes:</span><br>
            <span style="font-weight: 700; color: #00C04F;">{metadata['rows']:,}</span> rows | 
            <span style="font-weight: 700; color: #00C04F;">{metadata['columns_count']}</span> columns | 
            <span style="font-weight: 700; color: #F9BC06;">{len(metadata['numerical_columns'])}</span> numerical | 
            <span style="font-weight: 700; color: #02A0FC;">{len(metadata['categorical_columns'])}</span> categorical
        </div>
        """, unsafe_allow_html=True)

    # 3. Auto-clean and preview
    df_cleaned_viz = clean_data_for_viz(df)
    
    with st.expander("🔍 Preview Cleaned Data (Nulls & Duplicates handled)", expanded=False):
        st.dataframe(df_cleaned_viz.head(10), use_container_width=True)

    # PAGE-BASED CONTENT RENDERING
    if st.session_state.page == "overview":
        # OVERVIEW PAGE - Main Dashboard
        st.markdown("### 🏆 3. Executive KPIs")
        kpis = get_kpis(df_cleaned_viz, target_column)
        render_kpi_row(kpis)

        st.markdown("### 📈 4. Exploratory Data Visualizations")
        col1, col2 = st.columns(2)
        
        with col1:
            donut_fig = generate_category_pie(df_cleaned_viz, target_column)
            if donut_fig:
                st.plotly_chart(donut_fig, use_container_width=True)
            heatmap_fig = generate_heatmap(df_cleaned_viz)
            if heatmap_fig:
                st.plotly_chart(heatmap_fig, use_container_width=True)
                
        with col2:
            trend_fig = generate_trend_chart(df_cleaned_viz, target_column)
            if trend_fig:
                st.plotly_chart(trend_fig, use_container_width=True)
            rankings_fig = generate_rankings_bar(df_cleaned_viz, target_column)
            if rankings_fig:
                st.plotly_chart(rankings_fig, use_container_width=True)

    elif st.session_state.page == "explore":
        # DATA EXPLORATION PAGE
        st.markdown("### 📊 Data Exploration")
        st.info("Data exploration features: statistical analysis, missing values, data distributions")
        
        st.markdown("#### Dataset Summary")
        st.write(df_cleaned_viz.describe())
        
        st.markdown("#### Data Types")
        st.write(df_cleaned_viz.dtypes)
        
        st.markdown("#### Missing Values")
        missing = df_cleaned_viz.isnull().sum()
        st.write(missing[missing > 0] if missing.sum() > 0 else "No missing values found!")

    elif st.session_state.page == "ml":
        # PREDICTIVE ML PAGE
        st.markdown("### 🤖 Automated Machine Learning")
        
        if st.button("Train AutoML Models", key="train_ml"):
            with st.spinner("Training models..."):
                try:
                    X_encoded, y, target_is_cat = prepare_data_for_ml(df, target_column)
                    ml_results = run_automl_prediction_loop(X_encoded, y, target_is_cat)
                    st.session_state.ml_results = ml_results
                    
                    st.success(f"Best Model: {ml_results['best_model']}")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Problem Type", ml_results['problem_type'])
                    col2.metric("Score", f"{ml_results['score']:.4f}")
                    col3.metric("Metric", ml_results['evaluation_metric'])
                    
                    st.markdown("#### Top Features")
                    for feat, imp in ml_results['top_features'][:5]:
                        st.write(f"- **{feat}**: {imp*100:.2f}%")
                except Exception as e:
                    st.error(f"Error training models: {e}")

    elif st.session_state.page == "insights":
        # AI INSIGHTS PAGE
        st.markdown("### 💡 GenAI Executive Business Insights")
        
        if st.button("Generate AI Insights", key="gen_insights"):
            with st.spinner("Analyzing data..."):
                try:
                    ml_results = st.session_state.ml_results if st.session_state.ml_results else {}
                    insights = get_genai_insights(df_cleaned_viz, target_column, ml_results, gemini_api_key)
                    
                    for insight in insights:
                        render_insight_card(insight['title'], insight['desc'], insight['recommendation'])
                except Exception as e:
                    st.error(f"Error generating insights: {e}")

    elif st.session_state.page == "settings":
        # SETTINGS PAGE
        st.markdown("### ⚙️ Settings")
        st.info("Application Settings")
        st.write("- API Configuration: Set your Gemini API Key in the sidebar")
        st.write("- Data Pipeline: Auto-cleaning is enabled by default")
        st.write("- ML Models: Using AutoML with scikit-learn ensemble methods")

else:
    st.info("👈 Please upload a CSV/Excel file or enable the default Blinkit Demo Dataset to explore the dashboard.")


