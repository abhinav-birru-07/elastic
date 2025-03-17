import requests
import json

# Assuming you have access to auth.currentUser.uid in Python (replace accordingly)
USER_ID = "F4pStlKJQpg2Pz4R7S0vsg4HSAX2"  # Replace with actual user ID retrieval method


def send_request():
    url = "http://127.0.0.1:5000/get_my_prod"  # Replace with your actual endpoint URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "useRef": USER_ID
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)


send_request()