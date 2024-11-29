# ContentPlatform SDK

The ContentPlatform SDK is a Python client for interfacing with the Castlabs platform. It provides a simplified interface for uploading, encoding, managing media files, and monitoring encoding workflows. The SDK uses secure API keys for authentication and supports both production and staging environments.

## Features

- File Management: Upload, list, and manage files on the Castlabs platform.
- Encoding: Initiate, monitor, and retrieve encoding results for video files.
- Custom Workflow Support: Easily map and manage custom workflows.
- Presigned Uploads: Generate presigned URLs for secure uploads.
- Status Monitoring: Retrieve the status of encodings in real-time.

## Installation

This project uses Poetry for dependency management. To get started:

1. Ensure Poetry is installed on your system. [Installation guide](https://python-poetry.org/docs/).
2. Install dependencies: poetry install
3. To activate the virtual environment: poetry shell

## Getting Started

### Setup

Before using the SDK, ensure you have the following:

1. Organization URN: Found in your Castlabs account settings.
2. User URN: Associated with your user account.
3. API Access Key: Key used for authentication.

#### Initialization

To initialize the SDK:

```python
from castlabs import ContentPlatform

platform = ContentPlatform(
organization_urn="your-organization-urn",
user_urn="your-user-urn",
api_access_key_id="your-api-access-key-id",
api_secret_access_key="your-api-secret-access-key",
)
```

## Example Usage

Here’s an example script demonstrating common tasks with the SDK:

```python
from castlabs import ContentPlatform
```

### Initialize the platform

```python
platform = ContentPlatform(
organization_urn="your-organization-urn",
user_urn="your-user-urn",
api_access_key_id="your-api-access-key-id",
api_secret_access_key="your-api-secret-access-key",
)
```

### Upload a file

```python
local_file_path = "test_files/sherwood.mp4"
remote_path = platform.upload_file(local_file_path)
print(f"Uploaded file to: {remote_path}")
```

### List files in the remote directory

remote_directory = "video_1242"
files = platform.list_files(remote_directory)
print(f"Files in directory: {files}")

### Generate Presigned URL

Generate presigned credentials for secure uploads:

```python
remote_path = "video_141241"
credentials = platform.get_upload_credentials(remote_path)
requests.post(
        credentials.url,
        data=credentials.fields,
        files={"file": (os.path.basename(TEST_VIDEO_PATH), open(TEST_VIDEO_PATH, "rb"))},
    )
```

#### Encoding

Start encoding for an uploaded file:

```python
remote_path = "media/video.mp4"
encoding = platform.start_encoding(
remote_path,
group_name="default_group",
template="cmaf-abr",
webhook_url="https://example.com/webhook",
)
print(f"Encoding started. Status: {encoding.status}, Content URL: {encoding.content_url}")
```

The template can be changed to specify how the content should be encoded. The default
profile provides a good set of encoding options for automatic bit rate streaming.

#### Check Encoding Status

Retrieve the status of an encoding:

```python
status = platform.get_status(remote_path="media/video.mp4")
print(f"Encoding Status: {status.status}, HLS URL: {status.hls_url}")
```

#### List Encoding Groups

Retrieve a list of encoding groups:

```python
groups = platform.get_groups()
print(f"Encoding groups: {groups}")
```

### API Documentation

Initialization

```python
ContentPlatform(
organization_urn: str,
user_urn: str,
api_secret_access_key: str,
api_access_key_id: str,
environment: Literal["production", "staging"] = "production",
)
```

### Methods

#### `upload_file(file_path: str, remote_path: Optional[str] = None) -> str`

Uploads a local file to the Castlabs repository.

- file_path: Path to the local file.
- remote_path: Optional remote path. If not provided, a default will be generated.

#### `read_files(path: str) -> List[str]`

Lists files in the specified directory.

- remote_path: Path to the directory.

#### `get_upload_credentials(remote_path: str) -> UploadCredentials`

Generates presigned credentials for secure uploads.

- remote_path: Path to upload to.

#### `start_encoding(remote_path: str, group_na me: str = "default_group", encode_name: Optional[str] = None, template: str = "cmaf-abr", webhook_url: Optional[str] = None) -> Encoding`

Starts an encoding job for the specified file.

- remote_path: Path to the file to encode.
- group_name: Group name for the encoding job.
- encode_name: Optional name for the encoding job.
- template: Encoding template to use (default: "cmaf-abr").
- webhook_url: Optional URL for encoding status updates.

#### `get_status(remote_path: Optional[str] = None, group_name: str = "default_group", encode_name: Optional[str] = None) -> Encoding`

Gets the status of an encoding job.

- remote_path: Path to the file being encoded.
- group_name: Group name of the encoding job.
- encode_name: Name of the encoding job.

#### `get_groups() -> List[str]`

Returns a list of available encoding groups.

## Testing

To ensure the reliability and accuracy of the ContentPlatform SDK, we use `pytest` for testing. This allows for structured, automated testing of all SDK functionalities.

### Prerequisites for Testing

Before running the tests, ensure you have the following:

1. **Python Environment**: Ensure you have set up the virtual environment using `poetry install` and activated it with `poetry shell`.
2. **Environment Variables**: A `.env` file must be configured with the required API credentials.

### Setting Up the `.env` File

The `.env` file should contain the necessary credentials and settings required to interact with the Castlabs API during testing. An example file, [.env.example](.env.example), is provided in the repository. You can copy it and modify the values as needed:

The file should look something like this:

```bash
# This value is provided by Castlabs
ORGANIZATION_URN = "urn:janus:organization:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# See https://account.castlabs.com/account to get the following values
USER_URN = "urn:janus:user:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_ACCESS_KEY_ID = "urn:janus:accesskey:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_SECRET_ACCESS_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for feature requests or bugs.

## License

This SDK is licensed under the Apache2 License. See the LICENSE file for details.
