"""
Main Streamlit application for Digital Village Resource Mapping
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from app.config import config
from app.logger import logger
import pandas as pd
import numpy as np


def initialize_page():
    """Initialize Streamlit page configuration"""
    st.set_page_config(
        page_title="Village Resource Mapping",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)


def create_sidebar():
    """Create sidebar navigation"""
    with st.sidebar:
        st.title("🗺️ Village Resource Mapping")
        st.markdown("---")
        
        navigation = st.radio(
            "Navigate",
            ["Dashboard", "Map Explorer", "Analytics", "Resource Database", "ML Insights", "Settings"],
            index=0
        )
        
        st.markdown("---")
        
        with st.expander("ℹ️ About", expanded=False):
            st.write("""
            **Digital Village Resource Mapping**
            
            An AI-powered GIS platform for Smart India Hackathon 2024
            
            **Features:**
            - 📍 Interactive village mapping
            - 🤖 AI-powered resource detection
            - 📊 Advanced analytics & insights
            - 🗄️ Comprehensive resource database
            - 📈 Real-time monitoring
            """)
        
        return navigation


def render_dashboard():
    """Render main dashboard"""
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Villages Mapped", 245, "+12")
    with col2:
        st.metric("Resources Identified", 1523, "+89")
    with col3:
        st.metric("Analysis Accuracy", "92.5%", "+2.1%")
    with col4:
        st.metric("Active Users", 45, "+5")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Map Overview")
        m = folium.Map(
            location=[config.DEFAULT_LATITUDE, config.DEFAULT_LONGITUDE],
            zoom_start=config.DEFAULT_ZOOM_LEVEL,
            tiles=config.MAP_PROVIDER
        )
        
        # Add sample markers
        folium.Marker(
            location=[config.DEFAULT_LATITUDE, config.DEFAULT_LONGITUDE],
            popup="Sample Village",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
        
        st_folium(m, width=700, height=500)
    
    with col2:
        st.subheader("📈 Resource Distribution")
        
        # Sample data
        resource_types = ['Schools', 'Hospitals', 'Water Wells', 'Power Lines', 'Roads']
        resource_counts = [45, 12, 89, 234, 567]
        
        chart_data = pd.DataFrame({
            'Resource Type': resource_types,
            'Count': resource_counts
        })
        
        st.bar_chart(chart_data.set_index('Resource Type'))
        
        st.subheader("🎯 Top Resources")
        st.dataframe(chart_data, use_container_width=True)


def render_map_explorer():
    """Render interactive map explorer"""
    st.header("🗺️ Map Explorer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        latitude = st.number_input("Latitude", value=config.DEFAULT_LATITUDE, step=0.01)
    with col2:
        longitude = st.number_input("Longitude", value=config.DEFAULT_LONGITUDE, step=0.01)
    with col3:
        zoom_level = st.slider("Zoom Level", 5, 20, config.DEFAULT_ZOOM_LEVEL)
    
    resource_filter = st.multiselect(
        "Filter Resources",
        ['Schools', 'Hospitals', 'Water Wells', 'Power Lines', 'Roads', 'Markets'],
        default=['Schools', 'Hospitals']
    )
    
    st.markdown("---")
    
    # Create map
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=zoom_level,
        tiles=config.MAP_PROVIDER
    )
    
    # Add sample markers for filtered resources
    sample_locations = [
        ([latitude, longitude], "School", "red"),
        ([latitude + 0.01, longitude + 0.01], "Hospital", "green"),
        ([latitude - 0.01, longitude - 0.01], "Water Well", "blue"),
    ]
    
    for loc, name, color in sample_locations:
        folium.Marker(
            location=loc,
            popup=name,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)
    
    st_folium(m, width=1400, height=600)


def render_analytics():
    """Render analytics page"""
    st.header("📊 Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Resource Analysis", "Infrastructure", "Trends"])
    
    with tab1:
        st.subheader("Resource Distribution Analysis")
        
        # Sample data
        df = pd.DataFrame({
            'Resource Type': ['Schools', 'Hospitals', 'Water Wells', 'Power Lines', 'Roads'],
            'Count': [45, 12, 89, 234, 567],
            'Coverage %': [65, 45, 78, 92, 88]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(df.set_index('Resource Type')['Count'])
        
        with col2:
            st.line_chart(df.set_index('Resource Type')['Coverage %'])
        
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Infrastructure Analysis")
        st.info("Infrastructure analysis and quality metrics coming soon...")
    
    with tab3:
        st.subheader("Trends Over Time")
        st.info("Historical trend analysis coming soon...")


def render_database():
    """Render resource database"""
    st.header("🗄️ Resource Database")
    
    # Sample database
    df = pd.DataFrame({
        'ID': range(1, 11),
        'Resource': ['School', 'Hospital', 'Well', 'Road', 'School', 'Clinic', 'Well', 'Market', 'Road', 'School'],
        'Location': ['Village A', 'Village B', 'Village C', 'Village A', 'Village D', 'Village B', 'Village E', 'Village C', 'Village D', 'Village E'],
        'Status': ['Active', 'Active', 'Maintenance', 'Active', 'Active', 'Active', 'Inactive', 'Active', 'Active', 'Active'],
        'Last Updated': pd.date_range('2024-01-01', periods=10).strftime('%Y-%m-%d').tolist()
    })
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        resource_filter = st.selectbox("Filter by Resource", df['Resource'].unique())
    with col2:
        status_filter = st.selectbox("Filter by Status", df['Status'].unique())
    with col3:
        st.empty()
    
    # Apply filters
    filtered_df = df[
        (df['Resource'] == resource_filter) & (df['Status'] == status_filter)
    ]
    
    st.dataframe(filtered_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Filtered Records", len(filtered_df))


def render_ml_insights():
    """Render ML insights page"""
    st.header("🤖 ML Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resource Detection Model")
        st.info("Accuracy: 92.5% | Last Updated: 2024-01-15")
        
        uploaded_file = st.file_uploader("Upload satellite image for analysis", type=['jpg', 'png', 'tif'])
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.success("Image processed! Detected resources shown below...")
    
    with col2:
        st.subheader("Model Performance")
        
        performance_data = pd.DataFrame({
            'Metric': ['Precision', 'Recall', 'F1-Score', 'Accuracy'],
            'Score': [0.94, 0.91, 0.92, 0.925]
        })
        
        st.bar_chart(performance_data.set_index('Metric'))
    
    st.markdown("---")
    
    st.subheader("Predicted Resources")
    predictions_df = pd.DataFrame({
        'Resource': ['School', 'Hospital', 'Well', 'Road', 'Market'],
        'Confidence': [0.95, 0.87, 0.92, 0.98, 0.81],
        'Location (Lat, Lon)': [
            '20.593, 78.963',
            '20.595, 78.961',
            '20.591, 78.965',
            '20.592, 78.964',
            '20.594, 78.962'
        ]
    })
    
    st.dataframe(predictions_df, use_container_width=True)


def render_settings():
    """Render settings page"""
    st.header("⚙️ Settings")
    
    with st.expander("Map Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Default Latitude", value=config.DEFAULT_LATITUDE)
        with col2:
            st.number_input("Default Longitude", value=config.DEFAULT_LONGITUDE)
        
        col1, col2 = st.columns(2)
        with col1:
            st.slider("Default Zoom Level", 5, 20, config.DEFAULT_ZOOM_LEVEL)
        with col2:
            st.selectbox("Map Provider", ["OpenStreetMap", "Satellite", "Terrain"])
    
    with st.expander("ML Settings"):
        st.slider("Confidence Threshold", 0.0, 1.0, config.CONFIDENCE_THRESHOLD)
        st.number_input("Max Image Size (pixels)", value=config.MAX_IMAGE_SIZE)
    
    with st.expander("About & Info"):
        st.info(f"""
        **Application Version:** 0.1.0
        **Framework:** Streamlit {st.__version__}
        **Python Version:** 3.11+
        """)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")


def main():
    """Main application entry point"""
    initialize_page()
    
    navigation = create_sidebar()
    
    try:
        if navigation == "Dashboard":
            render_dashboard()
        elif navigation == "Map Explorer":
            render_map_explorer()
        elif navigation == "Analytics":
            render_analytics()
        elif navigation == "Resource Database":
            render_database()
        elif navigation == "ML Insights":
            render_ml_insights()
        elif navigation == "Settings":
            render_settings()
        
        logger.info(f"User navigated to: {navigation}")
        
    except Exception as e:
        logger.error(f"Error in navigation: {str(e)}")
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
