from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from modules.VideoProcessor import VideoProcessor
import cv2

app = Flask(__name__)

@app.route('/')
def upload_file_render():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        proc= VideoProcessor('{}'.format(f.filename))
        return stats(proc)

@app.route('/uploader/statistic')
def stats(proc):
    grabbed, frame = proc.get_next_frame()
    n = 0
    while grabbed:
        proc.time_change(n, proc.stream.get(cv2.CAP_PROP_POS_MSEC))
        if n % 220 == 0:
            proc.make_heatmap(frame, n)
        else:
            proc.make_heatmap(frame)
        # self.process_frame(frame, preview=True, crop=False)
        # cv2.imshow("frame", frame)
        grabbed, frame = proc.get_next_frame()
        n += 1
        if n == 1000:
            break
    return render_template('chart.html', values=proc.graph_data, labels=proc.time)



if __name__ == '__main__':
    app.run(debug=True)