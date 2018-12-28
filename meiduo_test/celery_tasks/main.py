from celery import Celery

# 创建celery 应用
celery_app = Celery("celery_tasks")

# 导入celery配置
# celery_app.config_from_object("celery_tasks_config")
celery_app.config_from_object('celery_tasks.config')


# 自动注册celery任务
celery_app.autodiscover_tasks(["celery_tasks.sms"])
