from flask import Flask, render_template, request, make_response, url_for, redirect
from werkzeug.utils import secure_filename
from modules.VideoProcessor import VideoProcessor
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import modules.sql_worker as sql_worker
import pymysql.cursors
import threading
import sys
import cv2
import io


app = Flask(__name__)

connection = sql_worker.creat_local_connection()

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
    x = []
    y = []
    print("started")
    sql_worker.drop_table('table2', connection)
    sql_worker.create_table('table2', connection)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO table2 (`x`, `y`) VALUES (%s, %s)"
            while grabbed:
                proc.time_change(n, proc.stream.get(cv2.CAP_PROP_POS_MSEC))
                if n % 220 == 0:
                    proc.make_heatmap(frame, n)
                else:
                    proc.make_heatmap(frame)
                print("my if statement")
                if n % proc.stream.get(cv2.CAP_PROP_FPS) == 0:
                    print(n)
                    x.append(float(sum(proc.graph_data)))
                    proc.graph_data.clear()
                    y.append(round(float(sum(proc.time)), 9))
                    #next lines for the future dynamic plot
                    # print(x, type(x), y, type(y))
                    # cursor.execute(sql, (x, y))
                grabbed, frame = proc.get_next_frame()
                n += 1
        connection.commit()
    finally:
        connection.close()
    return plot(x, y)


def plot(y, x):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y)
    canvas = FigureCanvas(fig)
    output = io.StringIO()
    fig.savefig("static/graph.png")
    return redirect(url_for('static', filename='graph.png'))

if __name__ == '__main__':
    app.run(debug=True)