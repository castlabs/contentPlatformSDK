# Content Repository API

Content Repository API deals with basic content operations on File and Folder level.

##### Contact

castLabs Support

[support@castlans.com](mailto:support@castlans.com)

[https://castlabs.atlassian.net/servicedesk/customer/portals](https://castlabs.atlassian.net/servicedesk/customer/portals)

##### API Endpoints

```
https://repository.content.castlabs.com/graphql
```

##### Headers

```
# The OAuth2 access token as aquired during login process. Must be included in all API calls.
Authorization: <YOUR_ACCESS_TOKEN_HERE>
```

##### Version

1.0.0

# Queries

## `file`

##### Description

Retrieves information about a specific file, identified by its `id`.

##### Response

Returns a [`File`](#definition-File)

##### Arguments

| Name                           | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| `id` - [`ID!`](#definition-ID) | ID of the file. E.g. s3://bucket/path/filename.mp4 |

#### Example

##### Query

```gql
query file($id: ID!) {
  file(id: $id) {
    id
    name
    last_modified
    size
    archived
    archive {
      ...ArchiveFragment
    }
    tracks {
      ...TrackFragment
    }
    tags {
      ...TagFragment
    }
    ffprobe
    warnings
    extra_info
    mediainfo_json
    mediainfo
    stills {
      ...StillFragment
    }
    deleted
  }
}
```

##### Variables

```json
{ "id": "4" }
```

##### Response

```json
{
  "data": {
    "file": {
      "id": "4",
      "name": "xyz789",
      "last_modified": "abc123",
      "size": 123.45,
      "archived": false,
      "archive": Archive,
      "tracks": [Track],
      "tags": [Tag],
      "ffprobe": [AWSJSON],
      "warnings": [AWSJSON],
      "extra_info": AWSJSON,
      "mediainfo_json": [AWSJSON],
      "mediainfo": "xyz789",
      "stills": [Still],
      "deleted": false
    }
  }
}
```

[Queries](#group-Operations-Queries)

## `folder`

##### Description

Retrieves information about a folder, identified by its `id`. Use `id` value 's3://' to retrieve information about all available buckets.

##### Response

Returns a [`Folder`](#definition-Folder)

##### Arguments

| Name                           | Description                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `id` - [`ID!`](#definition-ID) | The unique identifier for the new folder, expressed as a URL. Example: s3://my-bucket/folder/new-folder |

#### Example

##### Query

```gql
query folder($id: ID!) {
  folder(id: $id) {
    id
    name
    folders {
      ...FolderFragment
    }
    files {
      ...FileFragment
    }
    tags {
      ...TagFragment
    }
    parents {
      ...FolderFragment
    }
  }
}
```

##### Variables

```json
{ "id": 4 }
```

##### Response

```json
{
  "data": {
    "folder": {
      "id": 4,
      "name": "abc123",
      "folders": [Folder],
      "files": [File],
      "tags": [Tag],
      "parents": [Folder]
    }
  }
}
```

[Queries](#group-Operations-Queries)

## `organizations`

##### Description

Returns a list of organizations the user is a member of.

##### Response

Returns an [`OrganizationPayload`](#definition-OrganizationPayload)

#### Example

##### Query

```gql
query organizations {
  organizations {
    organizations {
      ...OrganizationFragment
    }
  }
}
```

##### Response

```json
{
  "data": {
    "organizations": {"organizations": [Organization]}
  }
}
```

[Queries](#group-Operations-Queries)

## `policies`

##### Description

Returns a PermissionPayload document for the user requesting it. This information can be used to determine which actions should be displayed or hidden in a user interface.

##### Response

Returns a [`PolicyPayload`](#definition-PolicyPayload)

#### Example

##### Query

```gql
query policies {
  policies {
    organization {
      ...OrganizationFragment
    }
    licensedServices
    policies {
      ...PolicyFragment
    }
  }
}
```

##### Response

```json
{
  "data": {
    "policies": {
      "organization": Organization,
      "licensedServices": ["abc123"],
      "policies": [Policy]
    }
  }
}
```

[Queries](#group-Operations-Queries)

## `process`

##### Description

Retrieves information about a specific process, identified by its `id`.

##### Response

Returns a [`ProcessPayload`](#definition-ProcessPayload)

##### Arguments

| Name                           | Description                            |
| ------------------------------ | -------------------------------------- |
| `id` - [`ID!`](#definition-ID) | The unique identifier for the process. |

#### Example

##### Query

```gql
query process($id: ID!) {
  process(id: $id) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{ "id": 4 }
```

##### Response

```json
{
  "data": {
    "process": {
      "id": "4",
      "state": "FAILED",
      "data": "xyz789",
      "message": "abc123",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Queries](#group-Operations-Queries)

## `roots`

##### Response

Returns [`[Folder!]!`](#definition-Folder)

#### Example

##### Query

```gql
query roots {
  roots {
    id
    name
    folders {
      ...FolderFragment
    }
    files {
      ...FileFragment
    }
    tags {
      ...TagFragment
    }
    parents {
      ...FolderFragment
    }
  }
}
```

##### Response

```json
{
  "data": {
    "roots": [
      {
        "id": 4,
        "name": "xyz789",
        "folders": [Folder],
        "files": [File],
        "tags": [Tag],
        "parents": [Folder]
      }
    ]
  }
}
```

[Queries](#group-Operations-Queries)

## `search`

No longer supported

##### Description

DEPRECATED: Returns a list of SearchResult objects for a given SearchInput object.

##### Response

Returns [`[SearchResult]`](#definition-SearchResult)

##### Arguments

| Name                                               | Description |
| -------------------------------------------------- | ----------- |
| `input` - [`SearchInput`](#definition-SearchInput) |             |

#### Example

##### Query

```gql
query search($input: SearchInput) {
  search(input: $input) {
    location
    type
    timestamp
    title
    ids {
      ...IdSearchResultIdFragment
    }
    tags {
      ...TagSearchResultFragment
    }
  }
}
```

##### Variables

```json
{"input": SearchInput}
```

##### Response

```json
{
  "data": {
    "search": [
      {
        "location": "4",
        "type": "abc123",
        "timestamp": AWSDateTime,
        "title": "abc123",
        "ids": [IdSearchResultId],
        "tags": [TagSearchResult]
      }
    ]
  }
}
```

[Queries](#group-Operations-Queries)

## `search_ids`

No longer supported

##### Description

DEPRECATED: Returns a list of SearchResult objects for a specified `id` and `relation`.

##### Response

Returns [`[SearchResult]`](#definition-SearchResult)

##### Arguments

| Name                                        | Description |
| ------------------------------------------- | ----------- |
| `id` - [`String!`](#definition-String)      |             |
| `relation` - [`String`](#definition-String) |             |
| `type` - [`String`](#definition-String)     |             |

#### Example

##### Query

```gql
query search_ids($id: String!, $relation: String, $type: String) {
  search_ids(id: $id, relation: $relation, type: $type) {
    location
    type
    timestamp
    title
    ids {
      ...IdSearchResultIdFragment
    }
    tags {
      ...TagSearchResultFragment
    }
  }
}
```

##### Variables

```json
{
  "id": "xyz789",
  "relation": "xyz789",
  "type": "abc123"
}
```

##### Response

```json
{
  "data": {
    "search_ids": [
      {
        "location": "4",
        "type": "abc123",
        "timestamp": AWSDateTime,
        "title": "xyz789",
        "ids": [IdSearchResultId],
        "tags": [TagSearchResult]
      }
    ]
  }
}
```

[Queries](#group-Operations-Queries)

## `search_metadata`

No longer supported

##### Description

DEPRECATED: Returns a MetadataSearchResult for a search term.

##### Response

Returns a [`MetadataSearchResult`](#definition-MetadataSearchResult)

##### Arguments

| Name                                            | Description |
| ----------------------------------------------- | ----------- |
| `search_term` - [`String!`](#definition-String) |             |

#### Example

##### Query

```gql
query search_metadata($search_term: String!) {
  search_metadata(search_term: $search_term) {
    hits {
      ...HitFragment
    }
  }
}
```

##### Variables

```json
{ "search_term": "xyz789" }
```

##### Response

```json
{"data": {"search_metadata": {"hits": [Hit]}}}
```

[Queries](#group-Operations-Queries)

## `userProfile`

##### Response

Returns a [`UserProfilePayload`](#definition-UserProfilePayload)

#### Example

##### Query

```gql
query userProfile {
  userProfile {
    staff
    name
    email
  }
}
```

##### Response

```json
{
  "data": {
    "userProfile": {
      "staff": true,
      "name": "xyz789",
      "email": "abc123"
    }
  }
}
```

# Mutations

## `copy_file`

##### Description

Trigger a copy process of a file to a new location.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                    | Description |
| ------------------------------------------------------- | ----------- |
| `input` - [`CopyFileInput!`](#definition-CopyFileInput) |             |

#### Example

##### Query

```gql
mutation copy_file($input: CopyFileInput!) {
  copy_file(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": CopyFileInput}
```

##### Response

```json
{
  "data": {
    "copy_file": {
      "id": 4,
      "state": "FAILED",
      "data": "abc123",
      "message": "abc123",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `createUploadTicket`

##### Description

Creates a new upload ticket for a folder. The ticket can be used to upload files to the folder using the AWS S3 multipart upload API.

##### Response

Returns an [`UploadTicketPayload!`](#definition-UploadTicketPayload)

##### Arguments

| Name                                                                        | Description |
| --------------------------------------------------------------------------- | ----------- |
| `input` - [`CreateUploadTicketInput!`](#definition-CreateUploadTicketInput) |             |

#### Example

##### Query

```gql
mutation createUploadTicket($input: CreateUploadTicketInput!) {
  createUploadTicket(input: $input) {
    directory
    token
    url
  }
}
```

##### Variables

```json
{"input": CreateUploadTicketInput}
```

##### Response

```json
{
  "data": {
    "createUploadTicket": {
      "directory": "abc123",
      "token": "abc123",
      "url": "abc123"
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `delete`

##### Description

Delete a file.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                               | Description |
| -------------------------------------------------- | ----------- |
| `input` - [`DeleteInput`](#definition-DeleteInput) |             |

#### Example

##### Query

```gql
mutation delete($input: DeleteInput) {
  delete(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": DeleteInput}
```

##### Response

```json
{"data": {"delete": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `generateDownloadUrl`

##### Description

Generates a short lived download URL for eligable content

##### Response

Returns a [`DownloadUrlPayload!`](#definition-DownloadUrlPayload)

##### Arguments

| Name                                                          | Description |
| ------------------------------------------------------------- | ----------- |
| `input` - [`DownloadUrlInput!`](#definition-DownloadUrlInput) |             |

#### Example

##### Query

```gql
mutation generateDownloadUrl($input: DownloadUrlInput!) {
  generateDownloadUrl(input: $input) {
    signed_url
  }
}
```

##### Variables

```json
{"input": DownloadUrlInput}
```

##### Response

```json
{
  "data": {
    "generateDownloadUrl": {
      "signed_url": "abc123"
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `generate_stills`

##### Description

Trigger generation of still images of the first video track of the file.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                  | Description |
| ----------------------------------------------------- | ----------- |
| `input` - [`RefreshInput!`](#definition-RefreshInput) |             |

#### Example

##### Query

```gql
mutation generate_stills($input: RefreshInput!) {
  generate_stills(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": RefreshInput}
```

##### Response

```json
{
  "data": {
    "generate_stills": {
      "id": 4,
      "state": "FAILED",
      "data": "abc123",
      "message": "xyz789",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `mkdir`

##### Description

Creates a directory.

##### Response

Returns a [`MkdirPayload!`](#definition-MkdirPayload)

##### Arguments

| Name                                              | Description |
| ------------------------------------------------- | ----------- |
| `input` - [`MkdirInput!`](#definition-MkdirInput) |             |

#### Example

##### Query

```gql
mutation mkdir($input: MkdirInput!) {
  mkdir(input: $input) {
    created
    parent {
      ...FolderFragment
    }
  }
}
```

##### Variables

```json
{"input": MkdirInput}
```

##### Response

```json
{"data": {"mkdir": {"created": false, "parent": Folder}}}
```

[Mutations](#group-Operations-Mutations)

## `move_file`

##### Description

Trigger a move process of a file to a new location.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                    | Description |
| ------------------------------------------------------- | ----------- |
| `input` - [`CopyFileInput!`](#definition-CopyFileInput) |             |

#### Example

##### Query

```gql
mutation move_file($input: CopyFileInput!) {
  move_file(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": CopyFileInput}
```

##### Response

```json
{
  "data": {
    "move_file": {
      "id": "4",
      "state": "FAILED",
      "data": "xyz789",
      "message": "abc123",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `previewGenerate`

##### Description

The previewGenerate process does generate the actual preview.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                                  | Description |
| --------------------------------------------------------------------- | ----------- |
| `input` - [`PreviewGenerateInput!`](#definition-PreviewGenerateInput) |             |

#### Example

##### Query

```gql
mutation previewGenerate($input: PreviewGenerateInput!) {
  previewGenerate(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": PreviewGenerateInput}
```

##### Response

```json
{
  "data": {
    "previewGenerate": {
      "id": 4,
      "state": "FAILED",
      "data": "xyz789",
      "message": "abc123",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `previewGenerateToken`

##### Description

Generates a short lived DRMtoday upfront auth token from an existing playback allowance generated by a previewGenerate Mutation.

##### Response

Returns a [`PreviewTokenPayload!`](#definition-PreviewTokenPayload)

##### Arguments

| Name                                                                            | Description |
| ------------------------------------------------------------------------------- | ----------- |
| `input` - [`GeneratePreviewTokenInput!`](#definition-GeneratePreviewTokenInput) |             |

#### Example

##### Query

```gql
mutation previewGenerateToken($input: GeneratePreviewTokenInput!) {
  previewGenerateToken(input: $input) {
    access_token
    drmtoday_token
    asset_id
    dash_url
    hls_url
  }
}
```

##### Variables

```json
{"input": GeneratePreviewTokenInput}
```

##### Response

```json
{
  "data": {
    "previewGenerateToken": {
      "access_token": "xyz789",
      "drmtoday_token": "xyz789",
      "asset_id": "abc123",
      "dash_url": "abc123",
      "hls_url": "xyz789"
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `previewPrepare`

##### Description

The previewPrepare process performs preparatory steps to generate a preview for a folder.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                                | Description |
| ------------------------------------------------------------------- | ----------- |
| `input` - [`PreviewPrepareInput!`](#definition-PreviewPrepareInput) |             |

#### Example

##### Query

```gql
mutation previewPrepare($input: PreviewPrepareInput!) {
  previewPrepare(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": PreviewPrepareInput}
```

##### Response

```json
{
  "data": {
    "previewPrepare": {
      "id": "4",
      "state": "FAILED",
      "data": "xyz789",
      "message": "abc123",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `publishProcessComplete`

##### Description

Internal: Publishes that a Process has been completed to message its subscriptions.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                   | Description |
| ------------------------------------------------------ | ----------- |
| `result` - [`ProcessInput!`](#definition-ProcessInput) |             |

#### Example

##### Query

```gql
mutation publishProcessComplete($result: ProcessInput!) {
  publishProcessComplete(result: $result) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"result": ProcessInput}
```

##### Response

```json
{
  "data": {
    "publishProcessComplete": {
      "id": "4",
      "state": "FAILED",
      "data": "xyz789",
      "message": "xyz789",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `refreshBasicQc`

##### Description

Trigger a refresh of the basic QC of the file.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                                  | Description |
| ----------------------------------------------------- | ----------- |
| `input` - [`RefreshInput!`](#definition-RefreshInput) |             |

#### Example

##### Query

```gql
mutation refreshBasicQc($input: RefreshInput!) {
  refreshBasicQc(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": RefreshInput}
```

##### Response

```json
{"data": {"refreshBasicQc": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `refreshExtra`

##### Description

Trigger a refresh of the extra data.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                                  | Description |
| ----------------------------------------------------- | ----------- |
| `input` - [`RefreshInput!`](#definition-RefreshInput) |             |

#### Example

##### Query

```gql
mutation refreshExtra($input: RefreshInput!) {
  refreshExtra(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": RefreshInput}
```

##### Response

```json
{"data": {"refreshExtra": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `refreshFFProbe`

##### Description

Trigger a refresh of the ffprobe data.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                                  | Description |
| ----------------------------------------------------- | ----------- |
| `input` - [`RefreshInput!`](#definition-RefreshInput) |             |

#### Example

##### Query

```gql
mutation refreshFFProbe($input: RefreshInput!) {
  refreshFFProbe(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": RefreshInput}
```

##### Response

```json
{"data": {"refreshFFProbe": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `refreshMediaInfo`

##### Description

Trigger a refresh of the mediainfo and mediainfo_json properties.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                                  | Description |
| ----------------------------------------------------- | ----------- |
| `input` - [`RefreshInput!`](#definition-RefreshInput) |             |

#### Example

##### Query

```gql
mutation refreshMediaInfo($input: RefreshInput!) {
  refreshMediaInfo(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": RefreshInput}
```

##### Response

```json
{"data": {"refreshMediaInfo": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `refreshTracks`

##### Description

Trigger a refresh of the tracks property.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                                  | Description |
| ----------------------------------------------------- | ----------- |
| `input` - [`RefreshInput!`](#definition-RefreshInput) |             |

#### Example

##### Query

```gql
mutation refreshTracks($input: RefreshInput!) {
  refreshTracks(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": RefreshInput}
```

##### Response

```json
{"data": {"refreshTracks": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `registerWebhook`

##### Description

Registers a webhook to the process.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                                  | Description |
| --------------------------------------------------------------------- | ----------- |
| `input` - [`RegisterWebhookInput!`](#definition-RegisterWebhookInput) |             |

#### Example

##### Query

```gql
mutation registerWebhook($input: RegisterWebhookInput!) {
  registerWebhook(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": RegisterWebhookInput}
```

##### Response

```json
{
  "data": {
    "registerWebhook": {
      "id": "4",
      "state": "FAILED",
      "data": "xyz789",
      "message": "xyz789",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `restore`

##### Description

Trigger restore of an archived file.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name                                                          | Description |
| ------------------------------------------------------------- | ----------- |
| `input` - [`RestoreFileInput!`](#definition-RestoreFileInput) |             |

#### Example

##### Query

```gql
mutation restore($input: RestoreFileInput!) {
  restore(input: $input) {
    id
    state
    data
    message
    action
    start_date
    end_date
  }
}
```

##### Variables

```json
{"input": RestoreFileInput}
```

##### Response

```json
{
  "data": {
    "restore": {
      "id": 4,
      "state": "FAILED",
      "data": "xyz789",
      "message": "abc123",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `tag_folder`

##### Description

Apply tags to a folder.

##### Response

Returns a [`TagFolderPayload!`](#definition-TagFolderPayload)

##### Arguments

| Name                                                     | Description |
| -------------------------------------------------------- | ----------- |
| `input` - [`TagFolderInput`](#definition-TagFolderInput) |             |

#### Example

##### Query

```gql
mutation tag_folder($input: TagFolderInput) {
  tag_folder(input: $input) {
    folder {
      ...FolderFragment
    }
  }
}
```

##### Variables

```json
{"input": TagFolderInput}
```

##### Response

```json
{"data": {"tag_folder": {"folder": Folder}}}
```

[Mutations](#group-Operations-Mutations)

## `undelete`

##### Description

Undelete a file.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                            | Description |
| ----------------------------------------------- | ----------- |
| `input` - [`FileInput!`](#definition-FileInput) |             |

#### Example

##### Query

```gql
mutation undelete($input: FileInput!) {
  undelete(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": FileInput}
```

##### Response

```json
{"data": {"undelete": {"file": File}}}
```

[Mutations](#group-Operations-Mutations)

## `updateFile`

##### Description

Use to update mutable file info.

##### Response

Returns an [`UpdateFilePayload!`](#definition-UpdateFilePayload)

##### Arguments

| Name                                                        | Description |
| ----------------------------------------------------------- | ----------- |
| `input` - [`UpdateFileInput!`](#definition-UpdateFileInput) |             |

#### Example

##### Query

```gql
mutation updateFile($input: UpdateFileInput!) {
  updateFile(input: $input) {
    file {
      ...FileFragment
    }
  }
}
```

##### Variables

```json
{"input": UpdateFileInput}
```

##### Response

```json
{"data": {"updateFile": {"file": File}}}
```

# Types

## AWSDateTime

##### Description

The AWSDateTime scalar type provided by AWS AppSync, represents a valid extended ISO 8601 DateTime string. In other words, this scalar type accepts datetime strings of the form YYYY-MM-DDThh:mm:ss.SSSZ. The scalar can also accept "negative years" of the form -YYYY which correspond to years before 0000. For example, "-2017-01-01T00:00Z" and "-9999-01-01T00:00Z" are both valid datetime strings. The field after the two digit seconds field is a nanoseconds f ield. It can accept between 1 and 9 digits. So, for example, "1970-01-01T12:00:00.2Z", "1970-01-01T12:00:00.277Z" and "1970-01-01T12:00:00.123456789Z" are all valid datetime strings. The seconds and nanoseconds fields are optional (the seconds field must be specified if the nanoseconds field is to be used). The time zone offset is compulsory for this scalar. The time zone offset must either be Z (representing the UTC time zone) or be in the format ±hh:mm:ss. The seconds field in the timezone offset will be considered valid even though it is not part of the ISO 8601 standard.

##### Example

```gql
AWSDateTime
```

[Types](#group-Types)

## AWSJSON

##### Description

The AWSJSON scalar type provided by AWS AppSync, represents a JSON string that complies with RFC 8259. Maps like "{"upvotes": 10}", lists like "\[1,2,3\]", and scalar values like ""AWSJSON example string"", "1", and "true" are accepted as valid JSON and will automatically be parsed and loaded in the resolver mapping templates as Maps, Lists, or Scalar values rather than as the literal input strings. Invalid JSON strings like "{a: 1}", "{'a': 1}" and "Unquoted string" will throw GraphQL validation errors.

##### Example

```gql
AWSJSON
```

[Types](#group-Types)

## AWSURL

##### Description

The AWSURL scalar type provided by AWS AppSync, represents a valid URL string (Ex: [https://www.amazon.com/](https://www.amazon.com/)). The URL may use any scheme and may also be a local URL (Ex: [http://localhost/](http://localhost/)). URLs without schemes like "amazon.com" or "[www.amazon.com](http://www.amazon.com)" are considered invalid. URLs which contain double slashes (two consecutive forward slashes) in their path are also considered invalid.

##### Example

```gql
AWSURL
```

[Types](#group-Types)

## Archive

##### Fields

| Field Name                                                    | Description                                                                           |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `restore_state` - [`RestoreState!`](#definition-RestoreState) | Restoration state of the object if any                                                |
| `expiration` - [`String`](#definition-String)                 | If restore_state=RESTORED this field has ISO formatted timestamp with timezone offset |
| `extra` - [`ExtraArchiveInfo`](#definition-ExtraArchiveInfo)  | Extra archive info which usually requires additional requests to access               |

##### Example

```json
{
  "restore_state": "ARCHIVED",
  "expiration": "abc123",
  "extra": ExtraArchiveInfo
}
```

[Types](#group-Types)

## Boolean

##### Description

The `Boolean` scalar type represents `true` or `false`.

##### Example

```json
true
```

[Types](#group-Types)

## Condition

##### Description

Represents a condition in a statement.

##### Fields

| Field Name                                    | Description                                      |
| --------------------------------------------- | ------------------------------------------------ |
| `operator` - [`String!`](#definition-String)  | The condition operator, such as "StringLike".    |
| `key` - [`String!`](#definition-String)       | The condition key, such as "input.vtk_template". |
| `values` - [`[String!]!`](#definition-String) | The condition value.                             |

##### Example

```json
{
  "operator": "xyz789",
  "key": "xyz789",
  "values": ["xyz789"]
}
```

[Types](#group-Types)

## CopyFileInput

##### Fields

| Input Field                              | Description                                               |
| ---------------------------------------- | --------------------------------------------------------- |
| `src` - [`String!`](#definition-String)  | ID of the source file. Typically expressed as S3 URL      |
| `dest` - [`String!`](#definition-String) | ID of the destination file. Typically expressed as S3 URL |

##### Example

```json
{
  "src": "xyz789",
  "dest": "xyz789"
}
```

[Types](#group-Types)

## CreateUploadTicketInput

##### Description

Input type for the createUploadProcess mutation.

##### Fields

| Input Field                                 | Description                                                                                             |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `folder_id` - [`ID!`](#definition-ID)       | The unique identifier for the new folder, expressed as a URL. Example: s3://my-bucket/folder/new-folder |
| `message` - [`String!`](#definition-String) | Message for the uploader                                                                                |

##### Example

```json
{ "folder_id": 4, "message": "abc123" }
```

[Types](#group-Types)

## DeleteInput

##### Fields

| Input Field                                                 | Description                                                  |
| ----------------------------------------------------------- | ------------------------------------------------------------ |
| `id` - [`ID!`](#definition-ID)                              | ID of the file or folder to be deleted. E.g. s3://bucket/... |
| `deletionTime` - [`DeletionTime`](#definition-DeletionTime) |                                                              |

##### Example

```json
{ "id": 4, "deletionTime": "NOW" }
```

[Types](#group-Types)

## DeletionTime

##### Values

| Enum Value      | Description |
| --------------- | ----------- |
| `NOW`           |             |
| `IN_THREE_DAYS` |             |

##### Example

```gql
"NOW"
```

[Types](#group-Types)

## DownloadUrlInput

##### Fields

| Input Field                         | Description                                        |
| ----------------------------------- | -------------------------------------------------- |
| `file_id` - [`ID!`](#definition-ID) | ID of the file. E.g. s3://bucket/path/filename.mp4 |

##### Example

```json
{ "file_id": 4 }
```

[Types](#group-Types)

## DownloadUrlPayload

##### Fields

| Field Name                                     | Description |
| ---------------------------------------------- | ----------- |
| `signed_url` - [`String!`](#definition-String) |             |

##### Example

```json
{ "signed_url": "abc123" }
```

[Types](#group-Types)

## ExtraArchiveInfo

##### Fields

| Field Name                                                | Description |
| --------------------------------------------------------- | ----------- |
| `restore_tier` - [`RestoreTier`](#definition-RestoreTier) |             |
| `restore_eta` - [`String`](#definition-String)            |             |

##### Example

```json
{
  "restore_tier": "RESTORE_TIER_1",
  "restore_eta": "xyz789"
}
```

[Types](#group-Types)

## File

##### Fields

| Field Name                                             | Description                                                                                                                       |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `id` - [`ID!`](#definition-ID)                         | ID of the file. E.g. s3://bucket/path/filename.mp4                                                                                |
| `name` - [`String!`](#definition-String)               | Human-readable name of the file. Typically the last part of the file's ID                                                         |
| `last_modified` - [`String!`](#definition-String)      | Date of last modification in ISO 8601 format. This can be considered to be the upload date/time.                                  |
| `size` - [`Float!`](#definition-Float)                 | Size of the file in bytes                                                                                                         |
| `archived` - [`Boolean!`](#definition-Boolean)         | If true the file is in long term storage and cannot be accessed immediately, else it is usable without taking any further action. |
| `archive` - [`Archive`](#definition-Archive)           | It's set for archived objects regardless where those are currently restored or not. otherwise it's not set.                       |
| `tracks` - [`[Track!]`](#definition-Track)             | Information about the file's tracks.                                                                                              |
| `tags` - [`[Tag!]`](#definition-Tag)                   | Tags assigned to the file.                                                                                                        |
| `ffprobe` - [`[AWSJSON!]`](#definition-AWSJSON)        | Contains the streams property of the file's ffprobe output.                                                                       |
| `warnings` - [`[AWSJSON!]`](#definition-AWSJSON)       | Contains the streams warnings - output of basic qc process.                                                                       |
| `extra_info` - [`AWSJSON`](#definition-AWSJSON)        | Contains the extra stream-specific information.                                                                                   |
| `mediainfo_json` - [`[AWSJSON!]`](#definition-AWSJSON) | Contains the mediainfo's JSON representation of the file.                                                                         |
| `mediainfo` - [`String`](#definition-String)           | Contains the mediainfo's textual output.                                                                                          |
| `stills` - [`[Still]!`](#definition-Still)             | Array of generated still images of the first video track of the file.                                                             |
| `deleted` - [`Boolean!`](#definition-Boolean)          | True if deleted but not yet purged from storage.                                                                                  |

##### Example

```json
{
  "id": "4",
  "name": "xyz789",
  "last_modified": "xyz789",
  "size": 123.45,
  "archived": false,
  "archive": Archive,
  "tracks": [Track],
  "tags": [Tag],
  "ffprobe": [AWSJSON],
  "warnings": [AWSJSON],
  "extra_info": AWSJSON,
  "mediainfo_json": [AWSJSON],
  "mediainfo": "xyz789",
  "stills": [Still],
  "deleted": false
}
```

[Types](#group-Types)

## FileInput

##### Fields

| Input Field                         | Description                                        |
| ----------------------------------- | -------------------------------------------------- |
| `file_id` - [`ID!`](#definition-ID) | ID of the file. E.g. s3://bucket/path/filename.mp4 |

##### Example

```json
{ "file_id": 4 }
```

[Types](#group-Types)

## Float

##### Description

The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).

##### Example

```json
987.65
```

[Types](#group-Types)

## Folder

##### Fields

| Field Name                                                                      | Description                                                                                                                                               |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id` - [`ID!`](#definition-ID)                                                  | The unique ID of the folder, expressed as a S3 URL, e.g. s3://bucket/path.                                                                                |
| `name` - [`String!`](#definition-String)                                        | A human-readable name for the folder, typically the last part of the folder's ID or short name of the bucket.                                             |
| `folders` - [`[Folder!]!`](#definition-Folder)                                  | A list of all sub-folders within this folder.                                                                                                             |
| `files` - [`[File!]!`](#definition-File)                                        | A list of all files within this folder. The `show_deleted` argument can be set to `true` to include deleted files that have not been purged from storage. |
| ##### Arguments<br><br>###### `show_deleted` - [`Boolean`](#definition-Boolean) |                                                                                                                                                           |
| `tags` - [`[Tag!]`](#definition-Tag)                                            | A list of tags assigned to this folder.                                                                                                                   |
| `parents` - [`[Folder!]!`](#definition-Folder)                                  | A list of this folder's parent folders.                                                                                                                   |

##### Example

```json
{
  "id": "4",
  "name": "xyz789",
  "folders": [Folder],
  "files": [File],
  "tags": [Tag],
  "parents": [Folder]
}
```

[Types](#group-Types)

## GeneratePreviewTokenInput

##### Description

Input type for the `previewGenerateToken` mutation, used to generate a token for accessing preview files.

##### Fields

| Input Field                                 | Description                                                                                                  |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `asset_id` - [`String`](#definition-String) | The `asset_id` of the preview file set, as returned in the `data` property of the `previewGenerate` process. |

##### Example

```json
{ "asset_id": "xyz789" }
```

[Types](#group-Types)

## Hit

##### Fields

| Field Name                                         | Description |
| -------------------------------------------------- | ----------- |
| `key` - [`String`](#definition-String)             |             |
| `brefix` - [`String!`](#definition-String)         |             |
| `tracks` - [`[Track!]`](#definition-Track)         |             |
| `ffprobe` - [`AWSJSON`](#definition-AWSJSON)       |             |
| `warnings` - [`AWSJSON`](#definition-AWSJSON)      |             |
| `extra_info` - [`AWSJSON`](#definition-AWSJSON)    |             |
| `mediainfo` - [`String`](#definition-String)       |             |
| `SequenceNumber` - [`String!`](#definition-String) |             |
| `timestamp` - [`String!`](#definition-String)      |             |

##### Example

```json
{
  "key": "xyz789",
  "brefix": "xyz789",
  "tracks": [Track],
  "ffprobe": AWSJSON,
  "warnings": AWSJSON,
  "extra_info": AWSJSON,
  "mediainfo": "xyz789",
  "SequenceNumber": "abc123",
  "timestamp": "abc123"
}
```

[Types](#group-Types)

## ID

##### Description

The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.

##### Example

```gql
"4"
```

[Types](#group-Types)

## IdSearchResultId

##### Fields

| Field Name                                  | Description |
| ------------------------------------------- | ----------- |
| `type` - [`String!`](#definition-String)    |             |
| `relation` - [`String`](#definition-String) |             |
| `domain` - [`String`](#definition-String)   |             |
| `value` - [`String!`](#definition-String)   |             |

##### Example

```json
{
  "type": "abc123",
  "relation": "xyz789",
  "domain": "abc123",
  "value": "xyz789"
}
```

[Types](#group-Types)

## Int

##### Description

The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

##### Example

```json
987
```

[Types](#group-Types)

## MetadataSearchResult

##### Fields

| Field Name                           | Description |
| ------------------------------------ | ----------- |
| `hits` - [`[Hit!]`](#definition-Hit) |             |

##### Example

```json
{"hits": [Hit]}
```

[Types](#group-Types)

## MkdirInput

##### Description

The input for the `mkdir` mutation, used to create a new folder in the underlying storage system.

##### Fields

| Input Field                           | Description                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `folder_id` - [`ID!`](#definition-ID) | The unique identifier for the new folder, expressed as a URL. Example: s3://my-bucket/folder/new-folder |

##### Example

```json
{ "folder_id": 4 }
```

[Types](#group-Types)

## MkdirPayload

##### Description

The return value of the mkdir permission, indicating whether a folder was created or not.

##### Fields

| Field Name                                   | Description                                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `created` - [`Boolean`](#definition-Boolean) | A boolean indicating whether the folder was actually created (true) or already existed (false).   |
| `parent` - [`Folder!`](#definition-Folder)   | The parent folder of the newly created folder, which can be used to update the client-side state. |

##### Example

```json
{"created": false, "parent": Folder}
```

[Types](#group-Types)

## Organization

##### Description

Represents an organization.

##### Fields

| Field Name                                      | Description                              |
| ----------------------------------------------- | ---------------------------------------- |
| `id` - [`ID!`](#definition-ID)                  | The unique ID of the organization.       |
| `name` - [`String!`](#definition-String)        | The name of the organization.            |
| `legacy_name` - [`String!`](#definition-String) | The legacy/api name of the organization. |

##### Example

```json
{
  "id": "4",
  "name": "xyz789",
  "legacy_name": "xyz789"
}
```

[Types](#group-Types)

## OrganizationPayload

##### Description

The list of organizations the user is a member of.

##### Fields

| Field Name                                                       | Description                               |
| ---------------------------------------------------------------- | ----------------------------------------- |
| `organizations` - [`[Organization!]!`](#definition-Organization) | The organization document in JSON format. |

##### Example

```json
{"organizations": [Organization]}
```

[Types](#group-Types)

## Policy

##### Description

Represents a policy in the system.

##### Fields

| Field Name                                              | Description                             |
| ------------------------------------------------------- | --------------------------------------- |
| `display_name` - [`String!`](#definition-String)        | The display name of the policy.         |
| `statements` - [`[Statement!]!`](#definition-Statement) | The statements that make up the policy. |

##### Example

```json
{
  "display_name": "xyz789",
  "statements": [Statement]
}
```

[Types](#group-Types)

## PolicyPayload

##### Description

Represents the payload/return value of a permission request.

##### Fields

| Field Name                                                  | Description                             |
| ----------------------------------------------------------- | --------------------------------------- |
| `organization` - [`Organization`](#definition-Organization) |                                         |
| `licensedServices` - [`[String!]!`](#definition-String)     | The permission document in JSON format. |
| `policies` - [`[Policy!]!`](#definition-Policy)             |                                         |

##### Example

```json
{
  "organization": Organization,
  "licensedServices": ["xyz789"],
  "policies": [Policy]
}
```

[Types](#group-Types)

## PreviewGenerateInput

##### Description

Input type to the `previewGenerate` mutation.

##### Fields

| Input Field                           | Description                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `folder_id` - [`ID!`](#definition-ID) | The unique identifier for the new folder, expressed as a URL. Example: s3://my-bucket/folder/new-folder |

##### Example

```json
{ "folder_id": "4" }
```

[Types](#group-Types)

## PreviewPrepareInput

##### Description

Input type to the `previewPrepare` mutation.

##### Fields

| Input Field                           | Description                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `folder_id` - [`ID!`](#definition-ID) | The unique identifier for the new folder, expressed as a URL. Example: s3://my-bucket/folder/new-folder |

##### Example

```json
{ "folder_id": "4" }
```

[Types](#group-Types)

## PreviewTokenPayload

##### Description

The PreviewTokenPayload entity holds all the necessary information for playing a preview.

##### Fields

| Field Name                                        | Description                                                                                                                                                                 |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `access_token` - [`String`](#definition-String)   | The access token provides authorization for accessing the encrypted DASH or HLS files and their respective manifests. Reference: Token-based Access Control for DASH (TAC). |
| `drmtoday_token` - [`String`](#definition-String) | The DRMtoday upfront token authorizes the delivery of the required license for playback.                                                                                    |
| `asset_id` - [`String!`](#definition-String)      | The unique identifier for the preview's asset, as specified in the previewGenerateToken mutation.                                                                           |
| `dash_url` - [`String`](#definition-String)       | The HTTPS URL for the DASH manifest, used for playback.                                                                                                                     |
| `hls_url` - [`String`](#definition-String)        | The HTTPS URL for the HLS manifest, used for playback.                                                                                                                      |

##### Example

```json
{
  "access_token": "xyz789",
  "drmtoday_token": "xyz789",
  "asset_id": "xyz789",
  "dash_url": "xyz789",
  "hls_url": "abc123"
}
```

[Types](#group-Types)

## ProcessInput

##### Description

Input type used to update a process subscription.

##### Fields

| Input Field                                                   | Description                                                                                                                                 |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `id` - [`ID!`](#definition-ID)                                | Unique identifier for the process.                                                                                                          |
| `state` - [`ProcessStateEnum!`](#definition-ProcessStateEnum) | Current state of the process.                                                                                                               |
| `data` - [`String`](#definition-String)                       | Optional additional information related to the action performed by the process. Typically set only when the process is in a terminal state. |
| `message` - [`String`](#definition-String)                    | Progress message to provide updates on the process status to the client.                                                                    |
| `action` - [`String`](#definition-String)                     | Type of action being performed by the process.                                                                                              |

##### Example

```json
{
  "id": "4",
  "state": "FAILED",
  "data": "xyz789",
  "message": "abc123",
  "action": "xyz789"
}
```

[Types](#group-Types)

## ProcessPayload

##### Fields

| Field Name                                                    | Description                                                                                                                                      |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id` - [`ID!`](#definition-ID)                                | A unique identifier for the process.                                                                                                             |
| `state` - [`ProcessStateEnum!`](#definition-ProcessStateEnum) | The current state of the process.                                                                                                                |
| `data` - [`String`](#definition-String)                       | Additional information related to the action performed by the process. This field is typically only set when the process is in a terminal state. |
| `message` - [`String`](#definition-String)                    | A message indicating the progress of the process. This can be used to provide updates on the process' status to the client.                      |
| `action` - [`String`](#definition-String)                     | The type of action being performed by the process.                                                                                               |
| `start_date` - [`AWSDateTime`](#definition-AWSDateTime)       | The date and time the process was created.                                                                                                       |
| `end_date` - [`AWSDateTime`](#definition-AWSDateTime)         | The date and time the process ended.                                                                                                             |

##### Example

```json
{
  "id": 4,
  "state": "FAILED",
  "data": "xyz789",
  "message": "abc123",
  "action": "abc123",
  "start_date": AWSDateTime,
  "end_date": AWSDateTime
}
```

[Types](#group-Types)

## ProcessStateEnum

##### Description

Enumeration of possible states of a process.

##### Values

| Enum Value    | Description                                                                                               |
| ------------- | --------------------------------------------------------------------------------------------------------- |
| `FAILED`      | The process has failed. The `message` and/or `data` property contains further details.                    |
| `IN_PROGRESS` | The process is still running. The `message` field contains information about the current state.           |
| `SUCCESS`     | The process finished successfully. If the process has a result, it will be available in the `data` field. |

##### Example

```gql
"FAILED"
```

[Types](#group-Types)

## RefreshInput

##### Fields

| Input Field                                | Description                                                                                         |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `file_id` - [`ID!`](#definition-ID)        | ID of the file. E.g. s3://bucket/path/filename.mp4                                                  |
| `force` - [`Boolean`](#definition-Boolean) | When force is true the refresh will be performed disregarding any existing values. Default = `true` |

##### Example

```json
{ "file_id": "4", "force": false }
```

[Types](#group-Types)

## RegisterWebhookInput

##### Fields

| Input Field                                     | Description |
| ----------------------------------------------- | ----------- |
| `process_id` - [`ID!`](#definition-ID)          |             |
| `webhook_url` - [`AWSURL!`](#definition-AWSURL) |             |

##### Example

```json
{"process_id": 4, "webhook_url": AWSURL}
```

[Types](#group-Types)

## RestoreFileInput

##### Description

Input type for the `restore` Mutation.

##### Fields

| Input Field                                       | Description                       |
| ------------------------------------------------- | --------------------------------- |
| `files` - [`[ID]`](#definition-ID)                | A list of file IDs to be restored |
| `tier` - [`RestoreTier`](#definition-RestoreTier) |                                   |
| `days` - [`Int`](#definition-Int)                 |                                   |

##### Example

```json
{ "files": [4], "tier": "RESTORE_TIER_1", "days": 987 }
```

[Types](#group-Types)

## RestoreState

##### Values

| Enum Value  | Description                                                                          |
| ----------- | ------------------------------------------------------------------------------------ |
| `ARCHIVED`  | The object is archived, not restored and restoration isn't started                   |
| `RESTORING` | Restoration is in progress. ETA can be read from the ArchiveState struct             |
| `RESTORED`  | The archived object is restored. Expiration can be read from the ArchiveState struct |

##### Example

```gql
"ARCHIVED"
```

[Types](#group-Types)

## RestoreTier

##### Values

| Enum Value       | Description |
| ---------------- | ----------- |
| `RESTORE_TIER_1` |             |
| `RESTORE_TIER_2` |             |
| `RESTORE_TIER_3` |             |

##### Example

```gql
"RESTORE_TIER_1"
```

[Types](#group-Types)

## SearchInput

##### Description

The SearchInput input object is used to execute a search query in the system. It defines the parameters for the search query, such as the starting index of the result set, the size of the result set, and the Elasticsearch query in the form of a JSON document.

##### Fields

| Input Field                                               | Description                                                              |
| --------------------------------------------------------- | ------------------------------------------------------------------------ |
| `from` - [`Int`](#definition-Int)                         | Specifies the starting index (0-based) of the result set to be returned. |
| `size` - [`Int`](#definition-Int)                         | Specifies the number of results to be returned in the result set.        |
| `query_fragment_json` - [`AWSJSON!`](#definition-AWSJSON) | The Elasticsearch query to be executed, represented as a JSON document.  |

##### Example

```json
{"from": 123, "size": 123, "query_fragment_json": AWSJSON}
```

[Types](#group-Types)

## SearchResult

##### Fields

| Field Name                                                     | Description |
| -------------------------------------------------------------- | ----------- |
| `location` - [`ID!`](#definition-ID)                           |             |
| `type` - [`String!`](#definition-String)                       |             |
| `timestamp` - [`AWSDateTime`](#definition-AWSDateTime)         |             |
| `title` - [`String!`](#definition-String)                      |             |
| `ids` - [`[IdSearchResultId!]!`](#definition-IdSearchResultId) |             |
| `tags` - [`[TagSearchResult!]!`](#definition-TagSearchResult)  |             |

##### Example

```json
{
  "location": "4",
  "type": "abc123",
  "timestamp": AWSDateTime,
  "title": "abc123",
  "ids": [IdSearchResultId],
  "tags": [TagSearchResult]
}
```

[Types](#group-Types)

## Statement

##### Description

Represents a statement in a policy.

##### Fields

| Field Name                                             | Description                                            |
| ------------------------------------------------------ | ------------------------------------------------------ |
| `effect` - [`String!`](#definition-String)             | The effect of the statement, either "allow" or "deny". |
| `actions` - [`[String!]!`](#definition-String)         | The actions that the statement applies to.             |
| `resources` - [`[String!]`](#definition-String)        | The resources that the statement applies to.           |
| `conditions` - [`[Condition!]`](#definition-Condition) | The conditions under which the statement is true.      |

##### Example

```json
{
  "effect": "abc123",
  "actions": ["abc123"],
  "resources": ["abc123"],
  "conditions": [Condition]
}
```

[Types](#group-Types)

## Still

##### Description

Represents a single still image.

##### Fields

| Field Name                               | Description                            |
| ---------------------------------------- | -------------------------------------- |
| `name` - [`String!`](#definition-String) | The human-readable name of the file.   |
| `url` - [`AWSURL!`](#definition-AWSURL)  | A signed URL to the actual image file. |

##### Example

```json
{
  "name": "xyz789",
  "url": AWSURL
}
```

[Types](#group-Types)

## String

##### Description

The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.

##### Example

```gql
"abc123"
```

[Types](#group-Types)

## Tag

##### Description

A Tag represents a key-value pair that is attached to a `File` or `Folder` object.

##### Fields

| Field Name                                | Description                              |
| ----------------------------------------- | ---------------------------------------- |
| `key` - [`String!`](#definition-String)   | The unique identifier for the tag key.   |
| `value` - [`String!`](#definition-String) | The corresponding value for the tag key. |

##### Example

```json
{
  "key": "abc123",
  "value": "xyz789"
}
```

[Types](#group-Types)

## TagFolderInput

##### Description

Input type for the tag_folder mutation.

##### Fields

| Input Field                                    | Description                                                                                             |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `folder_id` - [`ID!`](#definition-ID)          | The unique identifier for the new folder, expressed as a URL. Example: s3://my-bucket/folder/new-folder |
| `tags` - [`[TagInput!]`](#definition-TagInput) | The tags to be assigned to the folder.                                                                  |

##### Example

```json
{"folder_id": 4, "tags": [TagInput]}
```

[Types](#group-Types)

## TagFolderPayload

##### Description

Represents the payload/return value of the tag_folder mutation.

##### Fields

| Field Name                                 | Description                              |
| ------------------------------------------ | ---------------------------------------- |
| `folder` - [`Folder!`](#definition-Folder) | The updated folder object after tagging. |

##### Example

```json
{"folder": Folder}
```

[Types](#group-Types)

## TagInput

##### Description

Input type for the tag key-value pair.

##### Fields

| Input Field                              | Description                          |
| ---------------------------------------- | ------------------------------------ |
| `key` - [`String!`](#definition-String)  | The key for the tag.                 |
| `value` - [`String`](#definition-String) | The corresponding value for the tag. |

##### Example

```json
{
  "key": "xyz789",
  "value": "abc123"
}
```

[Types](#group-Types)

## TagSearchResult

##### Description

Represents the search result of a tag.

##### Fields

| Field Name                                | Description           |
| ----------------------------------------- | --------------------- |
| `name` - [`String!`](#definition-String)  | The name of the tag.  |
| `value` - [`String!`](#definition-String) | The value of the tag. |

##### Example

```json
{
  "name": "xyz789",
  "value": "abc123"
}
```

[Types](#group-Types)

## Track

##### Description

Represents a track within a media file.

##### Fields

| Field Name                                           | Description                                                                                                           |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `index` - [`Int!`](#definition-Int)                  | The index of the track as defined by the container format. 0 for raw media files.                                     |
| `enabled` - [`Boolean!`](#definition-Boolean)        | If disabled, it will not be used for any workflow.                                                                    |
| `language` - [`String!`](#definition-String)         | The language of the track, represented using a BCP-47 code.                                                           |
| `track_type` - [`TrackType!`](#definition-TrackType) | The type of the track, either close caption, subtitle, video, audio, or image. Immutable when audio, video, or image. |

##### Example

```json
{
  "index": 123,
  "enabled": false,
  "language": "abc123",
  "track_type": "video"
}
```

[Types](#group-Types)

## TrackInput

##### Fields

| Input Field                                          | Description |
| ---------------------------------------------------- | ----------- |
| `index` - [`Int!`](#definition-Int)                  |             |
| `track_type` - [`TrackType!`](#definition-TrackType) |             |
| `language` - [`String!`](#definition-String)         |             |
| `enabled` - [`Boolean!`](#definition-Boolean)        |             |

##### Example

```json
{
  "index": 987,
  "track_type": "video",
  "language": "xyz789",
  "enabled": true
}
```

[Types](#group-Types)

## TrackType

##### Values

| Enum Value      | Description |
| --------------- | ----------- |
| `video`         |             |
| `audio`         |             |
| `subtitle`      |             |
| `closedcaption` |             |
| `image`         |             |
| `data`          |             |

##### Example

```gql
"video"
```

[Types](#group-Types)

## UpdateFileInput

##### Description

Input type for `updateFile` mutation.

##### Fields

| Input Field                                         | Description                                        |
| --------------------------------------------------- | -------------------------------------------------- |
| `file_id` - [`ID!`](#definition-ID)                 | ID of the file. E.g. s3://bucket/path/filename.mp4 |
| `tracks` - [`[TrackInput]`](#definition-TrackInput) |                                                    |
| `tags` - [`[TagInput]`](#definition-TagInput)       |                                                    |

##### Example

```json
{
  "file_id": 4,
  "tracks": [TrackInput],
  "tags": [TagInput]
}
```

[Types](#group-Types)

## UpdateFilePayload

##### Description

Generic input type for several more specific file update mutations.

##### Fields

| Field Name                           | Description |
| ------------------------------------ | ----------- |
| `file` - [`File!`](#definition-File) |             |

##### Example

```json
{"file": File}
```

[Types](#group-Types)

## UploadTicketPayload

##### Fields

| Field Name                                    | Description |
| --------------------------------------------- | ----------- |
| `directory` - [`String!`](#definition-String) |             |
| `token` - [`String!`](#definition-String)     |             |
| `url` - [`String!`](#definition-String)       |             |

##### Example

```json
{
  "directory": "abc123",
  "token": "xyz789",
  "url": "abc123"
}
```

[Types](#group-Types)

## UserProfilePayload

##### Fields

| Field Name                                  | Description                      |
| ------------------------------------------- | -------------------------------- |
| `staff` - [`Boolean!`](#definition-Boolean) | Staff yes/no status of the user. |
| `name` - [`String!`](#definition-String)    | Name of the user.                |
| `email` - [`String!`](#definition-String)   | Email address of the user.       |

##### Example

```json
{
  "staff": false,
  "name": "abc123",
  "email": "xyz789"
}
```

[Documentation by Anvil SpectaQL](https://github.com/anvilco/spectaql)
