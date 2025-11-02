import streamlit as st
import pandas as pd
import json
from datetime import datetime
import requests
import random

# Configure the page
st.set_page_config(
    page_title="DisasterStay India - Emergency Housing",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful dark theme with gradients
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e0e0;
    }
    
    /* Headers with beautiful gradients */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        font-size: 1.8rem;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Cards with glass morphism effect */
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        color: #e0e0e0;
    }
    
    /* Emergency card with urgent gradient */
    .emergency-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Shelter cards with different gradients */
    .shelter-card {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.2) 0%, rgba(52, 152, 219, 0.2) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(46, 204, 113, 0.3);
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        color: #e0e0e0;
    }
    
    /* Metric cards with vibrant gradients */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Chat bubbles */
    .chat-bubble {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-bubble {
        background: rgba(255, 255, 255, 0.15);
        margin-right: 2rem;
        color: #e0e0e0;
    }
    
    /* Beautiful buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
    }
    
    /* Emergency button */
    .emergency-button button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    /* Input fields styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: #e0e0e0;
        padding: 0.5rem;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        padding: 0 1rem;
        background: transparent;
        color: #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Metric value styling */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Divider styling */
    .stDivider {
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Success and error messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.2) 0%, rgba(46, 204, 113, 0.1) 100%);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 10px;
        color: #2ecc71;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.2) 0%, rgba(231, 76, 60, 0.1) 100%);
        border: 1px solid rgba(231, 76, 60, 0.3);
        border-radius: 10px;
        color: #e74c3c;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.2) 0%, rgba(52, 152, 219, 0.1) 100%);
        border: 1px solid rgba(52, 152, 219, 0.3);
        border-radius: 10px;
        color: #3498db;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Text colors for better readability */
    p, li, span {
        color: #e0e0e0 !important;
    }
    
    strong {
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

class DisasterChatbot:
    def __init__(self):
        self.responses = {
            "hello": "Namaste! 🌟 I'm here to help you find emergency shelter during disasters. How can I assist you today?",
            "hi": "Namaste! 🙏 I'm DisasterStay Assistant. I can help you find shelter, emergency contacts, and safety information.",
            "shelter": "🏠 I can help you find emergency shelters. Go to the 'Find Shelter' section and enter your family size and location preferences.",
            "emergency": "🚨 For immediate emergencies, call 112 (National Emergency Number) or 108 (Ambulance). You can also use the emergency contacts in the app.",
            "flood": "🌊 During floods: Move to higher ground, avoid walking in floodwaters, and follow evacuation orders. Check the safety zones map in the app.",
            "earthquake": "🌋 During earthquakes: Drop, Cover, and Hold On. Stay away from buildings and windows. After shaking stops, move to open areas.",
            "cyclone": "🌀 During cyclones: Stay indoors, away from windows. Keep emergency kit ready. Listen to weather updates on All India Radio.",
            "medical": "🏥 For medical emergencies: Call 108 for ambulance. Major hospitals in your area are listed in the emergency info section.",
            "food": "🍲 Food and water distribution centers are available at most shelters. You can also contact: Indian Red Cross - 011-23711551",
            "contact": "📞 Emergency Contacts: Police-100, Fire-101, Ambulance-108, Disaster Relief-011-1078, Women Helpline-181",
            "thanks": "You're welcome! 🙏 Stay safe and don't hesitate to ask if you need more help.",
            "help": "🆘 I can help you with: Finding shelters, Emergency contacts, Safety tips, Disaster information. What do you need?",
            "location": "📍 I can help you find shelters in major Indian cities: Delhi, Mumbai, Chennai, Kolkata, Bangalore, Hyderabad and more. Please specify your city.",
            "capacity": "🛏️ Shelter capacities vary from 20 to 500 people. Use the filter in 'Find Shelter' to see current availability.",
            "family": "👨‍👩‍👧‍👦 Most shelters can accommodate families. Please specify your family size in the search form for accurate matching.",
            "pets": "🐕 Some shelters allow pets. Look for the 'Pets Allowed' amenity when searching for shelters.",
            "children": "👶 Many shelters have child-friendly facilities and special care. Look for 'Child Care' in shelter amenities."
        }
    
    def get_response(self, message):
        message = message.lower().strip()
        
        # Check for keywords in the message
        for keyword, response in self.responses.items():
            if keyword in message:
                return response
        
        return "🤖 I'm here to help with disaster-related queries. You can ask me about shelters, emergency contacts, safety tips, or current disasters. For specific help, try phrases like 'find shelter', 'emergency contacts', or 'safety tips'."

class DisasterStay:
    def __init__(self):
        self.shelters = []
        self.disasters = []
        self.requests = []
        self.indian_cities = {
            "Delhi": ["Central Delhi", "South Delhi", "North Delhi", "West Delhi", "East Delhi"],
            "Mumbai": ["South Mumbai", "Western Suburbs", "Eastern Suburbs", "Nav Mumbai"],
            "Chennai": ["North Chennai", "South Chennai", "Central Chennai", "West Chennai"],
            "Kolkata": ["North Kolkata", "South Kolkata", "Central Kolkata", "East Kolkata"],
            "Bangalore": ["Central Bangalore", "North Bangalore", "South Bangalore", "East Bangalore", "West Bangalore"],
            "Hyderabad": ["Old City", "New City", "West Hyderabad", "East Hyderabad"],
            "Ahmedabad": ["West Zone", "East Zone", "North Zone", "South Zone"],
            "Pune": ["Pune City", "Pimpri-Chinchwad", "Hinjewadi", "Hadapsar"]
        }
        self.load_sample_data()
    
    def load_sample_data(self):
        # Sample shelters data for Indian cities
        self.shelters = [
            {"id": "shelter-1", "name": "Delhi Central Relief Camp", "capacity": 200, "available_beds": 150, 
             "location": "Connaught Place, Delhi", "zone": "Central Delhi", "contact": "011-23345678", 
             "amenities": ["Food", "Medical", "Showers", "Child Care"], "city": "Delhi",
             "image": "🏢", "last_updated": "2 hours ago"},
            
            {"id": "shelter-2", "name": "Mumbai Coastal Safe Haven", "capacity": 300, "available_beds": 220, 
             "location": "Marine Drive, Mumbai", "zone": "South Mumbai", "contact": "022-26543210", 
             "amenities": ["Food", "Medical", "Pets Allowed", "Counseling"], "city": "Mumbai",
             "image": "🏫", "last_updated": "1 hour ago"},
            
            {"id": "shelter-3", "name": "Chennai Flood Relief Center", "capacity": 150, "available_beds": 85, 
             "location": "Anna Nagar, Chennai", "zone": "North Chennai", "contact": "044-26251817", 
             "amenities": ["Food", "Medical", "Showers", "Clothing"], "city": "Chennai",
             "image": "🏣", "last_updated": "3 hours ago"},
            
            {"id": "shelter-4", "name": "Kolkata Emergency Shelter", "capacity": 180, "available_beds": 180, 
             "location": "Salt Lake City, Kolkata", "zone": "East Kolkata", "contact": "033-24001234", 
             "amenities": ["Food", "Child Care", "Sleeping Bags", "Elderly Care"], "city": "Kolkata",
             "image": "🏬", "last_updated": "Just now"},
            
            {"id": "shelter-5", "name": "Bangalore Tech Park Shelter", "capacity": 120, "available_beds": 65, 
             "location": "Whitefield, Bangalore", "zone": "East Bangalore", "contact": "080-22998877", 
             "amenities": ["Food", "Medical", "WiFi", "Charging Stations"], "city": "Bangalore",
             "image": "🏛️", "last_updated": "4 hours ago"}
        ]
        
        # Sample active disasters in India
        self.disasters = [
            {"id": "flood-2024", "name": "Assam Floods 2024", "type": "flood", 
             "location": "Assam, Northeast India", "severity": "high", "active": True,
             "affected_areas": ["Guwahati", "Dibrugarh", "Jorhat", "Silchar"],
             "description": "Heavy monsoon rains causing Brahmaputra river to overflow"},
            
            {"id": "cyclone-2024", "name": "Cyclone Tej", "type": "cyclone", 
             "location": "Coastal Odisha & Andhra Pradesh", "severity": "medium", "active": True,
             "affected_areas": ["Puri", "Visakhapatnam", "Bhubaneswar", "Gopalpur"],
             "description": "Cyclone forming in Bay of Bengal, expected to make landfall in 48 hours"}
        ]
    
    def register_shelter(self, name, capacity, location, zone, contact, amenities, city):
        shelter = {
            "id": f"shelter-{len(self.shelters)+1}",
            "name": name,
            "capacity": capacity,
            "available_beds": capacity,
            "location": location,
            "zone": zone,
            "contact": contact,
            "amenities": amenities,
            "city": city,
            "image": random.choice(["🏢", "🏫", "🏣", "🏬", "🏛️"]),
            "last_updated": "Just now"
        }
        self.shelters.append(shelter)
        return shelter
    
    def find_housing(self, city, family_size, special_needs=""):
        available_shelters = []
        for shelter in self.shelters:
            if shelter["available_beds"] >= family_size and (not city or shelter["city"] == city):
                shelter_copy = shelter.copy()
                shelter_copy["beds_needed"] = family_size
                shelter_copy["match_score"] = self.calculate_match_score(shelter, special_needs)
                available_shelters.append(shelter_copy)
        
        # Sort by best match
        available_shelters.sort(key=lambda x: x["match_score"], reverse=True)
        return available_shelters
    
    def calculate_match_score(self, shelter, special_needs):
        score = 0
        amenities = shelter.get("amenities", [])
        
        if "Medical" in special_needs and "Medical" in amenities:
            score += 3
        if "Children" in special_needs and "Child Care" in amenities:
            score += 2
        if "Pets" in special_needs and "Pets Allowed" in amenities:
            score += 2
        if "Elderly" in special_needs and "Elderly Care" in amenities:
            score += 2
        if "WiFi" in special_needs and "WiFi" in amenities:
            score += 1
            
        return score
    
    def report_capacity(self, shelter_id, available_beds):
        for shelter in self.shelters:
            if shelter["id"] == shelter_id:
                shelter["available_beds"] = available_beds
                shelter["last_updated"] = "Just now"
                return shelter
        return None

def main():
    # Initialize session state
    if 'disaster_stay' not in st.session_state:
        st.session_state.disaster_stay = DisasterStay()
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = DisasterChatbot()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    ds = st.session_state.disaster_stay
    chatbot = st.session_state.chatbot
    
    # Header with beautiful design
    st.markdown('<h1 class="main-header">🏠 DisasterStay India</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #b0b0b0; margin-bottom: 3rem;">Emergency Housing Coordination Platform - Connecting people with safe shelter during disasters</p>', unsafe_allow_html=True)
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_beds = sum(s["available_beds"] for s in ds.shelters)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛏️ Available Beds</h3>
            <div class="metric-value">{total_beds}</div>
            <p>Across all shelters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_shelters = len([s for s in ds.shelters if s["available_beds"] > 0])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏠 Active Shelters</h3>
            <div class="metric-value">{active_shelters}</div>
            <p>Ready to help</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_disasters = len([d for d in ds.disasters if d["active"]])
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚠️ Active Disasters</h3>
            <div class="metric-value">{active_disasters}</div>
            <p>Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cities_covered = len(set(s["city"] for s in ds.shelters))
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏙️ Cities Covered</h3>
            <div class="metric-value">{cities_covered}</div>
            <p>Across India</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Emergency Alert
    active_disasters_list = [d for d in ds.disasters if d["active"]]
    if active_disasters_list:
        st.markdown("""
        <div class="emergency-card">
            <h3>🚨 ACTIVE DISASTER ALERT</h3>
            <p>Emergency shelters are activated in affected areas. Find safe shelter immediately if you're in these regions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Find Shelter", "📊 Manage", "🗺️ Disaster Info", "💬 Ask Assistant", "📞 Emergency"])
    
    with tab1:
        display_find_shelter(ds)
    
    with tab2:
        display_shelter_management(ds)
    
    with tab3:
        display_disaster_info(ds)
    
    with tab4:
        display_chatbot(chatbot)
    
    with tab5:
        display_emergency_contacts()

def display_find_shelter(ds):
    st.markdown('<div class="sub-header">🔍 Find Safe Shelter Near You</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Search form
            col1, col2 = st.columns(2)
            with col1:
                city = st.selectbox("Select City", ["All Cities"] + list(ds.indian_cities.keys()))
                family_size = st.number_input("Number of People", min_value=1, max_value=20, value=4, help="Total people needing shelter")
            
            with col2:
                if city != "All Cities":
                    zone = st.selectbox("Preferred Zone", ["Any Zone"] + ds.indian_cities[city])
                else:
                    zone = st.selectbox("Preferred Zone", ["Any Zone"])
                
                special_needs = st.multiselect("Special Requirements",
                                             ["Medical Conditions", "Children", "Elderly", "Pets", "WiFi Access", "None"])
            
            if st.button("🏠 Search Available Shelters", use_container_width=True):
                with st.spinner("Searching for safe shelters..."):
                    results = ds.find_housing(city if city != "All Cities" else "", family_size, ", ".join(special_needs))
                    
                    if results:
                        st.success(f"🎉 Found {len(results)} safe shelters matching your needs!")
                        
                        for shelter in results:
                            display_shelter_card(shelter, family_size)
                    else:
                        st.error("❌ No shelters found matching your criteria. Try expanding your search area or contact emergency services.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Quick help section
        st.markdown("""
        <div class="card">
            <h3>🚨 Quick Help</h3>
            <p><strong>Immediate Assistance:</strong></p>
            <p>• Call 112 for emergencies</p>
            <p>• Call 108 for ambulance</p>
            <p>• Women's Helpline: 181</p>
            <p>• Child Helpline: 1098</p>
            <br>
            <p><strong>Disaster Preparedness:</strong></p>
            <p>• Keep documents ready</p>
            <p>• Have emergency contacts</p>
            <p>• Prepare emergency kit</p>
        </div>
        """, unsafe_allow_html=True)

def display_shelter_card(shelter, family_size):
    st.markdown(f"""
    <div class="shelter-card">
        <div style="display: flex; justify-content: between; align-items: start;">
            <div style="flex: 1;">
                <h3>{shelter['image']} {shelter['name']}</h3>
                <p><strong>📍 Location:</strong> {shelter['location']}</p>
                <p><strong>🏙️ City:</strong> {shelter['city']} | <strong>📍 Zone:</strong> {shelter['zone']}</p>
                <p><strong>🛏️ Available:</strong> {shelter['available_beds']} beds (Capacity: {shelter['capacity']})</p>
                <p><strong>📞 Contact:</strong> {shelter['contact']}</p>
                <p><strong>⭐ Match Score:</strong> {shelter['match_score']}/5</p>
                <p><strong>🕒 Last Updated:</strong> {shelter['last_updated']}</p>
            </div>
        </div>
        <p><strong>🏪 Amenities:</strong> {', '.join(shelter['amenities'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(f"📞 Call for Reservation", key=f"call_{shelter['id']}"):
            st.success(f"💬 Please call {shelter['contact']} to reserve {family_size} beds at {shelter['name']}")
    with col2:
        if st.button("📍 Get Directions", key=f"dir_{shelter['id']}"):
            st.info(f"🗺️ Navigate to: {shelter['location']}")
    
    st.divider()

def display_shelter_management(ds):
    st.markdown('<div class="sub-header">📊 Shelter Management Portal</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ Register New Shelter", "📈 Update Status"])
    
    with tab1:
        st.markdown("""
        <div class="card">
            <h3>Register New Emergency Shelter</h3>
            <p>Help your community by registering available space as emergency shelter</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_shelter"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Shelter Name", placeholder="e.g., Community Center Relief Camp")
                capacity = st.number_input("Total Capacity", min_value=1, max_value=1000, value=50)
                city = st.selectbox("City", list(ds.indian_cities.keys()))
                zone = st.selectbox("Zone", ds.indian_cities[city])
            
            with col2:
                location = st.text_input("Full Address")
                contact = st.text_input("Contact Number", placeholder="e.g., 011-12345678")
                amenities = st.multiselect("Available Facilities", 
                                         ["Food", "Medical", "Showers", "Child Care", "Pets Allowed", 
                                          "Sleeping Bags", "Clothing", "Counseling", "WiFi", "Elderly Care"])
            
            if st.form_submit_button("🏠 Register Shelter", use_container_width=True):
                if name and location and contact:
                    new_shelter = ds.register_shelter(name, capacity, location, zone, contact, amenities, city)
                    st.success(f"🎉 Shelter '{name}' registered successfully! Shelter ID: {new_shelter['id']}")
                else:
                    st.error("❌ Please fill all required fields")
    
    with tab2:
        st.markdown("""
        <div class="card">
            <h3>Update Shelter Capacity</h3>
            <p>Keep shelter information updated to help people find available space</p>
        </div>
        """, unsafe_allow_html=True)
        
        shelter_options = {s["name"]: s["id"] for s in ds.shelters}
        selected_shelter = st.selectbox("Select Shelter to Update", list(shelter_options.keys()))
        
        if selected_shelter:
            shelter_id = shelter_options[selected_shelter]
            current_shelter = next((s for s in ds.shelters if s["id"] == shelter_id), None)
            
            if current_shelter:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Current Available Beds", current_shelter["available_beds"])
                with col2:
                    new_capacity = st.number_input("Update Available Beds", 
                                                 min_value=0, 
                                                 max_value=current_shelter["capacity"],
                                                 value=current_shelter["available_beds"])
                
                if st.button("🔄 Update Capacity", use_container_width=True):
                    updated = ds.report_capacity(shelter_id, new_capacity)
                    if updated:
                        st.success(f"✅ Updated {updated['name']} to {new_capacity} available beds")

def display_disaster_info(ds):
    st.markdown('<div class="sub-header">🗺️ Live Disaster Information</div>', unsafe_allow_html=True)
    
    # Active disasters
    active_disasters = [d for d in ds.disasters if d["active"]]
    if active_disasters:
        for disaster in active_disasters:
            if disaster["type"] == "flood":
                icon = "🌊"
                color = "#3498db"
            elif disaster["type"] == "cyclone":
                icon = "🌀"
                color = "#e74c3c"
            elif disaster["type"] == "earthquake":
                icon = "🌋"
                color = "#e67e22"
            else:
                icon = "⚠️"
                color = "#f39c12"
            
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid {color};">
                <h3>{icon} {disaster['name']}</h3>
                <p><strong>📍 Location:</strong> {disaster['location']}</p>
                <p><strong>📊 Severity:</strong> {disaster['severity'].title()}</p>
                <p><strong>📝 Description:</strong> {disaster['description']}</p>
                <p><strong>🏘️ Affected Areas:</strong> {', '.join(disaster['affected_areas'])}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No active major disasters currently. Stay prepared!")
    
    # Safety tips
    st.markdown("""
    <div class="card">
        <h3>🛡️ Disaster Safety Tips</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <h4>🌊 Flood Safety</h4>
                <p>• Move to higher ground</p>
                <p>• Avoid walking in floodwaters</p>
                <p>• Don't drive through flooded areas</p>
            </div>
            <div>
                <h4>🌀 Cyclone Safety</h4>
                <p>• Stay indoors away from windows</p>
                <p>• Keep emergency kit ready</p>
                <p>• Listen to All India Radio updates</p>
            </div>
            <div>
                <h4>🌋 Earthquake Safety</h4>
                <p>• Drop, Cover, and Hold On</p>
                <p>• Stay away from buildings</p>
                <p>• Move to open areas after shaking</p>
            </div>
            <div>
                <h4>🔥 Fire Safety</h4>
                <p>• Stop, Drop, and Roll if on fire</p>
                <p>• Crawl low in smoke</p>
                <p>• Feel doors before opening</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_chatbot(chatbot):
    st.markdown('<div class="sub-header">💬 DisasterStay Assistant</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p>Namaste! I'm your DisasterStay Assistant. I can help you with:</p>
        <p>• Finding emergency shelters</p>
        <p>• Emergency contact information</p>
        <p>• Disaster safety tips</p>
        <p>• Current disaster information</p>
        <p><strong>Try asking:</strong> "Find shelter", "Emergency contacts", "Flood safety", "Help"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history[-10:]:  # Show last 10 messages
            if chat["role"] == "user":
                st.markdown(f"""
                <div class="chat-bubble user-bubble">
                    <strong>You:</strong> {chat["message"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble bot-bubble">
                    <strong>🤖 Assistant:</strong> {chat["message"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Type your message here...", placeholder="Ask about shelters, emergencies, or safety tips...")
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        
        # Get bot response
        response = chatbot.get_response(user_input)
        st.session_state.chat_history.append({"role": "bot", "message": response})
        
        # Rerun to update chat display
        st.rerun()
    
    # Quick action buttons
    st.markdown("### Quick Questions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Find Shelter", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "message": "shelter"})
            response = chatbot.get_response("shelter")
            st.session_state.chat_history.append({"role": "bot", "message": response})
            st.rerun()
    with col2:
        if st.button("🚨 Emergency", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "message": "emergency"})
            response = chatbot.get_response("emergency")
            st.session_state.chat_history.append({"role": "bot", "message": response})
            st.rerun()
    with col3:
        if st.button("🆘 Help", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "message": "help"})
            response = chatbot.get_response("help")
            st.session_state.chat_history.append({"role": "bot", "message": response})
            st.rerun()

def display_emergency_contacts():
    st.markdown('<div class="sub-header">📞 Emergency Contacts & Resources</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="emergency-card">
            <h3>🚨 Immediate Emergency</h3>
            <h2>112</h2>
            <p>National Emergency Number</p>
            <p><strong>Police:</strong> 100</p>
            <p><strong>Fire:</strong> 101</p>
            <p><strong>Ambulance:</strong> 108</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>🏥 Medical Emergencies</h3>
            <p><strong>Ambulance:</strong> 108</p>
            <p><strong>COVID Helpline:</strong> 1075</p>
            <p><strong>Blood Bank:</strong> 1910</p>
            <p><strong>Poison Control:</strong> 1066</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>👥 Special Helplines</h3>
            <p><strong>Women's Helpline:</strong> 181</p>
            <p><strong>Child Helpline:</strong> 1098</p>
            <p><strong>Senior Citizens:</strong> 14567</p>
            <p><strong>Mental Health:</strong> 080-46110007</p>
            <p><strong>Disaster Relief:</strong> 011-1078</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>🏢 Relief Organizations</h3>
            <p><strong>NDMA:</strong> 011-26701700</p>
            <p><strong>Indian Red Cross:</strong> 011-23711551</p>
            <p><strong>Goonj:</strong> 011-26972351</p>
            <p><strong>SEEDS:</strong> 011-41055554</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()