import sys
import os
import subprocess
from flask import Flask, render_template, request, jsonify

print("Flask is running with:", sys.executable)

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-task", methods=["POST"])
def run_task():
    data = request.get_json()
    user_id = data.get("user_id", "")

    if len(user_id) >= 2:
        script_path = os.path.join(os.path.dirname(__file__), "react-python.py")

        if not os.path.exists(script_path):
            return jsonify({"status": "error", "message": f"Script not found: {script_path}"})

        log_file = os.path.join(os.path.dirname(__file__), "react_log.txt")

        try:
            # ✅ Use the current Python executable (works on local + Render)
            with open(log_file, "w") as f:
                subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=f,
                    stderr=f
                )

            return jsonify({
                "status": "success",
                "message": f"Task executed! Check {log_file} for logs"
            })

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    return jsonify({"status": "ignored", "message": "Need at least 2 characters"})


# Example second endpoint
@app.route("/run-script", methods=["POST"])
def run_script():
    data = request.get_json()
    login_id = data.get("loginId", "")
    return jsonify({"status": "ok", "received": login_id})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
