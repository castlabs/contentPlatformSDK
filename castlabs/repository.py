import json
import os
from logging import getLogger
from typing import Any, Dict, List, Optional, TypedDict
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import boto3

import castlabs.client as client

logger = getLogger("castlabs.repository")


class ContentsOfDirectory(TypedDict):
    id: str
    name: str
    size: float
    last_modified: str
    deleted: bool
    archived: bool
    archive: Any


class Repository:
    """
    The Repository class exposes functionality directly related to the repository and file-management
    on the ContentPlatform. The class will be initialized by the contentPlatformSDK. It should not be necessary
    to do this manually.
    """

    def __init__(self, client: client.Client):

        self.client = client

    def get_storage_locations(self) -> list:
        logger.info("Getting storage locations")
        storage_configs = self.client._query_api(
            "repository",
            query={
                "operationName": "GetRootsurn_janus_organization",
                "variables": {},
                "query": """
                    query GetRootsurn_janus_organization {
                        roots {
                            id
                            name
                            __typename
                        }
                    }""",
            },
            content_key="roots",
        )
        return [StorageLocation(storage_config, self) for storage_config in storage_configs]

    def get_storage_location(self, name: Optional[str] = None) -> "StorageLocation":
        """
        Per default a storage location for a user-account can be built based on the organization:urn
        If your account has access to various storage locations you can browse and select by Name

        :param name: (Optional) Name of the storage location if you want to select a non "master" location.
        :return: A :func:`~contentPlatformSDK.repository.StorageLocation` object or None
        """
        matching_locations = [
            storage_location
            for storage_location in self.get_storage_locations()
            # if name is None then we return the first location
            if storage_location.name == (name or storage_location.name)
        ]
        if matching_locations:
            return matching_locations[0]

        raise FileNotFoundError(f"Storage location with name {name} not found")

    def get_content_of_directory(
        self, storage: "StorageLocation", route: str, show_deleted: bool = False
    ) -> List[ContentsOfDirectory]:
        aws_key = storage.get_location_with_path(route, is_folder=True)
        logger.info(f"Getting content of directory {aws_key}")
        folder = self.client._query_api_dict(
            "repository",
            query={
                "operationName": "filefolderlistwitharchive",
                "variables": {"id": aws_key, "show_deleted": show_deleted},
                "query": """
                    query filefolderlistwitharchive($id: ID!, $show_deleted: Boolean) {
                        folder(id: $id) {
                            id
                            name
                            folders {
                                id
                                name
                            }
                            files(show_deleted: $show_deleted) {
                                id
                                name
                                size
                                last_modified
                                deleted
                                archived
                                archive {
                                    restore_state
                                    expiration
                                    extra {
                                        restore_tier
                                        restore_eta
                                    }
                                }
                             }
                        }
                    }""",
            },
            content_key="folder",
        )
        return folder["folders"] + folder["files"]  # type: ignore

    def create_upload_ticket(self, aws_key: str, message: str) -> str:
        """
        Create a sharable, authenticated upload link which can be used as HTML/IFRAME or in UploadClient.

        :param aws_key: Defines a storage location and folder path to which you want to upload
        :param message: A message that will be shown to the user if this url is accessed via a browser
        :return: HTTP URL
        """
        logger.info(f"Creating upload ticket for {aws_key}")
        upload_payload = self.client._query_api_dict(
            "repository",
            query={
                "operationName": "create_upload_ticket",
                "variables": {"folder_id": aws_key, "message": message},
                "query": """
                    mutation create_upload_ticket($folder_id: ID!, $message: String!) {
                        createUploadTicket(input: {
                            folder_id: $folder_id, message: $message
                        }) {
                            directory
                            token
                            url
                        }
                    }""",
            },
            content_key="createUploadTicket",
        )
        return upload_payload["url"]


class StorageLocation:
    """
    The StorageLocation class technically represents a root folder location accessible by the user
    """

    def __init__(self, config: dict, repository: Repository) -> None:
        self.name = config["name"]
        self.bucket = urlparse(config["id"]).netloc
        self.path = urlparse(config["id"]).path.lstrip("/")
        self.repository = repository

    @property
    def full_location(self) -> str:
        return f"s3://{self.bucket}/{self.path}"

    def get_location_with_path(self, path: str, is_folder: bool = False) -> str:
        full_path = self.full_location + path
        return full_path + "/" if not full_path.endswith("/") and is_folder else full_path

    def create_upload_client(self, path: str, message: str = "") -> "UploadClient":
        """
        :param path: Defines a folder path to which you want to upload within the StorageLocation
        :param message: A message that will be shown to the user if this url is accessed via a browser
        :return: A URL which can be used in the
        """
        return UploadClient(self, path, message)


class UploadClient:
    """
    This client allows the user to upload files programmatically to a storage location
    """

    def __init__(self, storage_location: StorageLocation, path: str, message: str) -> None:
        self._storage_location = storage_location
        self._message = message
        self._aws_s3_client = None

        full_path = storage_location.path + path
        self._path = full_path if full_path.endswith("/") else full_path + "/"

        aws_key = storage_location.get_location_with_path(path, is_folder=True)
        self.upload_url = storage_location.repository.create_upload_ticket(aws_key, self._message)

    @property
    def aws_s3_client(self) -> Any:
        """
        Based on the upload-ticket the user can retrieve an AWS BOTO3 S3 client

        :return: Boto3 S3 client
        """
        if not self._aws_s3_client:
            # authenticate with the uploader tool
            uploader_auth_request = Request(url=self.upload_url.replace("/#/", "/api_v1/upload/"), method="GET")
            uploader_auth_response = urlopen(uploader_auth_request).read().decode()
            uploader_auth_json = json.loads(uploader_auth_response)
            aws_session = boto3.Session(
                aws_access_key_id=uploader_auth_json["AccessKeyId"],
                aws_secret_access_key=uploader_auth_json["SecretAccessKey"],
                aws_session_token=uploader_auth_json["SessionToken"],
                region_name="us-east-1",
            )
            self._aws_s3_client = aws_session.client("s3")
            return self.aws_s3_client

        return self._aws_s3_client

    def upload_file(self, file_name: str) -> bool:
        """
        Programmatically upload a file to the storage location

        :param file_name: Local file path of the file to upload
        :return: True if successfully uploaded. An error is raised otherwise.
        """
        # Todo: a callback for progress tracking could be established:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#the-callback-parameter
        object_name = self._path + os.path.basename(file_name)
        self.aws_s3_client.upload_file(file_name, self._storage_location.bucket, object_name)
        return True

    def generate_presigned_url(self, expiration: int = 3600) -> Dict[str, str | Dict[str, str]]:
        """
        Generate a presigned URL to share an object

        :param object_name: The object name to share
        :param expiration: The time in seconds for the presigned URL to remain valid
        :return: The presigned URL
        """
        return self.aws_s3_client.generate_presigned_post(
            Bucket=self._storage_location.bucket,
            Key=self._path,
            ExpiresIn=expiration,
            Fields={"x-amz-server-side-encryption": "AES256"},
            Conditions=[
                {"x-amz-server-side-encryption": "AES256"},
            ],
        )
