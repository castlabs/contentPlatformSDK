import os
import time
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
    # Get upload credentials
    folder = "test_folder"
    remote_path = f"{folder}/{os.path.basename(TEST_VIDEO_PATH)}"
    credentials = platform.get_upload_credentials(remote_path)

    # Use a 'with' statement to ensure the file is closed
    with open(TEST_VIDEO_PATH, "rb") as f:
        response = requests.post(
            credentials.url,
            data=credentials.fields,
            files={"file": (os.path.basename(TEST_VIDEO_PATH), f)},
        )

    # S3 returns 204 No Content on a successful POST upload
    assert response.status_code == 204

    # Wait up to 5 seconds for S3 to reflect the change
    for _ in range(5):
        files = platform.list_files(folder)
        if os.path.basename(TEST_VIDEO_PATH) in files:
            break
        time.sleep(1)

    # Verify the file exists in the folder we just uploaded to
    files = platform.list_files(folder)
    assert os.path.basename(TEST_VIDEO_PATH) in files


def test_get_groups(platform: ContentPlatform) -> None:

    assert "default_group" in platform.get_groups()
