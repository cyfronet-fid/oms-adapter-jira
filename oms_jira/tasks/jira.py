from typing import Type, Optional

from oms_jira import db
from oms_jira.extensions import celery
from oms_jira.models import MP2JIRAMappable, ProjectItem, Project, Comment
from oms_jira.services.jira import update_issue_jira2mp, create_comment_jira2mp, update_comment_jira2mp
from oms_jira.tasks.common import singleton_task


@celery.task(autoretry_for=(Exception, ))
def process_jira_webhook(issue_id: Optional[int], data: dict):
    if issue_id is None:
        return

    webhook_event = data.get("webhookEvent")
    element_updated = _find_jira_item(ProjectItem, issue_id) or _find_jira_item(Project, issue_id)

    if element_updated:
        if webhook_event == "jira:issue_updated":
            update_issue_jira2mp(element_updated, data.get("changelog"))
        elif webhook_event == "comment_created":
            create_comment_jira2mp(element_updated, data.get("comment"))
        elif webhook_event == "comment_updated":
            comment = db.session.query(Comment).filter_by(jira_id=data.get("comment").get("id"))
            update_comment_jira2mp(comment.mp_id, data.get("comment").get("body"))
        else:  # webhook event not supported
            pass


def _find_jira_item(clazz: Type[MP2JIRAMappable], jira_id: int):
    return db.session.query(clazz).filter_by(jira_id=jira_id).first()
