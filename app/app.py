from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from modules.VideoProcessor import VideoProcessor

app = Flask(__name__)


@app.route('/')
def upload_file_render():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        processor = VideoProcessor('app/{}'.format(f.filename))
        return stats()

@app.route('/uploader/statistic')
def stats():
    return "statistic"



if __name__ == '__main__':
    app.run(debug=True)