# pylint: disable=too-few-public-methods, missing-function-docstring

"""File containing configs for all the environments"""
import os


class JIRAConfig:
    def __init__(self, **kwargs) -> None:
        self.username = kwargs.get("username", os.environ.get("OMS_JIRA_USERNAME"))
        self.password = kwargs.get("password", os.environ.get("OMS_JIRA_PASSWORD"))
        self.project = kwargs.get("project", os.environ.get("OMS_JIRA_PROJECT"))
        self.issue_type_id = kwargs.get("issue_type_id", os.environ.get("OMS_JIRA_ISSUE_TYPE_ID"))
        self.project_issue_type_id = kwargs.get("project_issue_type_id", os.environ.get("OMS_JIRA_PROJECT_ISSUE_TYPE_ID"))
        self.url = kwargs.get("url", os.environ.get("OMS_JIRA_URL"))
        self.context_path = kwargs.get("context_path", os.environ.get("OMS_JIRA_CONTEXT_PATH", "/jira"))
        self.webhook_secret = kwargs.get("webhook_secret", os.environ.get("OMS_JIRA_WEBHOOK_SECRET", ""))

        self.workflow = kwargs.get("workflow", {
            "todo": int(os.environ.get("OMS_JIRA_WF_TODO", "1")),
            "in_progress": int(os.environ.get("OMS_JIRA_WF_IN_PROGRESS", "2")),
            "waiting_for_response": int(
                os.environ.get("OMS_JIRA_WF_WAITING_FOR_RESPONSE", "3")
            ),
            "approved": int(os.environ.get("OMS_JIRA_WF_APPROVED", "4")),
            "rejected": int(os.environ.get("OMS_JIRA_WF_REJECTED", "5")),
            "closed": int(os.environ.get("OMS_JIRA_WF_CLOSED", "6")),
            "ready": int(os.environ.get("OMS_JIRA_WF_READY", "7")),
            "archived": int(os.environ.get("OMS_JIRA_WF_ARCHIVED", "8")),
        })

        self.custom_fields = kwargs.get("custom_fields", {
            "Epic Link": os.environ.get("OMS_JIRA_FIELD_Epic_Link", ""),
            "Epic Name": os.environ.get("OMS_JIRA_FIELD_Epic_Name", ""),
            "Order reference": os.environ.get("OMS_JIRA_FIELD_Order_reference", ""),
            "CI-Name": os.environ.get("OMS_JIRA_FIELD_CI_Name", ""),
            "CI-Surname": os.environ.get("OMS_JIRA_FIELD_CI_Surname", ""),
            "CI-Email": os.environ.get("OMS_JIRA_FIELD_CI_Email", ""),
            "CI-DisplayName": os.environ.get("OMS_JIRA_FIELD_CI_DisplayName", ""),
            "CI-EOSC-UniqueID": os.environ.get("OMS_JIRA_FIELD_CI_EOSC_UniqueID", ""),
            "CI-Institution": os.environ.get("OMS_JIRA_FIELD_CI_Institution", ""),
            "CI-Department": os.environ.get("OMS_JIRA_FIELD_CI_Department", ""),
            "CI-DepartmentalWebPage": os.environ.get(
                "OMS_JIRA_FIELD_CI_DepartmentalWebPage", ""
            ),
            "CI-SupervisorName": os.environ.get("OMS_JIRA_FIELD_CI_SupervisorName", ""),
            "CI-SupervisorProfile": os.environ.get(
                "OMS_JIRA_FIELD_CI_SupervisorProfile", ""
            ),
            "CP-CustomerTypology": os.environ.get("OMS_JIRA_FIELD_CP_CustomerTypology", ""),
            "CP-ReasonForAccess": os.environ.get("OMS_JIRA_FIELD_CP_ReasonForAccess", ""),
            "CP-UserGroupName": os.environ.get("OMS_JIRA_FIELD_CP_UserGroupName", ""),
            "CP-ProjectInformation": os.environ.get(
                "OMS_JIRA_FIELD_CP_ProjectInformation", ""
            ),
            "SO-ProjectName": os.environ.get("OMS_JIRA_FIELD_SO_ProjectName", ""),
            "CP-ScientificDiscipline": os.environ.get(
                "OMS_JIRA_FIELD_CP_ScientificDiscipline", ""
            ),
            "CP-Platforms": os.environ.get("OMS_JIRA_FIELD_CP_Platforms", ""),
            "CP-INeedAVoucher": os.environ.get("OMS_JIRA_FIELD_CP_INeedAVoucher", ""),
            "CP-VoucherID": os.environ.get("OMS_JIRA_FIELD_CP_VoucherID", ""),
            "SO-1": os.environ.get("OMS_JIRA_FIELD_SO_1", ""),
            "SO-ServiceOrderTarget": os.environ.get(
                "OMS_JIRA_FIELD_SO_ServiceOrderTarget", ""
            ),
            "SO-OfferType": os.environ.get("OMS_JIRA_FIELD_SO_OfferType", ""),
            "CP-CustomerCountry": os.environ.get("OMS_JIRA_FIELD_CP_CustomerCountry", ""),
            "CP-CollaborationCountry": os.environ.get(
                "OMS_JIRA_FIELD_CP_CollaborationCountry", ""
            ),
        })

        self.select_values = kwargs.get("select_values", {
            "CP-CustomerTypology": {
                "single_user": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_CP_CustomerTypology_single_user", ""
                ),
                "research": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_CP_CustomerTypology_research", ""
                ),
                "private_company": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_CP_CustomerTypology_private_company", ""
                ),
                "project": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_CP_CustomerTypology_project", ""
                ),
            },
            "CP-INeedAVoucher": {
                "yes": os.environ.get("OMS_JIRA_FIELD_SELECT_VALUES_CP_INeedAVoucher_true"),
                "no": os.environ.get("OMS_JIRA_FIELD_SELECT_VALUES_CP_INeedAVoucher_false"),
            },
            "SO-OfferType": {
                "orderable": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_SO_OfferType_normal", ""
                ),
                "open_access": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_SO_OfferType_open_access", ""
                ),
                "external": os.environ.get(
                    "OMS_JIRA_FIELD_SELECT_VALUES_SO_OfferType_catalog", ""
                ),
            },
        })


