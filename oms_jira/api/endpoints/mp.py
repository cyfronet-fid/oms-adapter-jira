"""Endpoints used by MP"""

from flask_restx import Resource, Namespace

from oms_jira.tasks.mp import process_mp_trigger

api = Namespace("mp", "Endpoint called when Marketplace ordering status changes (triggers data load & process)")


@api.route("/trigger")
class OMSTrigger(Resource):
    """Triggers data load"""

    @api.response(204, "MP Trigger received")
    def post(self):
        process_mp_trigger.delay()
        return None, 204
