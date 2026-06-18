
import requests
import math


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


def find_nearby_hospitals(lat, lon):

    try:

        headers = {
            "User-Agent": "AI-FirstAid-App"
        }

        # Get user's city/state from coordinates
        reverse_url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lon}&format=json"
        )

        reverse_response = requests.get(
            reverse_url,
            headers=headers,
            timeout=20
        )

        location_data = reverse_response.json()

        address = location_data.get("address", {})

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("county")
            or ""
        )

        state = address.get("state", "")

        search_query = f"hospital in {city} {state}"

        search_url = (
            "https://nominatim.openstreetmap.org/search"
            f"?q={search_query}"
            "&format=jsonv2"
            "&limit=15"
        )

        response = requests.get(
            search_url,
            headers=headers,
            timeout=20
        )

        data = response.json()

        hospitals = []

        for item in data:

            hlat = float(item["lat"])
            hlon = float(item["lon"])

            distance = calculate_distance(
                lat,
                lon,
                hlat,
                hlon
            )

            hospitals.append({
                "name": item.get(
                    "display_name",
                    "Hospital"
                ),
                "distance": round(distance, 2),
                "maps": (
                    f"https://www.google.com/maps/dir/"
                    f"{lat},{lon}/{hlat},{hlon}"
                )
            })

        hospitals.sort(
            key=lambda x: x["distance"]
        )

        print("Detected City:", city)
        print("Detected State:", state)
        print("Hospitals Found:", len(hospitals))

        return hospitals[:10]

    except Exception as e:

        print("Hospital Finder Error:", e)

        return []
