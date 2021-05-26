"""Models for the MP endpoints"""

from flask_restx import fields

from .common import api


mapping = api.model(
    "MP to JIRA mapping", {"mp_id": fields.Integer(), "jira_id": fields.Integer()}
)
