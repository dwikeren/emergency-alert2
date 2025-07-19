from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

app = Flask(__name__)
CORS(app)

# Setup Firebase credentials
SERVICE_ACCOUNT_FILE = 'emergencyalert-c61a1-firebase-adminsdk-fbsvc-d2e7ae9cdf.json'
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

@app.route("/")
def home():
    return "API Siap!"

@app.route("/kirim-alert", methods=["POST"])
def kirim_alert():
    try:
        data = request.get_json()
        bandara = data.get("bandara", "")
        level = data.get("level", "")

        credentials.refresh(Request())
        access_token = credentials.token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; UTF-8",
        }

        project_id = credentials.project_id
        url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

        message = {
            "message": {
                "topic": bandara,
                "data": {
                    "level": level,
                    "bandara": bandara
                }
            }
        }

        res = requests.post(url, headers=headers, data=json.dumps(message))
        return jsonify({"success": True, "status_code": res.status_code, "response": res.json()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ⚠️ Bagian ini dihapus untuk production
# Railway akan menjalankan Gunicorn, bukan Flask dev server
# if __name__ == "__main__":
#     app.run(debug=False, port=5000, host="0.0.0.0")
