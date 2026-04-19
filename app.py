from flask import Flask, render_template, request, jsonify
import requests
from obfuscator import obfuscate_code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def handle_obfuscate():
    try:
        data = request.json
        source = data.get('code', '')
        strength = int(data.get('strength', 5))
        script_name = data.get('name', 'Illusion Script')
        use_pastefy = data.get('use_pastefy', False)
        
        # Offuscamento con Motore Abyssal VM v9.0
        result = obfuscate_code(source, strength)
        if not result['success']:
            return jsonify({"success": False, "error": result['error']})

        obfuscated_code = result['code']

        if use_pastefy:
            try:
                r = requests.post("https://api.pastefy.app/v2/item", json={
                    "title": script_name,
                    "content": obfuscated_code,
                    "type": "PASTE"
                })
                if r.status_code == 200:
                    url = f"https://pastefy.app/{r.json()['item']['id']}/raw"
                    return jsonify({"success": True, "code": f'loadstring(game:HttpGet("{url}"))()', "is_pastefy": True})
                else:
                    return jsonify({"success": False, "error": "Pastefy API Error"})
            except:
                return jsonify({"success": False, "error": "Failed to connect to Pastefy"})

        return jsonify({"success": True, "code": obfuscated_code, "is_pastefy": False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
