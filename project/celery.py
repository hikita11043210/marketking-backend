import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Windows環境での設定
app.conf.update(
    broker_connection_retry_on_startup=True,
    worker_pool_restarts=True,
    task_track_started=True,
    worker_max_tasks_per_child=1,  # メモリリークを防ぐ
    worker_pool='solo'  # Windowsでの問題を回避
)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
