import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Sales': [1000, 1200, 900, 1500, 1800, 1700, 1600, 2000, 2200, 1900, 2100, 2500],
        'Expenses': [800, 850, 750, 950, 1000, 1100, 1200, 1300, 1400, 1200, 1100, 1000],
        'Customers': [100, 120, 115, 130, 140, 150, 160, 170, 180, 175, 165, 190]
    })

def update_line_chart(df, metric):
    fig = px.line(
        df,
        x='Month',
        y=metric,
        markers=True,
        title=f'Monthly {metric}'
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title=metric,
        template='plotly_white'
    )
    return fig

def update_bar_chart(df):
    avg_data = {
        'Metric': ['Sales', 'Expenses', 'Customers'],
        'Average': [
            df['Sales'].mean(),
            df['Expenses'].mean(),
            df['Customers'].mean() * 10  # Scaling for better visualization
        ]
    }
    fig = px.bar(
        avg_data,
        x='Metric',
        y='Average',
        title='Average Metrics',
        color='Metric'
    )
    fig.update_layout(template='plotly_white')
    return fig

def calculate_metrics(df, metric):
    total = df[metric].sum()
    avg = df[metric].mean()
    first = df[metric].iloc[0]
    last = df[metric].iloc[-1]
    growth = ((last - first) / first) * 100 if first > 0 else 0
    
    return total, avg, growth

def format_metric_value(value, metric):
    if metric != 'Customers':
        return f"${value:,.0f}"
    return f"{value:,.0f}"

def main():    
    st.set_page_config(
        page_title="Business Analytics Dashboard",
        layout="wide"
    )
    
    df = load_data()
    
    # Header
    st.title("Business Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    selected_metric = st.sidebar.selectbox(
        "Select Metric:",
        options=['Sales', 'Expenses', 'Customers'],
        index=0
    )
    
    # Convert month index to names for better display
    month_names = df['Month'].tolist()
    start_month, end_month = st.sidebar.select_slider(
        "Select Month Range:",
        options=range(len(month_names)),
        value=(0, 11),
        format_func=lambda x: month_names[x]
    )
    
    # Filter data based on selection
    filtered_df = df.iloc[start_month:end_month+1]
    
    # Key Metrics Section
    st.header("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    # Calculate metrics
    total, avg, growth = calculate_metrics(filtered_df, selected_metric)
    
    # Display metrics
    with col1:
        st.metric(
            label=f"Total {selected_metric}", 
            value=format_metric_value(total, selected_metric)
        )
    
    with col2:
        st.metric(
            label=f"Average {selected_metric}", 
            value=format_metric_value(avg, selected_metric)
        )
        
    with col3:
        st.metric(
            label="Growth Rate", 
            value=f"{growth:+.1f}%",
            delta=f"{growth:+.1f}%"
        )
    
    # Visualization Section
    st.markdown("---")
    st.header("Visualizations")
    
    # Create two columns for charts
    col1, col2 = st.columns([2, 1])
    
    # Line Chart
    with col1:
        st.subheader(f"Monthly Trend")
        line_fig = update_line_chart(filtered_df, selected_metric)
        st.plotly_chart(line_fig, use_container_width=True)
    
    # Bar Chart
    with col2:
        st.subheader("Comparison")
        bar_fig = update_bar_chart(filtered_df)
        st.plotly_chart(bar_fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.caption("Business Analytics Dashboard - Created with Streamlit")

if __name__ == "__main__":
    main()