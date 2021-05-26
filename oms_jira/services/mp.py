import datetime
import typing
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from apiclient import (
    APIClient,
    HeaderAuthentication,
    endpoint,
    JsonResponseHandler,
    JsonRequestFormatter,
)
from flask import current_app

from oms_jira import db
from oms_jira.models import Project
from settings import JIRAConfig


class Event(BaseModel):
    class TypeEnum(str, Enum):
        create = "create"
        update = "update"
        delete = "delete"

    class ResourceEnum(str, Enum):
        project = "project"
        project_item = "project_item"
        message = "message"

    class Change(BaseModel):
        field: str
        before: str
        after: str

    timestamp = datetime.datetime
    type: TypeEnum
    resource: ResourceEnum
    project_id: Optional[int]
    project_item_id: Optional[int]
    message_id: Optional[int]
    changes: Optional[List[Change]]


class EventResponse(BaseModel):
    events: List[Event]


class ProjectItemStatusEnum(str, Enum):
    created = "created"
    rejected = "rejected"
    waiting_for_response = "waiting_for_response"
    registered = "registered"
    in_progress = "in_progress"
    ready = "ready"
    closed = "closed"
    approved = "approved"


class RoleEnum(str, Enum):
    provider = "provider"
    mediator = "mediator"


class ScopeEnum(str, Enum):
    public = "public"
    internal = "internal"
    user_direct = "user_direct"


class MessageAuthor(BaseModel):
    email: EmailStr
    name: str
    role: RoleEnum


class MPMessage(BaseModel):
    project_id: int
    project_item_id: int
    author: typing.Optional[MessageAuthor]
    content: str
    scope: ScopeEnum


class MPMessageList(BaseModel):
    messages: List[MPMessage]


class ProjectOwner(BaseModel):
    uid: str
    email: str
    first_name: str
    last_name: str
    name: str


class ProjectItemAttributes(BaseModel):
    category: str
    service: str
    offer: str
    voucher_id: int
    offer_properties: List[dict]
    platforms: List[str]
    request_voucher: bool
    order_type: str


class MPProjectItem(BaseModel):
    class Status(BaseModel):
        value: str
        type: str

    id: int
    project_id: int
    status: Status
    attributes: ProjectItemAttributes
    user_secrets: dict

    def jira_fields(self, jira_config: JIRAConfig, project_key: str) -> dict:
        project = get_mp_client().get_project(self.project_id)
        return {
            "summary": f"Service order, {project.owner.name} {self.attributes.service}",
            "project": {"key": jira_config.project},
            "issuetype": {"id": jira_config.issue_type_id},
            jira_config.custom_fields.get("Order reference"): None,
            jira_config.custom_fields.get("Epic Link"): project_key,
            jira_config.custom_fields.get("CP-Platforms"): ", ".join(self.attributes.platforms),
            jira_config.custom_fields.get("CP-INeedAVoucher"): {
                "id": jira_config.select_values.get("CP-INeedAVoucher").get("yes" if self.attributes.request_voucher else "no")
            },
            jira_config.custom_fields.get("CP-VoucherID"): self.attributes.voucher_id,
            jira_config.custom_fields.get("SO-1"): {
                "category": self.attributes.category,
                "service": self.attributes.service,
                "offer": self.attributes.offer,
                "attributes": {prop["label"]: prop["value"] for prop in self.attributes.offer_properties}
            },
            # TODO: THIS WILL NOT WORK, NOT ENOUGH INFO FROM BACKEND
            jira_config.custom_fields.get("SO-ServiceOrderTarget"): "",
            # TODO: THIS WILL NOT WORK, NOT ENOUGH INFO FROM BACKEND
            jira_config.custom_fields.get("SO-OfferType"): {
                "id": jira_config.select_values.get("SO-OfferType")
            },
        }


class MPProjectItemList(BaseModel):
    project_items: List[MPProjectItem]


class ProjectAttributes(BaseModel):
    class CustomerTypology(str, Enum):
        single_user = "single_user"
        research = "research"
        private_company = "private_company"
        project = "project"

    name: str
    customer_typology: CustomerTypology
    organization: str
    department: str
    department_webpage: str
    scientific_domains: List[str]
    country: str
    collaboration_countries: List[str]
    user_group_name: str


class MPProject(BaseModel):
    id: int
    owner: ProjectOwner
    project_items: List[int]
    attributes: ProjectAttributes

    def jira_fields(self, jira_config: JIRAConfig) -> dict:
        single_user_or_community = (
            self.attributes.customer_typology
            == ProjectAttributes.CustomerTypology.single_user
            or self.attributes.customer_typology
            == ProjectAttributes.CustomerTypology.research
        )

        return {
            "summary": f"Project {self.owner.name}",
            "project": jira_config.project,
            "issuetype": {"id": jira_config.project_issue_type_id},
            jira_config.custom_fields.get("Epic Name"): self.attributes.name,
            jira_config.custom_fields.get("CI-Name"): self.owner.first_name,
            jira_config.custom_fields.get("CI-Surname"): self.owner.last_name,
            jira_config.custom_fields.get("CI-Email"): self.owner.email or None,
            jira_config.custom_fields.get(
                "CI-Institution"
            ): self.attributes.organization
            if single_user_or_community
            else None,
            jira_config.custom_fields.get("CI-Department"): self.attributes.department
            if single_user_or_community
            else None,
            jira_config.custom_fields.get(
                "CI-DepartmentalWebPage"
            ): self.attributes.department_webpage
            if single_user_or_community
            else None,
            jira_config.custom_fields.get("CI-DisplayName"): self.owner.name,
            jira_config.custom_fields.get("CP-ScientificDiscipline"): ", ".join(
                self.attributes.scientific_domains
            )
            if self.attributes.scientific_domains
            else "N/A",
            jira_config.custom_fields.get("CI-EOSC-UniqueID"): self.owner.uid,
            jira_config.custom_fields.get(
                "CP-CustomerTypology"
            ): jira_config.select_values.get("CP-CustomerTypology").get(
                self.attributes.customer_typology
            ),
            jira_config.custom_fields.get("CP-CustomerCountry"): self.attributes.country
            or "N/A",
            jira_config.custom_fields.get("CP-CollaborationCountry"): ", ".join(
                self.attributes.collaboration_countries
            )
            if self.attributes.collaboration_countries
            else "N/A",
            jira_config.custom_fields.get(
                "CP-UserGroupName"
            ): self.attributes.user_group_name,
            jira_config.custom_fields.get(
                "SO-ProjectName"
            ): f"{self.attributes.name} ({self.id})",
        }


