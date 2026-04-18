from flask import Flask, render_template, request, jsonify
import os
import sys
import webbrowser
from obfuscator import obfuscate_code
import json
from datetime import datetime
import uuid

# Configuration
PORT = 5000
app = Flask(__name__)

# In-memory storage for logs (for real-time viewing)
# In a real app, you'd fetch this from Supabase
execution_logs = []
obfuscation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def handle_obfuscate():
    try:
        data = request.json
        source = data.get('code', '')
        strength = data.get('strength', 5)
        custom_url = data.get('custom_url', '')
        
        if not source:
            return jsonify({"success": False, "error": "No code provided"})
            
        result = obfuscate_code(source, strength, custom_url)
        
        if result['success']:
            # Store in history
            script_id = str(uuid.uuid4())[:8]
            entry = {
                "id": script_id,
                "name": f"Script_{script_id}",
                "original": source,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Completed"
            }
            obfuscation_history.insert(0, entry)
            result['script_id'] = script_id
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify(obfuscation_history)

@app.route('/log_execution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        # This endpoint is called by the obfuscated script
        log_entry = {
            "player": data.get('player', 'Unknown'),
            "script_id": data.get('script_id', 'Unknown'),
            "time": datetime.now().strftime("%H:%M:%S")
        }
        execution_logs.insert(0, log_entry)
        return jsonify({"status": "logged"})
    except:
        return jsonify({"status": "error"})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify(execution_logs[:20]) # Return last 20 logs

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open(f'http://localhost:{PORT}')
    app.run(port=PORT, debug=False)
