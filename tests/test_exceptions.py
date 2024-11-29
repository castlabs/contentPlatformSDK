from typing import Callable
from unittest.mock import Mock

import pytest
from requests.exceptions import HTTPError

from castlabs.api import ContentPlatform
from castlabs.client import Client
from castlabs.errors import CPAuthorizationException, CPMalformedHttpRequestException


@pytest.fixture
def client(platform: ContentPlatform) -> Client:
    """
    Fixture to initialize and return the API client.
    Replace `YourAPIClient` with your actual client class.
    """
    return platform._client


@pytest.fixture
def mock_request(monkeypatch: pytest.MonkeyPatch) -> Callable[..., None]:
    """
    Fixture to mock the requests.request method.
    """

    def _mock_request(mock_response) -> None:
        def mock_response_func(method, url, headers, json, timeout):
            return mock_response

        monkeypatch.setattr("requests.request", mock_response_func)

    return _mock_request


def test_graphql_malformed_http_request_exception(client: Client, mock_request: Callable[..., None]) -> None:
    # Mock the response for a malformed request
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {
        "errors": [{"errorType": "MalformedHttpRequestException", "message": "Malformed request"}]
    }
    mock_request(mock_response)

    with pytest.raises(CPMalformedHttpRequestException):
        client._query_api(
            api="workflow",
            query={"query": "mock_query"},
            content_key="mock_key",
        )


def test_graphql_unauthorized_exception(client: Client, mock_request: Callable[..., None]) -> None:
    # Mock the response for an unauthorized request
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"errors": [{"errorType": "Unauthorized", "message": "Unauthorized access"}]}
    mock_request(mock_response)

    with pytest.raises(CPAuthorizationException):
        client._query_api(
            api="repository",
            query={"query": "mock_query"},
            content_key="mock_key",
        )


def test_graphql_generic_exception(client: Client, mock_request: Callable[..., None]) -> None:
    # Mock the response for a generic GraphQL error
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {
        "errors": [{"errorType": "UnknownError", "message": "An unknown error occurred"}]
    }
    mock_request(mock_response)

    with pytest.raises(Exception) as excinfo:
        client._query_api(
            api="workflow",
            query={"query": "mock_query"},
            content_key="mock_key",
        )

    assert str(excinfo.value) == "An unknown error occurred"


def test_graphql_successful_response(client: Client, mock_request: Callable[..., None]) -> None:
    # Mock a successful GraphQL response
    mock_response = Mock()
    mock_response.raise_for_status = Mock()  # Simulates no HTTP error
    mock_response.json.return_value = {"data": {"mock_key": {"field": "value"}}}
    mock_request(mock_response)

    result = client._query_api(
        api="repository",
        query={"query": "mock_query"},
        content_key="mock_key",
    )

    assert result == {"field": "value"}


def test_http_error_handling(client: Client, mock_request: Callable[..., None]) -> None:
    # Mock an HTTP error response
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError("HTTP Error occurred")
    mock_request(mock_response)

    with pytest.raises(HTTPError):
        client._query_api(
            api="workflow",
            query={"query": "mock_query"},
            content_key="mock_key",
        )


def test_bad_storage_location(platform: ContentPlatform) -> None:
    with pytest.raises(FileNotFoundError):
        platform._repository.get_storage_location("bad_location")


def test_get_bad_status(platform: ContentPlatform) -> None:
    with pytest.raises(ValueError):
        platform.get_status()

    with pytest.raises(KeyError):
        platform.get_status(encode_name="bad_encode_name")