class MPProjectList(BaseModel):
    projects: List[MPProject]


class MPRequestFormatter(JsonRequestFormatter):
    @classmethod
    def get_headers(cls) -> dict:
        headers = super().get_headers()
        headers.update({"Accept": "application/json"})
        return headers


class MPClient(APIClient):
    def __init__(self, endpoint_url: str, oms_id: str, auth_token: str):
        super().__init__(
            authentication_method=HeaderAuthentication(
                auth_token, parameter="X-User-Token", scheme=None
            ),
            response_handler=JsonResponseHandler,
            request_formatter=MPRequestFormatter,
        )

        self.auth_token = auth_token
        self.oms_id = int(oms_id)

        @endpoint(base_url=endpoint_url)
        class Endpoint:
            event_list = f"/api/v1/oms/{self.oms_id}/events"
            message_list = f"/api/v1/oms/{self.oms_id}/messages"
            message = f"/api/v1/oms/{self.oms_id}/messages/{{message_id}}"
            project_item_list = (
                f"/api/v1/oms/{self.oms_id}/projects/{{project_id}}/project_items"
            )
            project_item = f"/api/v1/oms/{self.oms_id}/projects/{{project_id}}/project_items/{{project_item_id}}"
            project_list = f"/api/v1/oms/{self.oms_id}/projects"
            project = f"/api/v1/oms/{self.oms_id}/projects/{{project_id}}"
            oms_list = f"/api/v1/oms"
            oms = f"/api/v1/oms/{self.oms_id}"

        self.endpoint = Endpoint

    def list_events(
        self, from_timestamp: datetime.datetime, limit: Optional[int] = None
    ) -> List[Event]:
        params = dict(oms_id=self.oms_id, from_timestamp=from_timestamp.isoformat())

        if limit is not None:
            params["limit"] = limit

        return EventResponse.parse_obj(
            self.get(self.endpoint.event_list, params=params)
        ).events

    def list_message(
        self,
        project_id: int,
        project_item_id: Optional[int] = None,
        from_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[MPMessage]:
        return MPMessageList.parse_obj(self.get(
            self.endpoint.message_list,
            params=dict(
                project_item_id=project_item_id,
                project_id=project_id,
                from_id=from_id,
                limit=limit,
            )).messages,
        )

    def get_message(self, message_id: int) -> MPMessage:
        return MPMessage.parse_obj(
            self.get(self.endpoint.message.format(message_id=message_id))
        )

    def create_message(self, message: MPMessage) -> MPMessage:
        return MPMessage.parse_obj(
            self.post(self.endpoint.message_list, data=message.dict())
        )

    def update_message(self, message_id: int, content: str) -> MPMessage:
        return MPMessage.parse_obj(
            self.patch(
                self.endpoint.message.format(message_id=message_id),
                data=dict(content=content),
            )
        )

    def list_project_item(self, project_id: int) -> List[MPProjectItem]:
        return MPProjectItemList.parse_obj(
            self.get(self.endpoint.project_item_list.format(project_id=project_id))
        ).project_items

    def get_project_item(self, project_id: int, project_item_id: int) -> MPProjectItem:
        return MPProjectItem.parse_obj(
            self.get(
                self.endpoint.project_item.format(
                    project_id=project_id, project_item_id=project_item_id
                )
            )
        )

    def update_project_item(
        self, project_id: int, project_item_id: int, status: ProjectItemStatusEnum
    ):
        return self.patch(
            self.endpoint.project_item.format(
                project_id=project_id, project_item_id=project_item_id
            ),
            data={"status": {"value": status, "type": status}, "user_secrets": {}},
        )

    def list_project(self) -> List[MPProject]:
        return MPProjectList.parse_obj(self.get(self.endpoint.project_list)).projects

    def get_project(self, project_id: int) -> MPProject:
        return MPProject.parse_obj(
            self.get(self.endpoint.project.format(project_id=project_id))
        )

    def list_oms(self):
        return self.get(self.endpoint.oms_list)

    def get_oms(self):
        return self.get(self.endpoint.oms)


def get_mp_client() -> MPClient:
    return MPClient(
        endpoint_url=current_app.config.get("MP_URL"),
        oms_id=current_app.config.get("OMS_ID"),
        auth_token=current_app.config.get("MP_TOKEN"),
    )
