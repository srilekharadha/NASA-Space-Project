
import streamlit as st
import pandas as pd
import requests
import folium

from streamlit_folium import st_folium
from folium.plugins import Draw
from datetime import date, timedelta
from geopy.geocoders import Nominatim


# =========================================================
# FIELD SHIFT - SMART AGRICULTURE PLATFORM
# =========================================================

st.set_page_config(
    page_title="FIELD SHIFT | Smart Agriculture",
    page_icon="🌱",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

defaults = {
    "nav": "Home",
    "next_page": None,
    "farmer": {},
    "latitude": 11.0168,
    "longitude": 76.9558,
    "crop": "Rice",
    "nasa_data": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


PAGES = [
    "Home",
    "Advanced Dashboard",
    "Farmer Setup",
    "Farm Mapping",
    "Crop Selection",
    "NASA POWER Analysis",
    "Farming Condition",
    "Smart Recommendations",
    "Voice Agri-Advisor",
    "About & Contact"
]

# ---------------- SAFE NAVIGATION ----------------

if st.session_state.next_page:
    next_page = st.session_state.next_page
    st.session_state.next_page = None

    if next_page in PAGES:
        st.session_state.nav = next_page


def go_to(page):
    st.session_state.next_page = page
    st.rerun()


# ---------------- CUSTOM CSS ----------------


# ---------------- PURPLE GALAXY THEME ----------------

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F7F2FF;
    color: #24113F;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #24113F, #3B1764);
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Main Title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #5B21B6;
}

/* Subtitle */
.subtitle {
    color: #7C6A99;
    font-size: 16px;
}

/* Hero Section */
.hero {
    background: linear-gradient(
        120deg,
        #24113F,
        #6D28D9,
        #A855F7
    );
    padding: 35px;
    border-radius: 18px;
    color: white;
}

.hero h1 {
    color: #FFFFFF;
    font-size: 38px;
}

.hero h3 {
    color: #F3E8FF;
}

.hero p {
    color: #F3E8FF;
    font-size: 17px;
}

/* Metric Cards */
.metric-card {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #E9D5FF;
    box-shadow: 0 3px 12px rgba(91, 33, 182, 0.07);
}

/* Section Headings */
.section-heading {
    color: #5B21B6;
    font-size: 25px;
    font-weight: 750;
}

/* Captions */
.small-note {
    color: #7C6A99;
    font-size: 13px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #6D28D9, #9333EA);
    color: white;
    border-radius: 9px;
    border: none;
    padding: 9px 18px;
    font-weight: 600;
    transition: 0.3s;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #581C87, #7E22CE);
    color: white;
    border: none;
    box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25);
}

/* Input Fields */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border: 1px solid #D8B4FE;
    border-radius: 8px;
}

/* Select Boxes */
.stSelectbox > div > div {
    border-color: #D8B4FE;
    border-radius: 8px;
}

/* Radio Buttons */
.stRadio label {
    color: #4C1D95;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #E9D5FF;
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #E9D5FF;
}

/* Success Messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Links */
a {
    color: #7E22CE !important;
}

/* Footer */
.footer {
    color: #7C6A99;
}

/* Farmer Setup - Form Label Visibility Fix */

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label,
.stRadio > label,
.stDateInput label,
.stCheckbox label,
.stForm label {
    color: #3B0764 !important;
    font-weight: 700 !important;
}

/* Input Text */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    color: #24113F !important;
    background-color: #FFFFFF !important;
}

/* Placeholder Text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9B8BAE !important;
}

/* Selectbox Text */
.stSelectbox div[data-baseweb="select"] * {
    color: #3B0764 !important;
}


/* ADVANCED DASHBOARD ONLY */

[data-testid="stAppViewContainer"]:has(.dashboard-scope) .dashboard-scope {
    color: #24113F;
}

[data-testid="stAppViewContainer"]:has(.dashboard-scope) [data-testid="stMetricLabel"],
[data-testid="stAppViewContainer"]:has(.dashboard-scope) [data-testid="stMetricLabel"] p {
    color: #3B0764 !important;
    font-weight: 700 !important;
}

