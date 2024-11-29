import base64
import json
from datetime import datetime, timezone
from hashlib import sha1, sha256
from hmac import HMAC
from logging import getLogger
from typing import Dict, List, Literal

import requests

from castlabs.errors import CPAuthorizationException, CPMalformedHttpRequestException
from castlabs.urls import ApiUrls

UTC = timezone.utc


logger = getLogger("castlabs.client")


class Client:
    """
    The contentPlatformSDK introduces naming of Objects that deviate from the GraphQL for the better understanding
    of generic Workflows.

    Mapping of terms:
    * PO -> Group
    * PO Item -> Process
    * workflow_process -> encoding_process (this and the publish_process are SUB processes of a Process object)
    * Workflow - The API module for managing Processes
    * Repository - The API module for managing the Filesystem
    """

    def __init__(
        self,
        organization_urn: str,
        user_urn: str,
        api_secret_access_key: str,
        api_access_key_id: str,
        urls: ApiUrls,
    ):
        """
        Initialize the SDK
        :param organization_urn: The organization URN (urn:janus:accesskey:XXX)
        :param user_urn: The user urn
        :param secret_access_key: The secret access key to use (urn:janus:accesskey:XXX)
        :param access_key_id: The key id
        :param environment: Define 'production' (default) or 'staging'
        """

        # for key exchange
        self.organization_urn = organization_urn
        self.organization_id = self.organization_urn.split(":")[-1]
        self._user_urn = user_urn
        self._api_secret_access_key = api_secret_access_key
        self._api_access_key_id = api_access_key_id

        # for authenticating the users actions
        self._id_token = None
        self._access_token = None

        self._urls = urls

        self._authenticate()

    def _authenticate(self) -> None:
        payload_str = json.dumps({"access_key_id": self._api_access_key_id, "timestamp": datetime.now(UTC).isoformat()})
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d")
        secret_token = HMAC(("castLabs " + self._api_secret_access_key).encode(), timestamp.encode(), sha256).digest()
        user_token = HMAC(secret_token, self._user_urn.encode(), sha256).digest()
        signing_key = HMAC(user_token, "castLabs-api_auth".encode(), sha256).digest()
        signature = base64.b64encode(HMAC(signing_key, payload_str.encode(), sha1).digest())

        headers = {
            "X-Castlabs-Keypair-Signature": signature,
            "Content-Type": "application/json",
        }

        response = requests.post(
            self._urls["credential_exchange"],
            headers=headers,
            data=payload_str.encode("UTF-8"),
            timeout=10,  # Set timeout for better resiliency
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        resp_json = response.json()
        self._id_token = resp_json["id_token"]
        self._access_token = resp_json["access_token"]

        logger.info("Authenticated successfully with the Castlabs API")

    def _query_api(
        self, api: Literal["workflow", "repository"], query: dict, content_key: str, method: str = "POST"
    ) -> Dict | List:
        """
        Generic API function

        :param query: GraphQL query
        :param api: API endpoint
        :param content_key: Key mapping the actual data of the response
        :param method: (Optional) HTTP method
        :return: Response object or list of objects
        """
        url = self._urls[api]
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "x-castlabs-organization": f"{self.organization_urn}",
        }

        logger.debug(f"Querying API: {api} with query: {query}")
        response = requests.request(
            method,
            url,
            headers=headers,
            json=query,  # Automatically encodes query to JSON
            timeout=10,  # Set timeout for better resiliency
        )

        logger.debug(f"Received response: {response.text}")

        # Raise an exception for HTTP errors
        response.raise_for_status()

        response_json = response.json()

        # Check for GraphQL-specific errors
        if "errors" in response_json:
            error = response_json["errors"][0]
            error_type = error.get("errorType")
            if error_type == "MalformedHttpRequestException":
                raise CPMalformedHttpRequestException(error)
            elif error_type == "Unauthorized":
                raise CPAuthorizationException(error)
            else:
                raise Exception(error["message"])

        return response_json["data"][content_key]

    def _query_api_dict(
        self, api: Literal["workflow", "repository"], query: dict, content_key: str, method: str = "POST"
    ) -> Dict:
        """
        Generic API function

        :param query: GraphQL query
        :param url: API endpoint
        :param content_key: Key mapping the actual data of the response
        :param method: (Optional) HTTP method
        :return: Response object
        """
        response = self._query_api(api, query, content_key, method)
        if isinstance(response, list):  # pragma: no cover
            raise Exception("Expected a single object but got a list")

        return response
