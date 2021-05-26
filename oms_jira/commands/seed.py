import datetime
import typing
from typing import Optional

import click
from pydantic import BaseModel

from oms_jira import db
from oms_jira.models import Bookkeeping
from oms_jira.models.mapping import Project


class SerializedComment(BaseModel):
    mp_id: int
    project_item_id: Optional[int]
    project_id: Optional[int]


class SerializedProject(BaseModel):
    mp_id: int
    jira_id: int


class SerializedProjectItem(BaseModel):
    mp_id: int
    jira_id: int
    project_id: int


class Seed(BaseModel):
    project_items: typing.List[SerializedProjectItem]
    projects: typing.List[SerializedProject]
    comments: typing.List[SerializedComment]
    timestamp: datetime.datetime


def seed(seed_file_path: str):
    try:
        data: Seed = Seed.parse_file(seed_file_path)
    except Exception as e:
        click.echo(e, err=True)
        return

    bookkeeping = db.session.query(Bookkeeping).one_or_none()
    if bookkeeping is None:
        db.session.add(Bookkeeping(last_event_timestamp=data.timestamp, last_event_id=None))
    else:
        bookkeeping.last_event_timestamp=data.timestamp
    db.session.commit()

    for p in data.projects:
        db.session.add(Project(**p.dict()))
    db.session.commit()
