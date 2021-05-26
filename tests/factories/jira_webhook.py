import factory


class CommentFactory(factory.DictFactory):
    self = "https://jira.atlassian.com/rest/api/2/issue/10148/comment/252789"
    id = "252789"
    author = {
        "self": "https://jira.atlassian.com/rest/api/2/user?username=brollins",
        "name": "brollins",
        "emailAddress": "bryansemail@atlassian.com",
        "avatarUrls": {
            "16x16": "https://jira.atlassian.com/secure/useravatar?size=small&avatarId=10605",
            "48x48": "https://jira.atlassian.com/secure/useravatar?avatarId=10605",
        },
        "displayName": "Bryan Rollins [Atlassian]",
        "active": True,
    }
    body = ("Just in time for AtlasCamp!",)
    updateAuthor = {
        "self": "https://jira.atlassian.com/rest/api/2/user?username=brollins",
        "name": "brollins",
        "emailAddress": "brollins@atlassian.com",
        "avatarUrls": {
            "16x16": "https://jira.atlassian.com/secure/useravatar?size=small&avatarId=10605",
            "48x48": "https://jira.atlassian.com/secure/useravatar?avatarId=10605",
        },
        "displayName": "Bryan Rollins [Atlassian]",
        "active": True,
    }
    created = "2011-06-07T10:31:26.805-0500"
    updated = "2011-06-07T10:31:26.805-0500"


class IssueFactory(factory.DictFactory):
    id = factory.Sequence(lambda n: n)
    self = factory.LazyAttribute(lambda issue: f"https://jira.atlassian.com/rest/api/2/issue/{issue.id}")
    key = factory.LazyAttribute(lambda issue: f"JRA-{issue.id + 100}")
    fields = {
        "summary": "I feel the need for speed",
        "created": "2009-12-16T23:46:10.612-0600",
        "description": "Make the issue nav load 10x faster",
        "labels": ["UI", "dialogue", "move"],
        "priority": "Minor",
    }


class UserFactory(factory.DictFactory):
    self = "https://jira.atlassian.com/rest/api/2/user?username=brollins"
    name = "brollins"
    key = "brollins"
    emailAddress = "bryansemail at atlassian dot com"
    avatarUrls = {
        "16x16": "https://jira.atlassian.com/secure/useravatar?size=small&avatarId=10605",
        "48x48": "https://jira.atlassian.com/secure/useravatar?avatarId=10605",
    }
    displayName = "Bryan Rollins [Atlassian]"
    active = "true"


class JiraWebhookRequestFactory(factory.DictFactory):
    id = factory.Sequence(lambda n: n + 1)
    timestamp = 1525698237764
    issue = factory.SubFactory(IssueFactory)
    user = factory.SubFactory(UserFactory)
    issue_id = 0
    issue_status = 4
    voucher_id_from = None
    voucher_id_to = None
    message = "Just in time for AtlasCamp!"
    request_type = "jira:issue_updated"
    comment = factory.SubFactory(CommentFactory)

    changelog = factory.LazyAttribute(
        lambda obj: {
            "items": [
                {
                    "toString": "A new summary.",
                    "to": obj.issue_status,
                    "fromString": "What is going on here?????",
                    "from": 0,
                    "fieldtype": "jira",
                    "field": "status",
                }
            ],
            "id": 10124,
        }
    )

    webhookEvent = "comment_updated"
