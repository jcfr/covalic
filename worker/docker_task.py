from .celery import app, config
from . import job_util, utils


@app.task(name='docker_task', bind=True)
@job_util.task(logPrint=True, progress=True)
def docker_task(*args, **kwargs):
    # TODO call the container with any args passed in docker_container.args
    # If non-zero return code, raise exception. If zero rc, send stdout (or
    # expected output file) to whatever URL is specified in output.
    pass
