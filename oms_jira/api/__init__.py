"""Api object definition and endpoint namespaces registration"""

from flask_restx import Api

from oms_jira.api.schemas import api as models_ns
from oms_jira.api.endpoints.mp import api as oms_trigger_ns
from oms_jira.api.endpoints.jira_webhook import api as jira_webhook_ns


api = Api(
    doc="/",
    version="1.0",
    title="Recommender system API",
    description="Recommender System API for getting recommendations, sending user "
    "actions, sending Marketplace database dumps and triggering "
    "recommender system offline learning.",
)

# API namespaces
api.add_namespace(models_ns)
api.add_namespace(oms_trigger_ns)
api.add_namespace(jira_webhook_ns)
