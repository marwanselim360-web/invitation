from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import urllib.parse
import json
import random

app = Flask(__name__)
CORS(app)

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json() or {}
    long_url = data.get('url')
    groom = data.get('groom', 'Groom').strip().replace(' ', '')
    bride = data.get('bride', 'Bride').strip().replace(' ', '')

    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    # محاولة إنشاء الرابط بالاسم المباشر
    desired_alias = f"{groom}-{bride}-Wedding"
    
    # 1. التجربة الأولى بالاسم الملكي المباشر
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}&alias={urllib.parse.quote(desired_alias)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as response:
            short_url = response.read().decode('utf-8').strip()
            if short_url.startswith('http'):
                return jsonify({'shortUrl': short_url})
    except Exception:
        pass

    # 2. في حال كان الاسم محجوزاً، يضاف رقم خفيف للحفاظ على الاسم
    try:
        rand_suffix = random.randint(10, 99)
        fallback_alias = f"{groom}-{bride}-Wedding-{rand_suffix}"
        api_url2 = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}&alias={urllib.parse.quote(fallback_alias)}"
        req2 = urllib.request.Request(api_url2, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req2, timeout=6) as response:
            short_url2 = response.read().decode('utf-8').strip()
            if short_url2.startswith('http'):
                return jsonify({'shortUrl': short_url2})
    except Exception:
        pass

    return jsonify({'shortUrl': long_url})

if __name__ == '__main__':
    print("🚀 Wedding Shortener running on port 5000")
    app.run(port=5000, debug=True)