class Config:
    """Default config"""

    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTPLUS_VALIDATE = True
    RESTPLUS_ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False
    REDIS_HOST = os.environ.get("OMS_REDIS_HOST", "redis://127.0.0.1:36379")
    JIRA_CONFIG = JIRAConfig()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OMS_ID = os.environ.get("OMS_ID")
    MP_TOKEN = os.environ.get("OMS_MP_TOKEN")
    MP_URL = os.environ.get("OMS_MP_URL")
    AUTHORIZATION_PASSWORD = os.environ.get("OMS_AUTHORIZATION_PASSWORD")


class ProductionConfig(Config):
    """Production config"""

    RESTPLUS_ERROR_404_HELP = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("OMS_DB")


class DevelopmentConfig(Config):
    """Development config"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "OMS_DB_HOST", "postgresql://postgres:postgres@127.0.0.1:35432/oms_jira"
    )
    MP_URL = os.environ.get("OMS_MP_URL", "http://localhost:5000")
    AUTHORIZATION_PASSWORD = os.environ.get("OMS_AUTHORIZATION_PASSWORD", "secretpassword")


class TestingConfig(Config):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(
            "OMS_DB_HOST", "postgresql://postgres:postgres@127.0.0.1:35432/oms_jira"
        )
        + "_test"
    )
    OMS_ID = 1
    MP_URL = "http://localhost:5000"
    MP_TOKEN = os.environ.get("OMS_MP_TOKEN", "NRKmtZsY8J4FCXttRRvH")
    AUTHORIZATION_PASSWORD = os.environ.get("OMS_AUTHORIZATION_PASSWORD", "secretpassword")
    JIRA_CONFIG = JIRAConfig(webhook_secret="12345678")


config_by_name = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
