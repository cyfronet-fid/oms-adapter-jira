import factory

from oms_jira import db
from oms_jira.models import Project
from oms_jira.models.mapping import ProjectItem, Comment


class MP2JIRAMappableFactory(factory.alchemy.SQLAlchemyModelFactory):
    mp_id = factory.Sequence(lambda n: n + 1)
    jira_id = factory.Sequence(lambda n: n + 1)


class ProjectFactory(MP2JIRAMappableFactory):
    class Meta:
        model = Project
        sqlalchemy_session = db.session


class ProjectItemFactory(MP2JIRAMappableFactory):
    class Meta:
        model = ProjectItem
        sqlalchemy_session = db.session


class CommentFactory(MP2JIRAMappableFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = db.session
