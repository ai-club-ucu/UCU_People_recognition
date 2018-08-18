from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from modules.VideoProcessor import VideoProcessor
import pymysql.cursors
import threading
import sys
import cv2

app = Flask(__name__)

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="",
                             db="dvd_collection",
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)

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


def stats(proc):
    grabbed, frame = proc.get_next_frame()
    n = 1
    print("started")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO dvd_collection.table1 (`x`, `y`) VALUES (%s, %s)"
            while grabbed:
                proc.time_change(n, proc.stream.get(cv2.CAP_PROP_POS_MSEC))
                if n % 220 == 0:
                    proc.make_heatmap(frame, n)
                else:
                    proc.make_heatmap(frame)
                print("my if statement")
                if n % proc.stream.get(cv2.CAP_PROP_FPS) == 0:
                    print(n)
                    x = float(sum(proc.graph_data))
                    proc.graph_data.clear()
                    y = round(float(sum(proc.time)), 9)
                    proc.time.clear()
                    print(x, type(x), y, type(y))
                    cursor.execute(sql, (x, y))
                # self.process_frame(frame, preview=True, crop=False)
                # cv2.imshow("frame", frame)
                grabbed, frame = proc.get_next_frame()
                n += 1
        connection.commit()
    finally:
        connection.close()



if __name__ == '__main__':
    app.run(debug=True)