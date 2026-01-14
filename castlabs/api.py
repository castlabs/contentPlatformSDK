import os
from datetime import timezone
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, computed_field

from castlabs.client import Client
from castlabs.repository import StorageLocation, UploadClient
from castlabs.urls import API_URLS

UTC = timezone.utc


class Encoding(BaseModel):
    content_url: str
    status: str
    group_name: str
    encode_name: str

    @computed_field
    @property
    def hls_url(self) -> str:
        return self.content_url + "hls.m3u8"

    @computed_field
    @property
    def dash_url(self) -> str:
        return self.content_url + "dash.mpd"

    @computed_field
    @property
    def complete(self) -> bool:
        return self.status in ["PUBLISH_SUCCESS", "ENCODING_FAILED", "PUBLISH_FAILED"]


class UploadCredentials(BaseModel):
    url: str
    fields: Dict[str, str]


class ContentPlatform:
    """
    The contentPlatform API provides a simple interface to interact with the Castlabs Content Platform.
    """

    def __init__(
        self,
        organization_urn: str,
        user_urn: str,
        api_secret_access_key: str,
        api_access_key_id: str,
        environment: Literal["production", "staging"] = "production",
    ):
        """
        Initialize the SDK
        :param organization_urn: The organization URN (urn:janus:accesskey:XXX)
        :param user_urn: The user urn
        :param api_secret_access_key: The secret access key to use (urn:janus:accesskey:XXX)
        :param api_access_key_id: The key id
        :param environment: Define 'production' (default) or 'staging'
        """

        self._client = Client(
            organization_urn=organization_urn,
            user_urn=user_urn,
            api_secret_access_key=api_secret_access_key,
            api_access_key_id=api_access_key_id,
            urls=API_URLS[environment],
        )

        # Initalize Properties
        self.__repository = None
        self.__workflow = None
        self.__storage_location = None
        self.__upload_clients = {}

    @property
    def _repository(self):
        """
        Access the repository API
        """
        if self.__repository is None:
            from castlabs.repository import Repository

            self.__repository = Repository(self._client)
        return self.__repository

    @property
    def _workflow(self):
        """
        Access the repository API
        """
        if self.__workflow is None:
            from castlabs.workflow import Workflow

            self.__workflow = Workflow(self._client)
        return self.__workflow

    @property
    def _storage_location(self) -> StorageLocation:
        """
        Access the storage location API
        """
        if self.__storage_location is None:
            self.__storage_location = self._repository.get_storage_location()

        return self.__storage_location

    def _get_upload_client(self, path: str) -> UploadClient:
        """
        Access the storage location API
        """
        if path not in self.__upload_clients:  # pragma: no cover
            self.__upload_clients[path] = self._storage_location.create_upload_client(path)

        return self.__upload_clients[path]

    def get_upload_url(self, remote_path: str) -> str:
        """
        Get the upload URL for a specific path
        :param remote_path: The path to upload to
        :return: The upload URL
        """
        return self._get_upload_client(remote_path).upload_url  # pragma: no cover

    def upload_file(self, file_path: str, remote_path: Optional[str] = None) -> str:
        """
        Upload a file to a specific path
        :param remote_path: The path to upload to
        :param file_path: The file to upload
        """
        remote_path = remote_path or os.path.basename(file_path).replace(".", "_")
        self._get_upload_client(remote_path).upload_file(file_path)

        return remote_path

    def get_upload_credentials(self, remote_path: str) -> UploadCredentials:
        """
        Get the upload credentials for a specific path
        :param remote_path: The path to upload to
        :return: The upload credentials
        """
        values = self._get_upload_client(remote_path).generate_presigned_url()
        return UploadCredentials(
            url=values["url"],  # type: ignore
            fields=values["fields"],  # type: ignore
        )

    def list_files(self, remote_path: str) -> List[str]:
        """
        Read files from a specific path
        :param remote_path: The path to read from
        :return: The list of files
        """
        return [c["name"] for c in self._repository.get_content_of_directory(self._storage_location, remote_path)]

    def start_encoding(
        self,
        remote_path: str,
        group_name: str = "default_group",
        encode_name: Optional[str] = None,
        template="cmaf-abr",
        format_specific_data: Optional[dict] = "{}",
        webhook_url: Optional[str] = None,
    ) -> Encoding:
        """
        Encode the files uploaded to a specific path
        :param path: The path to encode
        :param group_name: The group name
        :param encode_name: The encode name
        :param format_specific_data: Extra parameters for the encoding workflow
        """
        encode_name = encode_name or remote_path.split("/")[-1]

        process = self._workflow.create_vod_encoding(
            self._storage_location,
            remote_path,
            group_name,
            encode_name,
            template=template,
            format_specific_data=format_specific_data,
            webhook_url=webhook_url,
        )
        process.refresh_state()

        return Encoding(
            content_url=process.content_url,
            status=process.state,
            group_name=group_name,
            encode_name=encode_name,
        )

    def get_status(
        self,
        remote_path: Optional[str] = None,
        group_name: str = "default_group",
        encode_name: Optional[str] = None,
    ):
        """
        Get the status of an encoding
        :param remote_path: The path is being encoded
        :param group_name: The group name
        :param encode_name: The encode name
        """
        if not encode_name:
            if not remote_path:
                raise ValueError("One of remote_path and encode_name must be provided")

            encode_name = remote_path.split("/")[-1]

        process = self._workflow.get_process(group_name, encode_name)
        process.refresh_state()

        return Encoding(
            content_url=process.content_url,
            status=process.state,
            group_name=group_name,
            encode_name=encode_name,
        )

    def get_groups(self) -> List[str]:
        """
        Get the list of groups
        """
        return self._workflow.get_groups()
