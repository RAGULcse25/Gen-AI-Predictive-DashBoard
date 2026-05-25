import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Color palette inspired by the Blinkit Dashboard layout
THEME_COLORS = {
    "bg_dark": "#0B0F19",
    "card_bg": "#151C2C",
    "green": "#00C04F",
    "yellow": "#F9BC06",
    "blue": "#02A0FC",
    "purple": "#7C3AED",
    "text_light": "#F8FAFC",
    "text_muted": "#94A3B8"
}

def custom_plotly_layout(fig):
    """
    Applies custom styling to make Plotly charts blend with our premium dark dashboard theme.
    """
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=THEME_COLORS["text_light"],
        title_font_color=THEME_COLORS["text_light"],
        legend_font_color=THEME_COLORS["text_light"],
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            linecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color=THEME_COLORS["text_muted"])
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            linecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color=THEME_COLORS["text_muted"])
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    return fig

def get_kpis(df: pd.DataFrame, target_col: str):
    """
    Calculates 4-5 high-level KPIs based on the dataset.
    """
    kpis = []
    
    # KPI 1: Total Records
    kpis.append({
        "label": "Total Records",
        "value": f"{len(df):,}",
        "color": THEME_COLORS["blue"],
        "icon": "📊"
    })
    
    # KPI 2: Total Columns/Attributes
    kpis.append({
        "label": "Total Attributes",
        "value": str(df.shape[1]),
        "color": THEME_COLORS["yellow"],
        "icon": "⚙️"
    })
    
    # KPI 3 & 4: Numerical Target Statistics or Categorical stats
    if df[target_col].dtype in ['int64', 'float64']:
        total_val = df[target_col].sum()
        avg_val = df[target_col].mean()
        
        # Human readable format (Lakh/Crore or K/M/B)
        if total_val >= 10_000_000:
            formatted_sum = f"₹{total_val/10_000_000:.2f} Cr"
        elif total_val >= 100_000:
            formatted_sum = f"₹{total_val/100_000:.2f} Lakh"
        elif total_val >= 1_000:
            formatted_sum = f"${total_val/1_000:.1f}K"
        else:
            formatted_sum = f"{total_val:.2f}"
            
        kpis.append({
            "label": f"Total {target_col.title()}",
            "value": formatted_sum,
            "color": THEME_COLORS["green"],
            "icon": "💰"
        })
        
        kpis.append({
            "label": f"Avg {target_col.title()}",
            "value": f"{avg_val:.2f}",
            "color": THEME_COLORS["purple"],
            "icon": "📈"
        })
    else:
        unique_cnt = df[target_col].nunique()
        kpis.append({
            "label": f"Unique {target_col.title()}",
            "value": f"{unique_cnt:,}",
            "color": THEME_COLORS["green"],
            "icon": "🔑"
        })
        
        # Top Class name and percentage
        top_class = df[target_col].value_counts().index[0]
        top_pct = df[target_col].value_counts(normalize=True).values[0] * 100
        kpis.append({
            "label": f"Top Category ({top_class})",
            "value": f"{top_pct:.1f}%",
            "color": THEME_COLORS["purple"],
            "icon": "🏆"
        })
        
    return kpis

def generate_trend_chart(df: pd.DataFrame, target_col: str):
    """
    Finds a date column and plots target_col over time.
    """
    date_col = None
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower() or df[col].dtype == 'datetime64[ns]':
            date_col = col
            break
            
    if date_col:
        try:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col])
            df_temp = df_temp.sort_values(by=date_col)
            
            # Group by day or month depending on rows count
            if len(df_temp) > 500:
                trend_df = df_temp.groupby(df_temp[date_col].dt.to_period('M')).agg({target_col: 'sum' if df[target_col].dtype in ['int64', 'float64'] else 'count'}).reset_index()
                trend_df[date_col] = trend_df[date_col].dt.to_timestamp()
            else:
                trend_df = df_temp.groupby(df_temp[date_col].dt.date).agg({target_col: 'sum' if df[target_col].dtype in ['int64', 'float64'] else 'count'}).reset_index()
                
            fig = px.line(
                trend_df,
                x=date_col,
                y=target_col,
                color_discrete_sequence=[THEME_COLORS["green"]],
                title=f"{target_col.title()} Trend Over Time"
            )
            fig.update_traces(line=dict(width=3), mode='lines+markers')
            return custom_plotly_layout(fig)
        except Exception as e:
            pass
            
    # Fallback to index / first 30 rows
    fallback_df = df.head(30).reset_index()
    fig = px.line(
        fallback_df,
        x=fallback_df.index,
        y=target_col,
        color_discrete_sequence=[THEME_COLORS["green"]],
        title=f"Sample Trend ({target_col.title()})"
    )
    return custom_plotly_layout(fig)

