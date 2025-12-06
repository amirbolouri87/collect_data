import multiprocessing
import subprocess
from config.settings.integrations_config import GunicornConfig


workers = multiprocessing.cpu_count() * 2 + 1

subprocess.run(["python", "manage.py", "migrate", "--no-input"], check=True)

subprocess.run(["python", "manage.py", "collectstatic", "--no-input"], check=True)

if GunicornConfig.is_production() or GunicornConfig.is_staging():
    subprocess.run(
        [
            "gunicorn",
            f"--timeout={GunicornConfig.GUNICORN_TIMEOUT}",
            "-w", str(workers),
            "config.wsgi:application",
            "-b", f"{GunicornConfig.GUNICORN_HOST}:{GunicornConfig.GUNICORN_PORT}",
            ],
        check=True,
    )
else:
    subprocess.run(
        ["python", "manage.py", "runserver", f"{GunicornConfig.GUNICORN_HOST}:{GunicornConfig.GUNICORN_PORT}"],
        check=True
    )
