from flask import Flask, render_template, Response, request
from tracker import Tracker

app = Flask(__name__, static_folder='static')
tracker = Tracker("tennis.mp4")

@app.route('/')
def root():    
    return render_template('index.html', frames=tracker.frames)

def gen():
    while True:
        frame = tracker.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    print(request.form["frameNum"])
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)