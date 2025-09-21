# frontend/streamlit_app.py
"""Main Streamlit application for Entertainment Trend Analyzer"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Page config
st.set_page_config(
    page_title="Entertainment Trend Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# API Base URL
API_BASE = "http://127.0.0.1:5000/api"

def check_backend_connection():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def fetch_analytics_summary():
    """Fetch analytics summary from backend"""
    try:
        response = requests.get(f"{API_BASE}/analytics/summary", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def fetch_youtube_trending():
    """Fetch YouTube trending data"""
    try:
        response = requests.get(f"{API_BASE}/data/youtube/trending", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Entertainment Trend Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose Page", ["Dashboard", "Data Collection", "Analytics", "Settings"])
    
    # Backend status
    backend_status = check_backend_connection()
    if backend_status:
        st.sidebar.success("✅ Backend Connected")
    else:
        st.sidebar.error("❌ Backend Disconnected")
        st.error("⚠️ Backend server is not running. Please start it using: `python run.py`")
        return
    
    # Page routing
    if page == "Dashboard":
        show_dashboard()
    elif page == "Data Collection":
        show_data_collection()
    elif page == "Analytics":
        show_analytics()
    else:
        show_settings()

def show_dashboard():
    """Dashboard page"""
    st.header("📊 Trend Dashboard")
    
    # Fetch data
    with st.spinner("Loading dashboard data..."):
        analytics_data = fetch_analytics_summary()
        youtube_data = fetch_youtube_trending()
    
    if not analytics_data:
        st.error("Failed to load analytics data")
        return
    
    summary = analytics_data.get('summary', {})
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Content", summary.get('total_content', 0))
    
    with col2:
        platforms = summary.get('platforms', {})
        st.metric("YouTube Content", platforms.get('youtube', 0))
    
    with col3:
        st.metric("Instagram Content", platforms.get('instagram', 0))
    
    with col4:
        engagement = summary.get('engagement_stats', {})
        st.metric("Avg Engagement", f"{engagement.get('average_engagement_rate', 0)}%")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform distribution pie chart
        if platforms:
            fig_platforms = px.pie(
                values=list(platforms.values()),
                names=list(platforms.keys()),
                title="Content Distribution by Platform"
            )
            st.plotly_chart(fig_platforms, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        sentiment_data = summary.get('sentiment_distribution', {})
        if sentiment_data:
            fig_sentiment = px.bar(
                x=list(sentiment_data.keys()),
                y=list(sentiment_data.values()),
                title="Sentiment Distribution",
                color=list(sentiment_data.keys())
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Top hashtags
    st.subheader("🔥 Trending Hashtags")
    hashtags = summary.get('top_hashtags', [])
    if hashtags:
        hashtag_df = pd.DataFrame(hashtags)
        st.dataframe(hashtag_df, use_container_width=True)
    else:
        st.info("No hashtag data available")

def show_data_collection():
    """Data collection page"""
    st.header("📥 Data Collection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("YouTube Data")
        if st.button("Fetch YouTube Trending", key="youtube_btn"):
            with st.spinner("Fetching YouTube data..."):
                data = fetch_youtube_trending()
                if data and data.get('status') == 'success':
                    st.success(f"✅ Fetched {data.get('count', 0)} YouTube videos")
                    
                    # Display sample data
                    if data.get('data'):
                        sample_df = pd.DataFrame(data['data'][:5])  # First 5 items
                        st.dataframe(sample_df[['title', 'author', 'view_count', 'like_count']], use_container_width=True)
                else:
                    st.error("Failed to fetch YouTube data")
    
    with col2:
        st.subheader("Instagram Data")
        if st.button("Fetch Instagram Trending", key="instagram_btn"):
            with st.spinner("Fetching Instagram data..."):
                try:
                    response = requests.get(f"{API_BASE}/data/instagram/trending")
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ Fetched {data.get('count', 0)} Instagram posts")
                        
                        if data.get('data'):
                            sample_df = pd.DataFrame(data['data'][:5])
                            st.dataframe(sample_df[['title', 'author', 'like_count']], use_container_width=True)
                    else:
                        st.error("Failed to fetch Instagram data")
                except:
                    st.error("Error connecting to Instagram API")

def show_analytics():
    """Analytics page"""
    st.header("📈 Advanced Analytics")
    
    # Trending topics analysis
    st.subheader("🔥 Trending Topics Analysis")
    
    if st.button("Run Trend Analysis"):
        with st.spinner("Analyzing trends..."):
            try:
                response = requests.get(f"{API_BASE}/analytics/trending")
                if response.status_code == 200:
                    data = response.json()
                    trending_topics = data.get('trending_topics', [])
                    
                    if trending_topics:
                        # Create trending topics chart
                        df = pd.DataFrame(trending_topics)
                        fig = px.bar(
                            df.head(10), 
                            x='hashtag', 
                            y='score',
                            title="Top Trending Topics",
                            color='score'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show table
                        st.dataframe(df[['hashtag', 'score', 'volume', 'platforms']], use_container_width=True)
                    else:
                        st.info("No trending topics found")
                else:
                    st.error("Failed to analyze trends")
            except:
                st.error("Error running trend analysis")

def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("API Configuration")
    st.info("API keys are configured in the .env file")
    
    st.subheader("MCP Settings")
    st.checkbox("Enable MCP Analysis", value=True)
    st.selectbox("MCP Model", ["claude-3-sonnet", "gpt-4", "other"])
    
    st.subheader("Data Collection")
    st.slider("Max Results per Request", 10, 100, 50)
    st.slider("Update Interval (minutes)", 15, 120, 30)

if __name__ == "__main__":
    main()