def generate_category_pie(df: pd.DataFrame, target_col: str):
    """
    Finds a categorical column and plots category distribution.
    """
    cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    # Filter out target if target is categorical
    cat_cols = [c for c in cat_cols if c != target_col]
    
    if not cat_cols:
        # Fallback if no category columns: bin a numeric column
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        num_cols = [n for n in num_cols if n != target_col]
        if num_cols:
            df_temp = df.copy()
            df_temp['binned'] = pd.cut(df_temp[num_cols[0]], bins=3, labels=['Low', 'Medium', 'High'])
            primary_cat = 'binned'
        else:
            return None
    else:
        primary_cat = cat_cols[0]
        
    # Get top 5 categories
    cat_counts = df[primary_cat].value_counts().head(5).reset_index()
    cat_counts.columns = [primary_cat, 'count']
    
    fig = px.pie(
        cat_counts,
        values='count',
        names=primary_cat,
        hole=0.4,
        color_discrete_sequence=[THEME_COLORS["green"], THEME_COLORS["yellow"], THEME_COLORS["blue"], THEME_COLORS["purple"], "#FF6B6B"],
        title=f"Distribution of {primary_cat.title()}"
    )
    # Style as donut
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return custom_plotly_layout(fig)

def generate_rankings_bar(df: pd.DataFrame, target_col: str):
    """
    Groups target column by a category and creates horizontal bar chart.
    """
    cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    cat_cols = [c for c in cat_cols if c != target_col]
    
    if not cat_cols or df[target_col].dtype not in ['int64', 'float64']:
        # Fallback: Count of category values
        if cat_cols:
            ranking_cat = cat_cols[-1]
            ranking_df = df[ranking_cat].value_counts().head(8).reset_index()
            ranking_df.columns = [ranking_cat, 'Count']
            y_col = ranking_cat
            x_col = 'Count'
        else:
            return None
    else:
        # Use second category if available
        ranking_cat = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0]
        ranking_df = df.groupby(ranking_cat)[target_col].sum().sort_values(ascending=False).head(8).reset_index()
        y_col = ranking_cat
        x_col = target_col
        
    fig = px.bar(
        ranking_df,
        x=x_col,
        y=y_col,
        orientation='h',
        color_discrete_sequence=[THEME_COLORS["yellow"]],
        title=f"Top {y_col.title()} by {x_col.title()}"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return custom_plotly_layout(fig)

def generate_heatmap(df: pd.DataFrame):
    """
    Generates a heatmap. If datetime is present, generates a Day & Hour heatmap.
    Otherwise, generates a correlation matrix.
    """
    date_col = None
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower() or df[col].dtype == 'datetime64[ns]':
            date_col = col
            break
            
    if date_col:
        try:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col])
            df_temp['Day'] = df_temp[date_col].dt.day_name()
            df_temp['Hour'] = df_temp[date_col].dt.hour
            
            # Pivot table: Day vs Hour
            pivot_df = df_temp.groupby(['Day', 'Hour']).size().unstack(fill_value=0)
            
            # Reorder days
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            pivot_df = pivot_df.reindex(days_order).fillna(0)
            
            fig = px.imshow(
                pivot_df,
                labels=dict(x="Hour of Day", y="Day of Week", color="Count"),
                color_continuous_scale='Greens',
                title="Activity Heatmap (Day & Time)"
            )
            return custom_plotly_layout(fig)
        except:
            pass
            
    # Fallback to correlation heatmap
    num_df = df.select_dtypes(include=['number'])
    if num_df.shape[1] > 1:
        corr = num_df.corr().round(2)
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            title="Correlation Heatmap"
        )
        return custom_plotly_layout(fig)
        
    return None
