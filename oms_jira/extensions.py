"""Extensions for flask recommender"""
from urllib.parse import urlparse
import os

import redis
from celery import Celery
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
celery = Celery()

redis_broker = os.environ.get("REDIS_BROKER", "redis://localhost:36379/3")
redis_parsed = urlparse(redis_broker)

redis_client = redis.Redis(
    host=redis_parsed.hostname,
    port=int(redis_parsed.port),
    db=int(redis_parsed.path.lstrip("/")),
)
