from celery import Celery
import redis
import os

app = Celery('tasks')
app.config_from_object("celeryconfig", force=True)


class CommandFailedException(Exception):
        pass

def exec_shell(cmd):
    status = os.system(cmd)
    if status != 0:
        raise CommandFailedException("{cmd} terminated with status code{statusCode}".format(statusCode=status, cmd=cmd))


@app.task(bind=True, autoretry_for=(CommandFailedException,), retry_backoff=2,max_retries=1)
def convert_video(self, video_id, scale):
        exec_shell(
                "ffmpeg -y -i static/video/{video_id} -vf scale=-2:{scale} -c:v libx264  -preset ultrafast  -c:a copy static/video/temp/{video_id}.{scale}.mp4".format(
                video_id=video_id, scale=scale))
        exec_shell('mv static/video/temp/{video_id}.{scale}.mp4 static/video/{video_id}.{scale}'.format(
                video_id=video_id, scale=scale))


@app.task()
def generate_thumbnail(video_id):
    exec_shell("ffmpeg -y -i static/video/{video_id} -ss 00:00:00.00 -vframes 1 static/img/{video_id}.png".format(
        video_id=video_id))