[data-testid="stAppViewContainer"]:has(.dashboard-scope) [data-testid="stMetricValue"] {
    color: #24113F !important;
    font-weight: 800 !important;
}

/* ADVANCED DASHBOARD TEXT VISIBILITY ONLY */
[data-testid="stAppViewContainer"]:has(.dashboard-scope) [data-testid="stMetricLabel"],
[data-testid="stAppViewContainer"]:has(.dashboard-scope) [data-testid="stMetricLabel"] p,
[data-testid="stAppViewContainer"]:has(.dashboard-scope) label,
[data-testid="stAppViewContainer"]:has(.dashboard-scope) p,
[data-testid="stAppViewContainer"]:has(.dashboard-scope) span,
[data-testid="stAppViewContainer"]:has(.dashboard-scope) h1,
[data-testid="stAppViewContainer"]:has(.dashboard-scope) h2,
[data-testid="stAppViewContainer"]:has(.dashboard-scope) h3 {
    color: #24113F !important;
    font-weight: 600 !important;
}

[data-testid="stAppViewContainer"]:has(.dashboard-scope) [data-testid="stMetricValue"] {
    color: #3B0764 !important;
    font-weight: 800 !important;
}

/* ADVANCED DASHBOARD - METRIC LABELS AND VALUES ONLY */

