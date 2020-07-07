from flask import Flask, render_template, Response, request
from tracker import Tracker
import json

app = Flask(__name__, static_folder='static')
tracker = Tracker("static/tennis.mp4")
count = 0

@app.route('/')
def root():
    print(tracker.fps)
    data = {
        "fps": tracker.fps
    }    
    return render_template('index.html', data=data)

@app.route('/analysis', methods=['POST'])
def video_feed():
    global count
    pos = json.loads(request.form["pos"])
    tracker.analyze_frame(pos["frame"], pos["x"], pos["y"])
    count += 1
    if count > 2:
        print(tracker.calcSpeed()) 
    return "OK"


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)