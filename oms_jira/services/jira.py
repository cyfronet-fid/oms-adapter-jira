import typing

from flask import Flask, current_app
from jira import JIRA

from oms_jira import db
from oms_jira.models import ProjectItem, Comment, Project, MP2JIRAMappable
from oms_jira.services.mp import (
    get_mp_client,
    ProjectItemStatusEnum,
    MPMessage,
    MessageAuthor,
    ScopeEnum, Event,
)
from settings import JIRAConfig


class JiraClient:
    def __init__(self, app: Flask) -> None:
        self.config: JIRAConfig = app.config.get("JIRA_CONFIG")
        self.mp_client = get_mp_client()
        self.client = JIRA(
            self.config.url,
            basic_auth=(self.config.username, self.config.password),
        )

    def execute_event(self, event: Event):
        if event.resource == Event.ResourceEnum.project:
            self._handle_project_event(event)
        elif event.resource == Event.ResourceEnum.project_item:
            self._handle_project_item_event(event)
        elif event.resource == Event.ResourceEnum.message:
            self._handle_message_event(event)

    def _handle_project_event(self, event: Event):
        if event.type == Event.TypeEnum.create:
            project_source = self.mp_client.get_project(event.project_id)
            project_jira = self.client.create_issue(fields=project_source.jira_fields(self.config))

            db.session.add(Project(mp_id=event.project_id, jira_id=project_jira.id))
            db.session.flush()

        elif event.type == Event.TypeEnum.update:
            project_source = self.mp_client.get_project(event.project_id)
            jira_id = db.session.query(ProjectItem).filter_by(mp_id=event.project_id).first().jira_id
            self.client.issue(jira_id).update(fields=project_source.jira_fields(self.config))

    def _handle_project_item_event(self, event: Event):
        if event.type == Event.TypeEnum.create:
            project_item_source = self.mp_client.get_project_item(event.project_id, event.project_item_id)
            project_key = self.client.issue(db.session.query(Project).filter_by(mp_id=event.project_id).first().jira_id).key
            project_item_jira = self.client.create_issue(project_item_source.jira_fields(self.config, project_key))

            db.session.add(ProjectItem(jira_id=project_item_jira.id, mp_id=event.project_item_id))
            db.session.flush()

        elif event.type == Event.TypeEnum.update:
            project_item_source = self.mp_client.get_project_item(event.project_id, event.project_item_id)
            project_item = db.session.query(ProjectItem).filter_by(project_id=event.project_id, mp_id=event.project_item_id)

    def _handle_message_event(self, event: Event):
        if event.type == Event.TypeEnum.create:
            issue_id = None
            comment = None

            if event.project_id is not None:
                issue_id = db.session.query(Project).filter_by(mp_id=event.project_id).first().jira_id
                comment = Comment(parent_type=Comment.CommentType.Project, parent_id=event.project_id)
            elif event.project_item_id is not None:
                issue_id = db.session.query(ProjectItem).filter_by(mp_id=event.project_item_id).first().jira_id
                comment = Comment(parent_type=Comment.CommentType.ProjectItem, parent_id=event.project_item_id)

            comment.mp_id = event.message_id

            jira_comment = self.client.add_comment(issue_id, self.mp_client.get_message(event.message_id).content)
            comment.jira_id = jira_comment.id

            db.session.add(comment)
            db.session.flush()


def get_jira_client() -> JiraClient:
    return JiraClient(current_app)


def update_issue_jira2mp(project_item: ProjectItem, changelog: dict):
    mp_client = get_mp_client()
    for change in changelog.get("items", []):
        status = None
        if change.get("field") == "status":
            to = int(change.get("to"))
            workflow = current_app.config.get("JIRA_CONFIG").workflow
            if to == workflow.get("rejected"):
                status = ProjectItemStatusEnum.rejected
            elif to == workflow.get("waiting_for_response"):
                status = ProjectItemStatusEnum.waiting_for_response
            elif to == workflow.get("todo"):
                status = ProjectItemStatusEnum.registered
            elif to == workflow.get("in_progress"):
                status = ProjectItemStatusEnum.in_progress
            elif to == workflow.get("ready"):
                status = ProjectItemStatusEnum.ready
            elif to == workflow.get("closed"):
                status = ProjectItemStatusEnum.closed
            elif to == workflow.get("approved"):
                status = ProjectItemStatusEnum.approved
            else:  # unknown issue type
                pass
        mp_client.update_project_item(project_item.project_id, project_item.id, status)


def create_comment_jira2mp(owner: typing.Union[ProjectItem, Project], data: dict):
    jira_config = get_jira_client().config
    mp_client = get_mp_client()
    if not data or data.get("author").get("name") != jira_config.username:
        return

    content = data.get("body")

    project_id = None
    project_item_id = None

    if isinstance(owner, Project):
        project_id = owner.mp_id
    elif isinstance(owner, ProjectItem):
        project_item_id = owner.mp_id
    else:
        raise ValueError(f"{repr(owner)} is not a Project or ProjectItem")

    mp_client.create_message(
        MPMessage(
            project_id=project_id,
            project_item_id=project_item_id,
            content=content,
            scope=ScopeEnum.public,
        )
    )


def update_comment_jira2mp(comment_id: int, message_content: str):
    mp_client = get_mp_client()
    mp_client.update_message(comment_id, message_content)
