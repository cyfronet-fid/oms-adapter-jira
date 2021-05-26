import pytest

from oms_jira.tasks.mp import process_mp_trigger


@pytest.mark.celery_app
@pytest.mark.celery_worker
class TestMPTask:
    def test_sanity(self, flask_app, db_session):
        process_mp_trigger()
