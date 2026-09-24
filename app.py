from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import urllib.request
import urllib.parse
import json
import random

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def home():
    return send_from_directory('.', 'invitation-generator.html')

@app.route('/')
def serve_files(path):
    return send_from_directory('.', path)

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json() or {}
    long_url = data.get('url')
    groom = data.get('groom', 'Groom').strip().replace(' ', '')
    bride = data.get('bride', 'Bride').strip().replace(' ', '')

    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    alias = f"{groom}-{bride}-Wedding"
    
    # 1. Mo7awla TinyURL ma3 User-Agent sari3
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}&alias={urllib.parse.quote(alias)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=4) as response:
            res = response.read().decode('utf-8').strip()
            if res.startswith('http'):
                return jsonify({'shortUrl': res})
    except Exception:
        pass

    # 2. Mo7awla TinyURL b-raqam 3ashwa2y lw el-esm ma7gooz
    try:
        rand_id = random.randint(10, 99)
        alias_fallback = f"{groom}-{bride}-Wedding-{rand_id}"
        api_url2 = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}&alias={urllib.parse.quote(alias_fallback)}"
        req2 = urllib.request.Request(api_url2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req2, timeout=4) as response:
            res2 = response.read().decode('utf-8').strip()
            if res2.startswith('http'):
                return jsonify({'shortUrl': res2})
    except Exception:
        pass

    # 3. Badil sari3 gedan via CleanURI (msh byet2efer f Masr)
    try:
        clean_url = "https://cleanuri.com/api/v1/shorten"
        payload = urllib.parse.urlencode({'url': long_url}).encode('utf-8')
        req3 = urllib.request.Request(clean_url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req3, timeout=4) as response:
            json_res = json.loads(response.read().decode('utf-8'))
            if json_res and 'result_url' in json_res:
                return jsonify({'shortUrl': json_res['result_url']})
    except Exception:
        pass

    return jsonify({'shortUrl': long_url})

if __name__ == '__main__':
    print("🚀 Wedding Shortener running on port 5000...")
    app.run(port=5000, debug=True)