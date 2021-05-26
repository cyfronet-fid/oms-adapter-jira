"""Fixtures used by pytest shared across all tests"""

import pytest
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from oms_jira import create_app


@pytest.fixture()
def flask_app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture
def client(flask_app: Flask):
    """Flask app client that you can make HTTP requests to"""
    yield flask_app.test_client()


@pytest.fixture(scope="session")
def _db(request):
    """
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    """

    db = SQLAlchemy(app=create_app())
    db.drop_all()
    db.create_all()

    @request.addfinalizer
    def drop_database():
        db.drop_all()

    return db
