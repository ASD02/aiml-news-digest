from flask import Flask, request
import threading
import subprocess

app = Flask(__name__)

SLACK_SIGNING_SECRET = "your-slack-signing-secret"  # from api.slack.com/apps

@app.route("/slack/digest", methods=["POST"])
def slash_command():
    # Respond immediately (Slack requires <3s)
    threading.Thread(target=lambda: subprocess.run(["python", "run_digest.py"])).start()
    return "Starting digest... results will post to channels shortly. ⏳", 200

if __name__ == "__main__":
    app.run(port=3000)
