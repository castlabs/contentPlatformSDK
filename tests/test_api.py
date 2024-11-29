import os
from datetime import datetime, timedelta

import requests

from castlabs import ContentPlatform

TEST_VIDEO_PATH = "tests/test_data/test_video.mp4"


def test_end_to_end(platform: ContentPlatform) -> None:

    # Create a client which handles the authentication with the help of an API Key
    remote_path = platform.upload_file(TEST_VIDEO_PATH)
    assert platform.list_files(remote_path) == [os.path.basename(TEST_VIDEO_PATH)]

    # Start encoding
    status = platform.start_encoding(
        remote_path, webhook_url="https://webhook.site/fe3d7dcb-ad4b-4274-81e6-aad0251a2ed2"
    )

    # Wait for the encoding to finish
    start_time = datetime.now()
    timeout = start_time + timedelta(minutes=3)
    while start_time < timeout and not (status := platform.get_status(remote_path)).complete:
        print(f"Status: {status}")

    # Check if the encoding was successful using the encode name
    assert platform.get_status(encode_name=status.encode_name).status == "PUBLISH_SUCCESS"
    assert os.environ["ORGANIZATION_URN"] in status.hls_url
    assert os.environ["ORGANIZATION_URN"] in status.dash_url

    # Check we can download the files
    assert requests.get(status.hls_url).status_code == 200
    assert requests.get(status.dash_url).status_code == 200


def test_upload_url(platform: ContentPlatform) -> None:

    # Get a browser based upload URL
    assert platform.get_upload_url("test_folder").startswith("https://up.content.castlabs.com")
    assert platform.get_upload_url("test_folder").startswith("https://up.content.castlabs.com")

    # Get upload credentials
    credentials = platform.get_upload_credentials("test_folder")
    requests.post(
        credentials.url,
        data=credentials.fields,
        files={"file": (os.path.basename(TEST_VIDEO_PATH), open(TEST_VIDEO_PATH, "rb"))},
    )
    assert platform.list_files("test_folder") == [os.path.basename(TEST_VIDEO_PATH)]

    credentials_2 = platform.get_upload_credentials("test_folder_1")
    assert credentials_2.url == credentials.url
    assert credentials_2.fields != credentials.fields


def test_get_groups(platform: ContentPlatform) -> None:

    assert "default_group" in platform.get_groups()
