import streamlit as st
from streamlit_js_eval import get_geolocation
from first_aid_data import FIRST_AID_CARDS
from ai_helper import analyze_text_emergency, analyze_image_emergency
from hospital_finder import find_nearby_hospitals

st.set_page_config(
    page_title="AI Emergency First Aid Assistant",
    page_icon="🚑",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fbff 0%, #eef5ff 50%, #fff5f5 100%);
}

.hero {
    background: linear-gradient(135deg, #d90429, #ef233c);
    padding: 35px;
    border-radius: 25px;
    color: white;
    text-align: center;
    box-shadow: 0px 8px 25px rgba(217, 4, 41, 0.3);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 45px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
}

.card {
    padding: 25px;
    border-radius: 22px;
    text-align: center;
    min-height: 160px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: 0.3s;
    border: 1px solid rgba(255,255,255,0.8);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.15);
}

.icon {
    font-size: 48px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 10px;
}

.result-box {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
    border-left: 7px solid #ef233c;
}

.emergency-box {
    background: #fff1f2;
    padding: 20px;
    border-radius: 18px;
    border-left: 6px solid #dc2626;
    margin-bottom: 15px;
}

.hospital-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <h1>🚑 AI Emergency First Aid Assistant</h1>
    <p>Instant first-aid guidance, AI emergency analysis, nearby hospitals, and emergency contacts</p>
</div>
""", unsafe_allow_html=True)


menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🩹 Common First Aid",
        "🤖 Custom Emergency Help",
        "🏥 Nearby Hospitals",
        "☎️ Emergency Numbers"
    ]
)


if menu == "🏠 Home":
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card" style="background:#ffe8e8;">
            <div class="icon">🩹</div>
            <div class="card-title">Common First Aid</div>
            <p>Quick help for common emergencies</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card" style="background:#e8f5ff;">
            <div class="icon">🤖</div>
            <div class="card-title">AI Help</div>
            <p>Text or image based emergency help</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card" style="background:#f0fff4;">
            <div class="icon">🏥</div>
            <div class="card-title">Hospitals</div>
            <p>Find nearby hospitals</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card" style="background:#fffbe6;">
            <div class="icon">☎️</div>
            <div class="card-title">Emergency Numbers</div>
            <p>Important helpline numbers</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Use the sidebar to open any feature.")


elif menu == "🩹 Common First Aid":
    st.header("🩹 Common First Aid")

    items = list(FIRST_AID_CARDS.items())

    for i in range(0, len(items), 4):
        cols = st.columns(4)

        for col, (name, data) in zip(cols, items[i:i+4]):
            with col:
                st.markdown(f"""
                <div class="card" style="background:{data['color']};">
                    <div class="icon">{data['icon']}</div>
                    <div class="card-title">{name}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"View {name} Help", key=name):
                    st.session_state.selected_card = name

    if "selected_card" in st.session_state:
        selected = st.session_state.selected_card
        data = FIRST_AID_CARDS[selected]

        st.subheader(f"{data['icon']} {selected} First Aid")

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        for index, step in enumerate(data["steps"], start=1):
            st.write(f"**Step {index}:** {step}")
        st.markdown("</div>", unsafe_allow_html=True)


elif menu == "🤖 Custom Emergency Help":
    st.header("🤖 Custom Emergency Help")

    option = st.radio(
        "Choose input type",
        ["Text Emergency Description", "Upload Emergency Image"],
        horizontal=True
    )

    if option == "Text Emergency Description":
        user_text = st.text_area(
            "Describe the emergency situation",
            placeholder="Example: My brother burned his hand with hot water..."
        )

        if st.button("Analyze Emergency"):
            if user_text.strip():
                with st.spinner("AI is analyzing the emergency..."):
                    result = analyze_text_emergency(user_text)

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter the emergency situation.")

    else:
        image_file = st.file_uploader(
            "Upload injury/emergency image",
            type=["jpg", "jpeg", "png"]
        )

        if image_file:
            st.image(image_file, caption="Uploaded Image", width=350)

            if st.button("Analyze Image"):
                with st.spinner("AI is analyzing the image..."):
                    result = analyze_image_emergency(image_file)

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)


# elif menu == "🏥 Nearby Hospitals":
#     st.header("🏥 Nearby Hospital Finder")

#     st.write("Click the button below to detect your current location and find nearby hospitals.")

#     # location = get_geolocation()
#     location = get_geolocation()

#     # st.write("Location Data:", location)
#     if location:
#         lat = location["coords"]["latitude"]
#         lon = location["coords"]["longitude"]

#         st.success(f"Location detected: {lat}, {lon}")

#         if st.button("Find Nearby Hospitals"):
#             with st.spinner("Searching nearby hospitals..."):
#                 hospitals = find_nearby_hospitals(lat, lon)

#             if hospitals:
#                 for hospital in hospitals:
#                     st.markdown(f"""
#                     <div class="hospital-card">
#                         <h3>🏥 {hospital['name']}</h3>
#                         <p><b>Distance:</b> {hospital['distance']} km</p>
#                         <a href="{hospital['maps']}" target="_blank">Open Directions</a>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.warning("No hospitals found nearby. Try increasing radius in code.")
#     else:
#         st.warning("Please allow location permission in your browser.")

elif menu == "🏥 Nearby Hospitals":

    st.header("🏥 Nearby Hospital Finder")

    st.write(
        "Click the button below to detect your current location and find nearby hospitals."
    )

    location = get_geolocation()

    if location:

        # User denied permission
        if "error" in location:

            st.error("❌ Location permission denied.")

            st.info(
                """
                To use this feature:

                1. Click the location icon in your browser address bar.
                2. Change Location permission to Allow.
                3. Refresh the page.
                """
            )

            st.write("Error Details:", location["error"])

        # Location successfully received
        elif "coords" in location:

            lat = location["coords"]["latitude"]
            lon = location["coords"]["longitude"]

            st.success("✅ Location detected successfully")

            st.write(f"📍 Latitude: {lat}")
            st.write(f"📍 Longitude: {lon}")

            if st.button("🔍 Find Nearby Hospitals"):

                with st.spinner("Searching nearby hospitals..."):

                    hospitals = find_nearby_hospitals(
                        lat,
                        lon
                    )

                if hospitals:

                    st.success(
                        f"Found {len(hospitals)} hospitals nearby"
                    )

                    for hospital in hospitals:

                        st.markdown(f"""
                        <div class="hospital-card">
                            <h3>🏥 {hospital['name']}</h3>
                            <p><b>Distance:</b> {hospital['distance']} km</p>
                            <a href="{hospital['maps']}" target="_blank">
                                🗺️ Open Directions
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

                else:

                    st.warning(
                        "No hospitals found nearby."
                    )

                    st.markdown(
                        f"""
                        ### 🌍 Search on Google Maps

                        [Open Google Maps Hospital Search](https://www.google.com/maps/search/hospital/@{lat},{lon},15z)
                        """
                    )

        else:

            st.warning(
                "Unable to retrieve coordinates."
            )

            st.write(location)

    else:

        st.warning(
            "Waiting for location permission..."
        )
elif menu == "☎️ Emergency Numbers":
    st.header("☎️ Emergency Contact Numbers")

    numbers = {
        "National Emergency": "112",
        "Ambulance": "108 / 102",
        "Police": "100",
        "Fire": "101",
        "Women Helpline": "1091",
        "Child Helpline": "1098",
        "Medical Helpline": "104"
    }

    for name, number in numbers.items():
        st.markdown(f"""
        <div class="emergency-box">
            <h3>{name}</h3>
            <h2>{number}</h2>
        </div>
        """, unsafe_allow_html=True)