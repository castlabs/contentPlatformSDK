from typing import Dict, Literal, TypedDict


class ApiUrls(TypedDict):
    credential_exchange: str
    workflow: str
    repository: str


API_URLS: Dict[Literal["production", "staging"], ApiUrls] = {
    "production": {
        "credential_exchange": "https://auth.castlabs.com/api/v1/keypair/credentialexchange",
        "workflow": "https://workflow.content.castlabs.com/graphql",
        "repository": "https://repository.content.castlabs.com/graphql",
    },
    "staging": {
        "credential_exchange": "https://auth.test.cs.castlabs.com/api/v1/keypair/credentialexchange",
        "workflow": "https://workflow.content-stag.castlabs.com/graphql",
        "repository": "https://repository.content-stag.castlabs.com/graphql",
    },
}
