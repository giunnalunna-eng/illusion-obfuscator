from flask import Flask, render_template, request, jsonify
import requests
import time
from obfuscator import obfuscate_code

app = Flask(__name__)

# Memoria temporanea per le esecuzioni dei giocatori
execution_logs = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def handle_obfuscate():
    try:
        data = request.json
        source = data.get('code', '')
        strength = int(data.get('strength', 5))
        script_name = data.get('name', 'Untitled')
        use_pastefy = data.get('use_pastefy', False)
        
        result = obfuscate_code(source, strength)
        if not result['success']:
            return jsonify({"success": False, "error": result['error']})

        obf_code = result['code']

        if use_pastefy:
            r = requests.post("https://api.pastefy.app/v2/item", json={
                "title": script_name,
                "content": obf_code,
                "type": "PASTE"
            })
            if r.status_code == 200:
                url = f"https://pastefy.app/{r.json()['item']['id']}/raw"
                return jsonify({"success": True, "code": f'loadstring(game:HttpGet("{url}"))()', "is_pastefy": True})
            else:
                return jsonify({"success": False, "error": "Pastefy Error"})

        return jsonify({"success": True, "code": obf_code, "is_pastefy": False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/log_execution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        player_name = data.get('player', 'Unknown')
        script_id = data.get('script_id', 'Unknown')
        execution_logs.insert(0, {
            "player": player_name,
            "script": script_id,
            "time": time.strftime("%H:%M:%S")
        })
        if len(execution_logs) > 50: execution_logs.pop()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify(execution_logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
