import datetime

import pytest
from flask import Flask

from oms_jira.services.mp import MPClient, get_mp_client, MPMessage


@pytest.mark.vcr
class TestMPClient:
    project_id = 1436
    project_item_id = 1
    message_id = 659

    @pytest.fixture()
    def mp_client(self, flask_app: Flask) -> MPClient:
        return get_mp_client()

    def test_oms_list(self, mp_client: MPClient):
        assert mp_client.list_oms() == {
            "omses": [
                {
                    "id": 1,
                    "name": "SOMBO",
                    "type": "global",
                    "default": True,
                    "trigger_url": "http://127.0.0.1:9000/oms/trugger",
                    "custom_params": {"order_target": {"mandatory": False}},
                }
            ]
        }

    def test_oms(self, mp_client: MPClient):
        assert mp_client.get_oms() == {
            "custom_params": {"order_target": {"mandatory": False}},
            "default": True,
            "id": 1,
            "name": "SOMBO",
            "trigger_url": "http://127.0.0.1:9000/oms/trugger",
            "type": "global",
        }

    def test_list_events(self, mp_client: MPClient):
        assert mp_client.list_events(
            from_timestamp=datetime.datetime.fromisoformat("2021-05-25 21:01:45")
        ) == {
            "events": [
                {
                    "timestamp": "2021-05-25T21:07:42Z",
                    "type": "create",
                    "resource": "project_item",
                    "project_id": 1436,
                    "project_item_id": 3,
                },
                {
                    "timestamp": "2021-05-25T21:07:44Z",
                    "type": "update",
                    "resource": "project_item",
                    "changes": [
                        {"after": "ready", "field": "status.type", "before": "created"},
                        {
                            "after": "ready",
                            "field": "status.value",
                            "before": "created",
                        },
                    ],
                    "project_id": 1436,
                    "project_item_id": 3,
                },
            ]
        }

    def test_list_project(self, mp_client: MPClient):
        assert mp_client.list_project() == {
            "projects": [
                {
                    "id": 1436,
                    "owner": {"email": "email@domain", "name": "John Doe"},
                    "project_items": [1, 2, 3],
                    "attributes": {
                        "name": "Sample project",
                        "customer_typology": "single_user",
                        "organization": "CYF",
                        "department": "",
                        "department_webpage": "http://cyfronet.pl",
                        "scientific_domains": ["Aerospace Engineering"],
                        "country": "Poland",
                        "collaboration_countries": [],
                        "user_group_name": "",
                    },
                },
            ]
        }

    def test_get_project(self, mp_client: MPClient):
        assert mp_client.get_project(self.project_id) == {
            "attributes": {
                "collaboration_countries": [],
                "country": "Poland",
                "customer_typology": "single_user",
                "department": "",
                "department_webpage": "http://cyfronet.pl",
                "name": "Sample project",
                "organization": "CYF",
                "scientific_domains": ["Aerospace Engineering"],
                "user_group_name": "",
            },
            "id": 1436,
            "owner": {"email": "email@domain", "name": "John Doe"},
            "project_items": [1, 2, 3],
        }

    def test_list_message(self, mp_client: MPClient):
        assert mp_client.list_message(self.project_id, self.project_item_id) == {
            "messages": [
                {
                    "author": {
                        "email": "email@domain",
                        "name": "John Doe",
                        "role": "user",
                    },
                    "content": "Sample message",
                    "created_at": "2021-05-25T23:21:24Z",
                    "id": 657,
                    "scope": "public",
                    "updated_at": "2021-05-25T23:21:25Z",
                }
            ]
        }

    def test_get_message(self, mp_client: MPClient):
        assert mp_client.get_message(self.message_id) == {
            "author": {
                "email": "email@domain",
                "name": "John Doe",
                "role": "user",
            },
            "content": "Sample message",
            "created_at": "2021-05-25T23:21:24Z",
            "id": 659,
            "scope": "public",
            "updated_at": "2021-05-25T23:21:25Z",
        }

    def test_create_message(self, mp_client: MPClient):
        message = MPMessage(
            project_id=self.project_id,
            project_item_id=self.project_item_id,
            author=dict(
                email="helpdesk@helpdesk.com", name="Operator", role="mediator"
            ),
            content="Reply",
            scope="public",
        )

        assert mp_client.create_message(message) == {
            "author": {
                "email": "helpdesk@helpdesk.com",
                "name": "Operator",
                "role": "mediator",
            },
            "content": "Reply",
            "created_at": "2021-05-25T23:58:29Z",
            "id": 659,
            "scope": "public",
            "updated_at": "2021-05-25T23:58:29Z",
        }

    def test_update_message(self, mp_client: MPClient):
        assert mp_client.update_message(self.message_id, "Updated Content") == {
            "author": {
                "email": "helpdesk@helpdesk.com",
                "name": "Operator",
                "role": "mediator",
            },
            "content": "Updated Content",
            "created_at": "2021-05-25T23:58:29Z",
            "id": 659,
            "scope": "public",
            "updated_at": "2021-05-26T00:04:02Z",
        }

    def test_list_project_item(self, mp_client: MPClient):
        assert mp_client.list_project_item(self.project_id) == {
            "project_items": [
                {
                    "attributes": {
                        "category": "Discovery",
                        "offer": "For Researchers",
                        "offer_properties": [],
                        "order_type": "open_access",
                        "platforms": ["EUDAT", "DICE"],
                        "request_voucher": False,
                        "service": "B2FIND",
                    },
                    "id": 1,
                    "project_id": 1436,
                    "status": {"type": "ready", "value": "ready"},
                    "user_secrets": {},
                }
            ]
        }

    def test_get_project_item(self, mp_client: MPClient):
        assert mp_client.get_project_item(self.project_id, self.project_item_id) == {
            "attributes": {
                "category": "Discovery",
                "offer": "For Researchers",
                "offer_properties": [],
                "order_type": "open_access",
                "platforms": ["EUDAT", "DICE"],
                "request_voucher": False,
                "service": "B2FIND",
            },
            "id": 1,
            "project_id": 1436,
            "status": {"type": "ready", "value": "ready"},
            "user_secrets": {},
        }

    def test_update_project_item(self, mp_client: MPClient):
        assert mp_client.update_project_item(
            self.project_id, self.project_item_id, "in_progress"
        ) == {
            "attributes": {
                "category": "Orchestration",
                "offer": "Offer",
                "offer_properties": [],
                "order_type": "other",
                "platforms": [],
                "request_voucher": False,
                "service": "00 New resource test offert ",
            },
            "id": 1,
            "project_id": 1436,
            "status": {"type": "in_progress", "value": "in_progress"},
            "user_secrets": {},
        }
