from flask import Flask, render_template, request, jsonify
from spotify_downloader import download_single_url, check_dependencies

app = Flask(__name__)

# Run checks on startup
try:
    check_dependencies()
except SystemExit:
    print("Dependencies failed. Please fix before running app.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400
        
    success, message = download_single_url(url)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