[data-testid="stAppViewContainer"]:has(.dashboard-scope)
[data-testid="stMetricLabel"],
[data-testid="stAppViewContainer"]:has(.dashboard-scope)
[data-testid="stMetricLabel"] p {
    color: #3B0764 !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

[data-testid="stAppViewContainer"]:has(.dashboard-scope)
[data-testid="stMetricValue"],
[data-testid="stAppViewContainer"]:has(.dashboard-scope)
[data-testid="stMetricValue"] div {
    color: #24113F !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

[data-testid="stAppViewContainer"]:has(.dashboard-scope)
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E9D5FF !important;
    border-radius: 12px !important;
    padding: 12px !important;
}



</style>
""", unsafe_allow_html=True)



# ---------------- HELPER FUNCTIONS ----------------

def section_title(title, subtitle=None):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.caption(subtitle)


def get_latest_value(data, parameter):
    if not data or parameter not in data:
        return None

    values = data.get(parameter, {})
    valid = []

    for key, value in values.items():
        try:
            number = float(value)
            if number > -900:
                valid.append((key, number))
        except (ValueError, TypeError):
            pass

    if not valid:
        return None

    valid.sort(key=lambda x: x[0])
    return valid[-1][1]


def fetch_nasa_data(lat, lon):
    end_date = date.today() - timedelta(days=2)
    start_date = end_date - timedelta(days=6)

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M,GWETTOP",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result["properties"]["parameter"]

    except Exception as error:
        st.error(f"NASA POWER data could not be loaded: {error}")
        return None


def nasa_dataframe(data):
    if not data:
        return pd.DataFrame()

    temperature = data.get("T2M", {})
    rainfall = data.get("PRECTOTCORR", {})
    humidity = data.get("RH2M", {})
    soil = data.get("GWETTOP", {})

    df = pd.DataFrame({
        "Date": list(temperature.keys()),
        "Temperature (°C)": list(temperature.values()),
        "Rainfall (mm/day)": [
            rainfall.get(day) for day in temperature.keys()
        ],
        "Humidity (%)": [
            humidity.get(day) for day in temperature.keys()
        ],
        "Soil Wetness": [
            soil.get(day) for day in temperature.keys()
        ]
    })

    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")

    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("Date")
    return df


def crop_temperature_range(crop):
    ranges = {
        "Rice": (20, 35),
        "Wheat": (10, 25),
        "Maize": (18, 32),
        "Tomato": (18, 30),
        "Cotton": (21, 35),
        "Groundnut": (20, 30),
        "Sugarcane": (20, 35),
        "Millets": (20, 32)
    }

    return ranges.get(crop, (18, 32))


def farming_status(temp, rain, humidity):
    if temp is None:
        return "YELLOW", "Insufficient data to assess conditions."

    if temp < 10 or temp > 40:
        return "RED", "Temperature is outside the broad screening range."

    if rain is not None and rain > 30:
        return "YELLOW", "Recent rainfall is relatively high. Check drainage."

    if humidity is not None and humidity > 90:
        return "YELLOW", "High humidity may increase disease risk."

    return "GREEN", "No major warning detected by this basic screening."


def load_nasa():
    with st.spinner("Fetching NASA POWER environmental data..."):
        data = fetch_nasa_data(
            st.session_state.latitude,
            st.session_state.longitude
        )

    if data:
        st.session_state.nasa_data = data
        st.success("NASA POWER data loaded successfully!")


def current_dataframe():
    return nasa_dataframe(st.session_state.nasa_data)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("# 🌱 FIELD SHIFT")
    st.caption("Adapting Farms with NASA Data")

    st.divider()

    selected_page = st.radio(
        "NAVIGATION",
        PAGES,
        key="nav"
    )

    st.divider()

    st.markdown("### 🌍 Farm Coordinates")
    st.write(f"Latitude: {st.session_state.latitude:.4f}")
    st.write(f"Longitude: {st.session_state.longitude:.4f}")

    st.divider()
    st.caption("Smart Agriculture Platform")


# =========================================================
# HOME
# =========================================================

if selected_page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🌱 FIELD SHIFT</h1>
        <h3>Adapting Farms with NASA Data</h3>
        <p>
        A smart agricultural decision-support platform
        helping farmers understand environmental conditions
        and make informed farming decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    section_title("Welcome to Smart Agriculture")

    st.write(
        "FIELD SHIFT combines NASA POWER environmental estimates, "
        "farm location information and crop-based guidance "
        "to support agricultural planning."
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 🛰️ NASA Data")
        st.write("Explore environmental information from NASA POWER.")

    with b:
        st.markdown("### 🗺️ Farm Mapping")
        st.write("Select and view your farm location on an interactive map.")

    with c:
        st.markdown("### 🌾 Crop Guidance")
        st.write("Explore crop-related recommendations and alerts.")

    st.write("")
    section_title("Explore FIELD SHIFT")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Open Dashboard", use_container_width=True):
            go_to("Advanced Dashboard")

    with col2:
        if st.button("🗺️ Map My Farm", use_container_width=True):
            go_to("Farm Mapping")

    with col3:
        if st.button("🛰️ NASA Analysis", use_container_width=True):
            go_to("NASA POWER Analysis")


# =========================================================
# ADVANCED DASHBOARD
# =========================================================

elif selected_page == "Advanced Dashboard":

    st.markdown(
        '<div class="main-title">📊 Advanced Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your complete farm intelligence overview</div>',
        unsafe_allow_html=True
    )

    farmer = st.session_state.farmer

    # Metric visibility fix - labels and values only
    st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p {
        color: #3B0764 !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #24113F !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👨‍🌾 Farmer", farmer.get("name", "Not added"))

    with col2:
        st.metric("🌾 Selected Crop", st.session_state.crop)

    with col3:
        st.metric("📍 Latitude", f"{st.session_state.latitude:.3f}")

    with col4:
        st.metric("📍 Longitude", f"{st.session_state.longitude:.3f}")

    st.divider()

    section_title("🌦️ Recent Environmental Overview")

    if st.session_state.nasa_data is None:

        st.info("Load NASA POWER data to view your dashboard charts.")

        if st.button("🛰️ Load NASA POWER Data"):
            load_nasa()
            st.rerun()

    else:
        df = current_dataframe()

        if not df.empty:

            latest = df.iloc[-1]

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                value = latest["Temperature (°C)"]
                st.metric(
                    "🌡️ Temperature",
                    f"{value:.1f} °C" if pd.notna(value) else "N/A"
                )

            with c2:
                value = latest["Rainfall (mm/day)"]
                st.metric(
                    "🌧️ Rainfall",
                    f"{value:.1f} mm" if pd.notna(value) else "N/A"
                )

            with c3:
                value = latest["Humidity (%)"]
                st.metric(
                    "💧 Humidity",
                    f"{value:.1f} %" if pd.notna(value) else "N/A"
                )

            with c4:
                value = latest["Soil Wetness"]
                st.metric(
                    "🌱 Soil Wetness",
                    f"{value:.2f}" if pd.notna(value) else "N/A"
                )

            st.write("")
            section_title("📈 Environmental Data Trends")

            chart1, chart2 = st.columns(2)

            with chart1:
                st.markdown("#### 🌡️ Temperature Trend")
                st.line_chart(
                    df.set_index("Date")[["Temperature (°C)"]]
                )

            with chart2:
                st.markdown("#### 🌧️ Rainfall Trend")
                st.bar_chart(
                    df.set_index("Date")[["Rainfall (mm/day)"]]
                )

            chart3, chart4 = st.columns(2)

            with chart3:
                st.markdown("#### 💧 Humidity Trend")
                st.line_chart(
                    df.set_index("Date")[["Humidity (%)"]]
                )

            with chart4:
                st.markdown("#### 🌱 Soil Wetness Trend")
                st.line_chart(
                    df.set_index("Date")[["Soil Wetness"]]
                )

            st.divider()

            section_title("🚜 Farm Activity Summary")

            activity1, activity2 = st.columns(2)

            with activity1:
                st.markdown("#### Farm Information")
                st.write("**Farm Name:**", farmer.get("farm_name", "Not added"))
                st.write("**Farm Size:**", farmer.get("farm_size", "Not added"))
                st.write("**Farming Type:**", farmer.get("farming_type", "Not added"))
                st.write("**Location:**", farmer.get("location", "Not added"))

            with activity2:
                st.markdown("#### Current Project Status")
                st.write("✅ Farmer profile section available")
                st.write("✅ Interactive farm mapping available")
                st.write("✅ Crop selection available")
                st.write("✅ NASA POWER analysis available")
                st.write("✅ Smart recommendations available")

            st.caption(
                "NASA POWER provides gridded environmental estimates, "
                "not direct measurements from farm sensors or a live forecast."
            )

            if st.button("🔄 Refresh Environmental Data"):
                load_nasa()
                st.rerun()


    
# =========================================================
# FARMER SETUP
# =========================================================


elif selected_page == "Farmer Setup":

    st.markdown(
        '<div class="main-title">👨‍🌾 Farmer Setup</div>',
        unsafe_allow_html=True
    )

    section_title("Create Your Farm Profile")

    with st.form("farmer_form"):

        name = st.text_input("Farmer Name")
        farm_name = st.text_input("Farm Name")

        village = st.text_input("Village")
        town = st.text_input("Town / District")

        phone = st.text_input("Contact Number")

        col1, col2 = st.columns(2)

        with col1:
            farm_size = st.text_input("Farm Size (acres)")

        with col2:
            farming_type = st.selectbox(
                "Farming Type",
                ["Organic", "Conventional", "Mixed", "Natural Farming"]
            )

        submitted = st.form_submit_button("Save Farm Profile")

        if submitted:

            if not name or not farm_name or not village or not town:
                st.warning(
                    "Please enter Farmer Name, Farm Name, Village and Town."
                )

            else:
                try:
                    geolocator = Nominatim(
                        user_agent="field_shift_farm_mapping"
                    )

                    search_location = (
                        f"{village}, {town}, India"
                    )

                    place = geolocator.geocode(
                        search_location,
                        timeout=10
                    )

                    if place:

                        st.session_state.latitude = place.latitude
                        st.session_state.longitude = place.longitude

                        st.session_state.farm_location_name = (
                            f"{village}, {town}"
                        )

                        st.session_state.farmer = {
                            "name": name,
                            "farm_name": farm_name,
                            "location": f"{village}, {town}",
                            "phone": phone,
                            "farm_size": farm_size,
                            "farming_type": farming_type
                        }

                        st.success("Farmer profile saved successfully!")

                        st.info(
                            f"Farm location found: {place.address}"
                        )

                        st.success(
                            "Farm coordinates updated! "
                            "Open Farm Mapping to view your location."
                        )

                    else:
                        st.error(
                            "Location not found. Please check your "
                            "Village and Town spelling."
                        )

                except Exception as e:
                    st.error(
                        f"Location search failed: {e}"
                    )

# =========================================================
# FARM MAPPING
# =========================================================


elif selected_page == "Farm Mapping":

    st.markdown(
        '<div class="main-title">🗺️ Farm Mapping</div>',
        unsafe_allow_html=True
    )

    st.write("Click on the map to select your farm location.")

    # FARM MAP
    m = folium.Map(
        location=[
            st.session_state.latitude,
            st.session_state.longitude
        ],
        zoom_start=13
    )

    folium.Marker(
    [
        st.session_state.latitude,
        st.session_state.longitude
    ],
    tooltip="Selected Farm Location",
    popup=st.session_state.get(
        "farm_location_name", "Your Farm"
    ),
    icon=folium.Icon(color="green", icon="leaf")
).add_to(m)

    Draw(
        export=True,
        draw_options={
            "polyline": True,
            "polygon": True,
            "rectangle": True,
            "circle": True,
            "marker": True,
            "circlemarker": False
        }
    ).add_to(m)

    map_data = st_folium(
        m,
        width=None,
        height=500,
        returned_objects=["last_clicked"]
    )

    if map_data and map_data.get("last_clicked"):
        clicked = map_data["last_clicked"]

        st.session_state.latitude = clicked["lat"]
        st.session_state.longitude = clicked["lng"]

        st.success("Farm location coordinates updated!")

    st.write("### Selected Coordinates")

    st.code(
        f"Latitude: {st.session_state.latitude:.6f}\n"
        f"Longitude: {st.session_state.longitude:.6f}"
    )

    # GOOGLE MAPS NAVIGATION
    st.markdown("### 🚗 Navigate to Your Farm")

    st.write(
        "Open Google Maps to view directions to your selected farm location."
    )

    google_maps_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={st.session_state.latitude},"
        f"{st.session_state.longitude}"
        "&travelmode=driving"
    )

    st.link_button(
        "📍 Navigate to Farm",
        google_maps_url,
        use_container_width=True
    )

    st.caption(
        "Google Maps will open with your selected farm as the destination."
    )

    # NASA DATA
    if st.button("Get NASA Data for This Location"):
        load_nasa()
        st.rerun()

# =========================================================
# CROP SELECTION
# =========================================================

elif selected_page == "Crop Selection":

    st.markdown(
        '<div class="main-title">🌾 Crop Selection</div>',
        unsafe_allow_html=True
    )

    section_title("Choose Your Crop")

    crops = [
        "Rice",
        "Wheat",
        "Maize",
        "Tomato",
        "Cotton",
        "Groundnut",
        "Sugarcane",
        "Millets"
    ]

    selected_crop = st.selectbox(
        "Select Crop",
        crops,
        index=crops.index(st.session_state.crop)
    )

    st.session_state.crop = selected_crop

    crop_info = {
        "Rice": "Rice cultivation generally requires adequate water availability.",
        "Wheat": "Wheat growth is influenced by temperature and water availability.",
        "Maize": "Maize requires suitable temperature and soil moisture.",
        "Tomato": "Tomato cultivation benefits from suitable moisture and temperature.",
        "Cotton": "Cotton cultivation requires appropriate temperature and water management.",
        "Groundnut": "Groundnut performs best with suitable soil moisture and drainage.",
        "Sugarcane": "Sugarcane generally has a long growing period and water requirements.",
        "Millets": "Millets are important crops in many semi-arid farming regions."
    }

    st.success(f"Selected Crop: {selected_crop}")

    st.info(crop_info[selected_crop])


# =========================================================
# NASA POWER ANALYSIS
# =========================================================

elif selected_page == "NASA POWER Analysis":

    st.markdown(
        '<div class="main-title">🛰️ NASA POWER Analysis</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore recent environmental estimates for your selected farm coordinates."
    )

    st.write(
        f"Coordinates: {st.session_state.latitude:.4f}, "
        f"{st.session_state.longitude:.4f}"
    )

    if st.button("Fetch NASA POWER Data"):
        load_nasa()

    if st.session_state.nasa_data:
        df = current_dataframe()

        if not df.empty:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download Environmental Data",
                df.to_csv(index=False),
                file_name="field_shift_nasa_data.csv",
                mime="text/csv"
            )

            st.caption(
                "Data source: NASA POWER API. Values are gridded "
                "environmental estimates and may differ from local sensor readings."
            )


# =========================================================
# FARMING CONDITION
# =========================================================

elif selected_page == "Farming Condition":

    st.markdown(
        '<div class="main-title">🚦 Farming Condition</div>',
        unsafe_allow_html=True
    )

    if st.session_state.nasa_data is None:
        st.warning("Please fetch NASA POWER data first.")

        if st.button("Fetch Data Now"):
            load_nasa()
            st.rerun()

    else:
        temp = get_latest_value(
            st.session_state.nasa_data,
            "T2M"
        )

        rain = get_latest_value(
            st.session_state.nasa_data,
            "PRECTOTCORR"
        )

        humidity = get_latest_value(
            st.session_state.nasa_data,
            "RH2M"
        )

        status, message = farming_status(
            temp,
            rain,
            humidity
        )

        if status == "GREEN":
            st.success("🟢 GREEN – No major warning detected")

        elif status == "YELLOW":
            st.warning("🟡 YELLOW – Attention recommended")

        else:
            st.error("🔴 RED – Potential environmental concern")

        st.write(message)

        st.divider()

        st.metric(
            "Temperature",
            f"{temp:.1f} °C" if temp is not None else "N/A"
        )

        st.metric(
            "Rainfall",
            f"{rain:.1f} mm/day" if rain is not None else "N/A"
        )

        st.metric(
            "Humidity",
            f"{humidity:.1f} %" if humidity is not None else "N/A"
        )

        st.caption(
            "These are simple illustrative screening rules, not validated "
            "agronomic thresholds or a substitute for expert advice."
        )


# =========================================================
# SMART RECOMMENDATIONS
# =========================================================

elif selected_page == "Smart Recommendations":

    st.markdown(
        '<div class="main-title">💡 Smart Recommendations</div>',
        unsafe_allow_html=True
    )

    crop = st.session_state.crop

    recommendations = {
        "Rice": [
            "Monitor water availability regularly.",
            "Check field drainage after heavy rainfall.",
            "Observe crop growth for signs of pests or disease.",
            "Use locally recommended nutrient management."
        ],
        "Wheat": [
            "Monitor temperature during crop development.",
            "Check soil moisture regularly.",
            "Inspect crops for disease symptoms.",
            "Follow local sowing and nutrient guidance."
        ],
        "Maize": [
            "Monitor soil moisture.",
            "Check for pest activity.",
            "Maintain suitable field drainage.",
            "Use locally recommended fertilizer practices."
        ],
        "Tomato": [
            "Avoid prolonged waterlogging.",
            "Monitor leaf health regularly.",
            "Observe moisture conditions.",
            "Check for common crop diseases."
        ],
        "Cotton": [
            "Monitor pest activity.",
            "Check soil moisture conditions.",
            "Observe crop growth regularly.",
            "Follow local integrated pest management guidance."
        ],
        "Groundnut": [
            "Monitor soil moisture.",
            "Maintain good field drainage.",
            "Inspect crop health regularly.",
            "Follow locally recommended nutrient practices."
        ],
        "Sugarcane": [
            "Monitor water availability.",
            "Check field drainage.",
            "Observe crop growth and health.",
            "Follow local irrigation guidance."
        ],
        "Millets": [
            "Monitor rainfall and soil moisture.",
            "Inspect crop health regularly.",
            "Maintain suitable weed management.",
            "Use locally suitable seed varieties."
        ]
    }

    st.success(f"Recommendations for {crop}")

    for item in recommendations[crop]:
        st.checkbox(item, key=f"recommend_{crop}_{item}")

    st.info(
        "These are general educational suggestions. "
        "Consult local agricultural experts for farm-specific decisions."
    )


# =========================================================
# VOICE AGRI ADVISOR
# =========================================================

elif selected_page == "Voice Agri-Advisor":

    st.markdown(
        '<div class="main-title">🎙️ Voice Agri-Advisor</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask basic farming questions using the voice input feature."
    )

    language = st.selectbox(
        "Choose Language",
        ["English", "Tamil"]
    )

    st.components.v1.html("""
    <div style="font-family:Arial;padding:15px;background:#ffffff;
                border-radius:12px;border:1px solid #dce9dc;">
        <h3 style="color:#14532d;">🎙️ Voice Assistant</h3>
        <button id="start"
            style="background:#15803d;color:white;padding:12px 20px;
            border:0;border-radius:8px;cursor:pointer;">
            Start Speaking
        </button>
        <p id="result" style="color:#14532d;margin-top:15px;">
            Your speech will appear here.
        </p>
        <script>
        const button = document.getElementById("start");
        const result = document.getElementById("result");

        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.lang = "en-IN";

            button.onclick = () => {
                recognition.start();
                result.innerText = "Listening...";
            };

            recognition.onresult = (event) => {
                result.innerText =
                    event.results[0][0].transcript;
            };

            recognition.onerror = () => {
                result.innerText =
                    "Voice recognition error. Please try again.";
            };
        } else {
            button.disabled = true;
            result.innerText =
                "Speech recognition is not supported in this browser.";
        }
        </script>
    </div>
    """, height=200)

    st.caption(
        "Basic browser speech recognition demonstration. "
        "It does not automatically provide AI-generated farming answers."
    )

    question = st.text_input("Or type your farming question")

    if st.button("Get Basic Guidance"):
        q = question.lower()

        if "rain" in q or "மழை" in q:
            st.info(
                "Check recent rainfall information and field drainage."
            )

        elif "water" in q or "தண்ணீர்" in q:
            st.info(
                "Monitor soil moisture and follow crop-specific irrigation guidance."
            )

        elif "temperature" in q or "வெப்பம்" in q:
            st.info(
                "Check the recent NASA POWER temperature estimates."
            )

        elif question.strip():
            st.info(
                "Please check the Smart Recommendations and NASA POWER Analysis sections."
            )

        else:
            st.warning("Please enter a question first.")


# =========================================================
# ABOUT & CONTACT
# =========================================================

elif selected_page == "About & Contact":

    st.markdown(
        '<div class="main-title">🌍 About FIELD SHIFT</div>',
        unsafe_allow_html=True
    )

    st.write("""
    FIELD SHIFT is a smart agriculture decision-support prototype.

    It uses NASA POWER environmental data and farm location information
    to help users explore environmental conditions and general crop guidance.
    """)

    section_title("Our Key Features")

    st.write("🛰️ NASA POWER environmental data")
    st.write("🗺️ Interactive farm mapping")
    st.write("🌾 Crop selection")
    st.write("📊 Advanced environmental dashboard")
    st.write("🚦 Basic farming condition screening")
    st.write("💡 Crop-based general recommendations")
    st.write("🎙️ Basic voice advisor")

    st.divider()

    section_title("Contact")

    st.write("Project: FIELD SHIFT")
    st.write("Theme: Adapting Farms with NASA Data")
    st.write("Category: Smart Agriculture")

    st.info(
        "FIELD SHIFT is a prototype for agricultural decision support. "
        "Its outputs should be checked against local conditions and "
        "qualified agricultural guidance."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#64748b;padding:12px;">
        🌱 <b>FIELD SHIFT</b> | Adapting Farms with NASA Data
        <br>
        Smart Agriculture Decision Support Prototype
    </div>
    """,
    unsafe_allow_html=True
)
