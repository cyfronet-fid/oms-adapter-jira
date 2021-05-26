# pylint: disable-all

import json
from typing import Callable

import pytest

from tests.factories.jira_webhook import JiraWebhookRequestFactory
from tests.factories.mapping import ProjectFactory


@pytest.fixture
def jira_webhook_caller(client) -> Callable:
    def call(data: dict = None, query_string: dict = None):
        data = JiraWebhookRequestFactory() if data is None else data
        return client.post(
            "/api/webhooks/jira",
            json=data,
            query_string={
                "secret": "12345678",
                "issue_id": data.get("issue_id"),
                "user_id": data.get("user").get("name"),
                "user_key": data.get("user").get("key"),
            }
            if query_string is None
            else query_string,
        )

    return call


class TestJiraWebhook:
    def test_sanity(self, jira_webhook_caller):
        response = jira_webhook_caller()
        assert response.status_code == 204

    def test_access_denied(self, jira_webhook_caller):
        response = jira_webhook_caller(query_string={"secret": "1234"})
        assert response.status_code == 401

    def test_issue_created(self, jira_webhook_caller):
        jira_id = 0
        ProjectFactory(jira_id=jira_id)
        jira_webhook_caller(data=JiraWebhookRequestFactory(id=jira_id))
