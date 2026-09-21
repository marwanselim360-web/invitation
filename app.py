from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# المجلد الحالي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# فتح الدعوة مباشرة بالرابط
@app.route('/invite')
def serve_invite():
    return send_from_directory(BASE_DIR, 'invite.html')

# تشغيل الأغنية وصور العروسين
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    # تشغيل السيرفر على بورت 5000
    app.run(host='0.0.0.0', port=5000, debug=True)