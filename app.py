from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        ydl_opts = {
            'format': 'b',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Get direct stream URL
            video_url = info.get('url')
            if not video_url:
                # Try formats list
                formats = info.get('formats', [])
                for f in reversed(formats):
                    if f.get('url'):
                        video_url = f['url']
                        break

            if not video_url:
                return jsonify({'error': 'Could not extract download URL'}), 500

            return jsonify({
                'success': True,
                'download_url': video_url,
                'filename': f"{info.get('title', 'video')}.mp4"
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

