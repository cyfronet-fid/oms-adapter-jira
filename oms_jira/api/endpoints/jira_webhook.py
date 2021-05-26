"""Triggers for JIRA OMS adapter from JIRA side"""
from functools import wraps

from flask import request, current_app
from flask_restx import Resource, Namespace

from oms_jira.tasks.jira import process_jira_webhook

api = Namespace("api/webhooks", "Endpoint called by JIRA when something changes")


def secret_required(func):
    """
    Ensure that only call with `secret` authorization is passed through
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.args.get("secret") != current_app.config.get("JIRA_CONFIG").webhook_secret:
            return None, 401
        return func(*args, **kwargs)

    return wrapper


@api.route("/jira")
class JIRAWebhook(Resource):
    """Triggers data load"""

    @api.response(204, "Webhook received")
    @api.response(401, "Authorization error")
    @secret_required
    def post(self):
        data: dict = request.json
        query: dict = request.args
        issue_id = int(query.get("issue_id")) if query.get("issue_id") else None

        process_jira_webhook.delay(issue_id, data)

        return None, 204
