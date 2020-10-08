from flask import Flask, render_template, Response
import socket, cv2, pickle, struct
import time

app = Flask(__name__)


def captureVideo():
    capture = cv2.VideoCapture(0)
    # Read until the video is completed
    # Once we switch to Rtsp it will go forever (Technically)
    while True:
        # Capture Frame by Frame:
        ret, image = capture.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat


@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(captureVideo(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/about")
def about():
    return "<h1> About Page </h1>"


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
