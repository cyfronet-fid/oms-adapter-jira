"""Celery factory"""

from oms_jira import init_celery, init_sentry_celery

init_sentry_celery()

app = init_celery()
app.conf.imports = app.conf.imports + (
    "oms_jira.tasks",
)
