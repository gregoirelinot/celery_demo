import os
from flask import Flask, render_template, jsonify, redirect, url_for, request, send_from_directory
import random
import string
from worker import convert_video, generate_thumbnail
from celery import group


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='', template_folder='')

resolutions = [144, 240, 360, 720, 1080]

def randomId():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)


def getVideoById(video_id):
    return list(filter(lambda x: x.split('.')[0] == video_id, os.listdir('static/video/')))


def getAllVideo():
    return os.listdir('static/img')


@app.route('/watch')
def videoWatch():
    id = request.args.get('q')
    return render_template('static/watch.html', videos=getVideoById(id))


@app.route('/all')
def allVideo():
    return render_template('static/index.html', video_img=getAllVideo())


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            video_id = randomId()

            filename = os.path.join("static/video", video_id)
            file.save(filename)

            generate_thumbnail.apply_async((video_id,),queue='priority.high')

            group(convert_video.s(video_id,resolution) for resolution in resolutions).delay()
            return redirect('/watch?q={}'.format(video_id))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
