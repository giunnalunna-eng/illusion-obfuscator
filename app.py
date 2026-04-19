from flask import Flask, render_template, request, jsonify
from obfuscator import obfuscate_code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def handle_obfuscate():
    data = request.json
    result = obfuscate_code(data.get('code', ''), 5)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
