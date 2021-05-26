import enum

from ..extensions import db


class MP2JIRAMappable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mp_id = db.Column(db.Integer, nullable=False)
    jira_id = db.Column(db.Integer, unique=True, nullable=False)

    __abstract__ = True


class Project(MP2JIRAMappable):
    def __repr__(self):
        return f"<Project {self.id}:{self.mp_id}:{self.jira_id}>"


class ProjectItem(MP2JIRAMappable):
    project_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<ProjectItem {self.id}:{self.mp_id}:{self.jira_id}>"


class Comment(MP2JIRAMappable):
    class CommentType(enum.Enum):
        Project = "Project"
        ProjectItem = "ProjectItem"

    parent_type = db.Column(db.Enum(CommentType))
    parent_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}:{self.mp_id}:{self.jira_id} (parent_type: {self.parent_type})>"
