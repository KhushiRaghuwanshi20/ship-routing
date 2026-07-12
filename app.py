import streamlit as st
import folium
from streamlit_folium import st_folium
from engine import RoutingEngine

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ship Routing System", layout="wide")

# --- REFINED PROFESSIONAL CSS ---
st.markdown("""
    <style>
    /* Global Background & Text */
    .stApp { background-color: #FFFFFF; }
    
    * { 
        color: #000000 !important; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }

    /* Main Blue Header */
    .main-header {
        text-align: center;
        background-color: #1E3A8A;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .main-header h1 { color: #FFFFFF !important; margin: 0; font-size: 28px; }

    /* Sidebar Styling - Clean & Visible */
    section[data-testid="stSidebar"] {
        background-color: #F1F5F9 !important;
        border-right: 2px solid #1E3A8A;
    }
    
    /* Input Parameter Box Fix */
    div[data-baseweb="select"] > div {
        border: 2px solid #1E3A8A !important;
        background-color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* Metric Cards - Professional Blue Highlight */
    [data-testid="stMetricValue"] {
        color: #1E3A8A !important;
        font-weight: 900 !important;
        font-size: 32px !important;
    }
    .stMetric {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='main-header'><h1>Optimal Ship Routing Intelligence System</h1></div>", unsafe_allow_html=True)

# --- PORTS DATA ---
PORTS = {
    "Mumbai, India": (18.95, 72.82),
    "Dubai, UAE": (25.01, 55.06),
    "Singapore Port": (1.27, 103.80),
    "Colombo, Sri Lanka": (6.94, 79.85),
    "Suez Canal": (29.93, 32.55)
}

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 🗺️ Route Control")
    origin = st.selectbox("DEPARTURE PORT", list(PORTS.keys()))
    destination = st.selectbox("ARRIVAL PORT", list(PORTS.keys()), index=1)
    
    st.divider()
    st.markdown("### ⚙️ Navigation Factors")
    weather = st.slider("WEATHER INTENSITY", 1.0, 5.0, 1.0)
    traffic = st.slider("TRAFFIC DENSITY", 1.0, 5.0, 1.0)
    
    st.divider()
    fuel_opt = st.checkbox("ENABLE FUEL OPTIMIZATION")

# --- ALGORITHM EXECUTION ---
engine = RoutingEngine(PORTS)

if origin != destination:
    res = engine.calculate_astar_path(origin, destination, weather, traffic, fuel_opt)

    # --- RESULTS DASHBOARD ---
    st.markdown("### 📊 Path Analytics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Direct Dist", f"{res['base_dist']} KM")
    c2.metric("A* Optimized Cost", f"{res['optimized_cost']}")
    c3.metric("Estimated ETA", f"{res['eta_hrs']} Hrs")
    c4.metric("Fuel Usage", f"{res['fuel_tons']} Tons")

    st.divider()

    # --- MAP & METHODOLOGY ---
    col_map, col_info = st.columns([2, 1])

    with col_map:
        st.subheader("Interactive Navigational Chart")
        # English Language Map
        m = folium.Map(location=[15, 75], zoom_start=4, tiles="CartoDB Voyager")
        
        # Drawing the path calculated by the algorithm
        folium.PolyLine(res['path'], color="#1E3A8A", weight=6, opacity=0.85).add_to(m)
        folium.Marker(PORTS[origin], tooltip="Origin", icon=folium.Icon(color='blue')).add_to(m)
        folium.Marker(PORTS[destination], tooltip="Destination", icon=folium.Icon(color='red')).add_to(m)
        
        st_folium(m, width="100%", height=500)

    with col_info:
        st.subheader("Algorithm Feedback")
        
        st.info(f"**Optimization Mode:** {'Low Carbon' if fuel_opt else 'Time Priority'}")
        
        st.write("**Cost Function Dynamics:**")
        st.caption("Integrating Distance, Weather, and Traffic into the A* Graph Search.")
        
        if weather > 3:
            st.warning("⚠️ High Risk: Routing penalty applied for safety.")
        else:
            st.success("✅ Clear Path: Maximum efficiency maintained.")

else:
    st.error("Select different ports to calculate route.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-weight: bold;'>SVIIT Indore | Department of Computer Science Engineering | 2026</p>", unsafe_allow_html=True)