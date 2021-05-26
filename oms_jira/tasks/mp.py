from oms_jira import db
from oms_jira.extensions import celery
from oms_jira.models import Bookkeeping
from oms_jira.services.jira import get_jira_client
from oms_jira.services.mp import get_mp_client
from oms_jira.tasks.common import singleton_task
from oms_jira.models.mapping import ProjectItem
import json


@celery.task(autoretry_for=(Exception, ))
@singleton_task
def process_mp_trigger():
    """Process mp changes and inform JIRA about it"""

    mp_client = get_mp_client()
    jira_client = get_jira_client()
    bookkeeping: Bookkeeping = db.session.query(Bookkeeping).first()
    last_timestamp = bookkeeping.last_event_timestamp
    for event in mp_client.list_events(last_timestamp):
        print(event)
        jira_client.execute_event(event)
        bookkeeping.last_event_timestamp = event.timestamp
        db.session.commit()