from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import urllib.parse

app = Flask(__name__)
# السماح للواجهة بالاتصال بالباك إند بدون مشاكل
CORS(app)

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get('url')
    groom = data.get('groom', 'groom')
    bride = data.get('bride', 'bride')

    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    alias = f"{groom.strip()}-{bride.strip()}-wedding".replace(" ", "-")

    try:
        # الاتصال بـ TinyURL مباشرة من السيرفر (بدون قيود متصفح)
        api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}&alias={urllib.parse.quote(alias)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            short_url = response.read().decode('utf-8').strip()
            return jsonify({'shortUrl': short_url})
    except Exception:
        try:
            # لو الاسم محجوز، اختصار عادي برقم عشوائي
            api_url_fallback = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
            req = urllib.request.Request(api_url_fallback, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                short_url = response.read().decode('utf-8').strip()
                return jsonify({'shortUrl': short_url})
        except Exception as e:
            return jsonify({'shortUrl': long_url, 'error': str(e)}), 200

if __name__ == '__main__':
    print("🚀 Wedding Shortener Backend is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)