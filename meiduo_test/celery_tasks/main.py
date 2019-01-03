import os

from celery import Celery

# 设置Django运行所依赖的环境
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_test.settings.dev'

# 创建celery 应用
celery_app = Celery("celery_tasks")

# 导入celery配置
# celery_app.config_from_object("celery_tasks_config")
celery_app.config_from_object('celery_tasks.config')


# 自动注册celery任务
celery_app.autodiscover_tasks(["celery_tasks.sms", "celery_tasks.email"])
