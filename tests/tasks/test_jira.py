import pytest

from oms_jira.tasks.jira import process_jira_webhook


@pytest.mark.celery_app
@pytest.mark.celery_worker
class TestJiraTask:
    def test_sanity(self, flask_app):
        task = process_jira_webhook.delay()
        task.wait(timeout=None, interval=0.5)
