# Content Workflow API

##### API Endpoints

```
https://workflow.content.castlabs.com/graphql
```

##### Headers

```
# The OAuth2 access token as aquired during login process. Must be included in all API calls.
Authorization: <YOUR_ACCESS_TOKEN_HERE>
```

##### Version

1.0.0

# Queries

## `airlines`

##### Description

Retrieves a list of airlines suitable for building a user interface.

##### Response

Returns an [`AirlinesPayload`](#definition-AirlinesPayload)

#### Example

##### Query

```gql
query airlines {
  airlines {
    airlines {
      ...AirlineFragment
    }
  }
}
```

##### Response

```json
{"data": {"airlines": {"airlines": [Airline]}}}
```

[Queries](#group-Operations-Queries)

## `list_POs`

##### Description

Retrieves a list of POs filtered by airline, name, and/or date.

##### Response

Returns a [`POsPayload!`](#definition-POsPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`ListPOsInput!`](#definition-ListPOsInput) |     |

#### Example

##### Query

```gql
query list_POs($input: ListPOsInput!) {
  list_POs(input: $input) {
    pos {
      ...POFragment
    }
  }
}
```

##### Variables

```json
{"input": ListPOsInput}
```

##### Response

```json
{"data": {"list_POs": {"pos": [PO]}}}
```

[Queries](#group-Operations-Queries)

## `process`

##### Description

Retrieves the status information of a long-running process.

##### Response

Returns a [`ProcessPayload`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `id` - [`ID!`](#definition-ID) |     |

#### Example

##### Query

```gql
query process($id: ID!) {
  process(id: $id) {
    id
    input
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
{"id": "4"}
```

##### Response

```json
{
  "data": {
    "process": {
      "id": 4,
      "input": "xyz789",
      "state": "FAILED",
      "data": "xyz789",
      "message": "xyz789",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

# Mutations

## `deleteEncodesOfPoItem`

##### Response

Returns a [`POItem`](#definition-POItem)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`POItemInput!`](#definition-POItemInput) |     |

#### Example

##### Query

```gql
mutation deleteEncodesOfPoItem($input: POItemInput!) {
  deleteEncodesOfPoItem(input: $input) {
    id
    po_item_id
    customer
    po {
      ...POFragment
    }
    po_destination
    encodes {
      ...EncodeFragment
    }
    workflow_process {
      ...ProcessPayloadFragment
    }
    publish_process {
      ...ProcessPayloadFragment
    }
    filename
    input_brefix
    output_brefix
    watermark
    aspect_ratio
    vtk_template
    vtk_job {
      ...VtkJobFragment
    }
    vtk_jobs {
      ...VtkJobFragment
    }
    workflow
    tracks {
      ...TrackFragment
    }
    preview {
      ...POItemPreviewFragment
    }
    format_specific_data
    format_specific_data_json
    metadata_source
    wrap_up_workflow
    checkpoint_content_uploaded
    checkpoint_content_complete
    checkpoint_encodes_done
    checkpoint_metadata_available
    metadata_message
  }
}
```

##### Variables

```json
{"input": POItemInput}
```

##### Response

```json
{
  "data": {
    "deleteEncodesOfPoItem": {
      "id": 4,
      "po_item_id": "xyz789",
      "customer": "xyz789",
      "po": PO,
      "po_destination": "abc123",
      "encodes": [Encode],
      "workflow_process": ProcessPayload,
      "publish_process": ProcessPayload,
      "filename": "abc123",
      "input_brefix": "abc123",
      "output_brefix": "abc123",
      "watermark": true,
      "aspect_ratio": "xyz789",
      "vtk_template": "xyz789",
      "vtk_job": VtkJob,
      "vtk_jobs": [VtkJob],
      "workflow": "xyz789",
      "tracks": [Track],
      "preview": POItemPreview,
      "format_specific_data": AWSJSON,
      "format_specific_data_json": AWSJSON,
      "metadata_source": "abc123",
      "wrap_up_workflow": "abc123",
      "checkpoint_content_uploaded": true,
      "checkpoint_content_complete": false,
      "checkpoint_encodes_done": false,
      "checkpoint_metadata_available": false,
      "metadata_message": "xyz789"
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `publish`

##### Description

Publish given PO items and finalize PO.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`POInput`](#definition-POInput) | Input for the PO to publish. |

#### Example

##### Query

```gql
mutation publish($input: POInput) {
  publish(input: $input) {
    id
    input
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
{"input": POInput}
```

##### Response

```json
{
  "data": {
    "publish": {
      "id": "4",
      "input": "abc123",
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

## `publishPo`

No longer supported

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`POItemInput!`](#definition-POItemInput) |     |

#### Example

##### Query

```gql
mutation publishPo($input: POItemInput!) {
  publishPo(input: $input) {
    id
    input
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
{"input": POItemInput}
```

##### Response

```json
{
  "data": {
    "publishPo": {
      "id": "4",
      "input": "abc123",
      "state": "FAILED",
      "data": "abc123",
      "message": "abc123",
      "action": "abc123",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `publishPoItem`

##### Description

Publish a single PO item.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`POItemInput!`](#definition-POItemInput) | Input for the PO item to publish. |

#### Example

##### Query

```gql
mutation publishPoItem($input: POItemInput!) {
  publishPoItem(input: $input) {
    id
    input
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
{"input": POItemInput}
```

##### Response

```json
{
  "data": {
    "publishPoItem": {
      "id": "4",
      "input": "abc123",
      "state": "FAILED",
      "data": "xyz789",
      "message": "xyz789",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `registerWebhook`

##### Description

Registers a webhook to the process. The webhook will be called when the process reaches a terminal state.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`RegisterWebhookInput!`](#definition-RegisterWebhookInput) |     |

#### Example

##### Query

```gql
mutation registerWebhook($input: RegisterWebhookInput!) {
  registerWebhook(input: $input) {
    id
    input
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
      "input": "abc123",
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

## `restartPoItem`

##### Description

Restart a PO item that has failed or needs to be re-run for other reasons.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`POItemInput!`](#definition-POItemInput) |     |

#### Example

##### Query

```gql
mutation restartPoItem($input: POItemInput!) {
  restartPoItem(input: $input) {
    id
    input
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
{"input": POItemInput}
```

##### Response

```json
{
  "data": {
    "restartPoItem": {
      "id": "4",
      "input": "xyz789",
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

## `start_workflow_above_default`

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`StartWorkflowAboveDefaultInput!`](#definition-StartWorkflowAboveDefaultInput) |     |

#### Example

##### Query

```gql
mutation start_workflow_above_default($input: StartWorkflowAboveDefaultInput!) {
  start_workflow_above_default(input: $input) {
    id
    input
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
{"input": StartWorkflowAboveDefaultInput}
```

##### Response

```json
{
  "data": {
    "start_workflow_above_default": {
      "id": "4",
      "input": "abc123",
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

## `start_workflow_aerq_default`

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`StartWorkflowAerqDefaultInput!`](#definition-StartWorkflowAerqDefaultInput) |     |

#### Example

##### Query

```gql
mutation start_workflow_aerq_default($input: StartWorkflowAerqDefaultInput!) {
  start_workflow_aerq_default(input: $input) {
    id
    input
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
{"input": StartWorkflowAerqDefaultInput}
```

##### Response

```json
{
  "data": {
    "start_workflow_aerq_default": {
      "id": "4",
      "input": "xyz789",
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

## `start_workflow_default`

##### Description

Start a default content delivery workflow from an external ID.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`StartWorkflowDefaultInput!`](#definition-StartWorkflowDefaultInput) |     |

#### Example

##### Query

```gql
mutation start_workflow_default($input: StartWorkflowDefaultInput!) {
  start_workflow_default(input: $input) {
    id
    input
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
{"input": StartWorkflowDefaultInput}
```

##### Response

```json
{
  "data": {
    "start_workflow_default": {
      "id": "4",
      "input": "abc123",
      "state": "FAILED",
      "data": "xyz789",
      "message": "xyz789",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
```

[Mutations](#group-Operations-Mutations)

## `start_workflow_lsy_order`

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`StartWorkflowLsyInput!`](#definition-StartWorkflowLsyInput) |     |

#### Example

##### Query

```gql
mutation start_workflow_lsy_order($input: StartWorkflowLsyInput!) {
  start_workflow_lsy_order(input: $input) {
    id
    input
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
{"input": StartWorkflowLsyInput}
```

##### Response

```json
{
  "data": {
    "start_workflow_lsy_order": {
      "id": "4",
      "input": "abc123",
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

## `start_workflow_vod_batch`

##### Description

Start a VOD workflow that emits a number if individualized, watermarked streams.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`StartWorkflowVodInput!`](#definition-StartWorkflowVodInput) | Input for the VOD workflow. |

#### Example

##### Query

```gql
mutation start_workflow_vod_batch($input: StartWorkflowVodInput!) {
  start_workflow_vod_batch(input: $input) {
    id
    input
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
{"input": StartWorkflowVodInput}
```

##### Response

```json
{
  "data": {
    "start_workflow_vod_batch": {
      "id": "4",
      "input": "xyz789",
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

## `start_workflow_vod_default`

##### Description

Start a VOD workflow that emits a single stream.

##### Response

Returns a [`ProcessPayload!`](#definition-ProcessPayload)

##### Arguments

| Name | Description |
| --- | --- |
| `input` - [`StartWorkflowVodInput!`](#definition-StartWorkflowVodInput) | Input for the VOD workflow. |

#### Example

##### Query

```gql
mutation start_workflow_vod_default($input: StartWorkflowVodInput!) {
  start_workflow_vod_default(input: $input) {
    id
    input
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
{"input": StartWorkflowVodInput}
```

##### Response

```json
{
  "data": {
    "start_workflow_vod_default": {
      "id": "4",
      "input": "abc123",
      "state": "FAILED",
      "data": "abc123",
      "message": "xyz789",
      "action": "xyz789",
      "start_date": AWSDateTime,
      "end_date": AWSDateTime
    }
  }
}
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

## AWSEmail

##### Example

```gql
AWSEmail
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

## Airline

##### Description

Representation of an airline with its code, name, and possessive form. Even though the term airline is used, it also represents content recipients other than airlines.

##### Fields

| Field Name | Description |
| --- | --- |
| `iata_code` - [`String`](#definition-String) | Unique identifier for the airline / content recipient, such as the IATA 2-letter code. |
| `airline_name` - [`String`](#definition-String) | Name of the airline as displayed in the user interface. |
| `airline_possessive` - [`String`](#definition-String) | Possessive form of the airline name, such as "Austrian Airlines'" or "Aeroflot's". |
| `preview_organization` - [`String`](#definition-String) | DRMtoday organization used for previewing content. |
| `prod_organization` - [`String`](#definition-String) | DRMtoday organization used for controlling access to the production content. |

##### Example

```json
{
  "iata_code": "xyz789",
  "airline_name": "xyz789",
  "airline_possessive": "xyz789",
  "preview_organization": "abc123",
  "prod_organization": "abc123"
}
```

[Types](#group-Types)

## AirlinesPayload

##### Description

A list of airlines visible to the requesting user.

##### Fields

| Field Name | Description |
| --- | --- |
| `airlines` - [`[Airline!]!`](#definition-Airline) | list of airlines |

##### Example

```json
{"airlines": [Airline]}
```

[Types](#group-Types)

## Boolean

##### Description

The `Boolean` scalar type represents `true` or `false`.

[Types](#group-Types)

## CodecType

##### Values

| Enum Value | Description |
| --- | --- |
| `video` | Video track. |
| `audio` | Audio track. |
| `subtitle` | Subtitle track. |
| `closedcaption` | Closed caption track. |
| `image` | Image track/file. |

##### Example

```gql
"video"
```

[Types](#group-Types)

## Encode

##### Description

Represents a file produced as part of a workflow result.

##### Fields

| Field Name | Description |
| --- | --- |
| `id` - [`ID`](#definition-ID) | Unique identifier for the file, in the format of s3://bucket/path/filename.mp4. |
| `name` - [`String`](#definition-String) | Human-readable name of the file, typically the last part of the file's ID. |
| `size` - [`Float`](#definition-Float) | Size of the file in bytes. |
| `last_modified` - [`String`](#definition-String) | Last modification date of the file in ISO 8601 date string format. |

##### Example

```json
{
  "id": "4",
  "name": "xyz789",
  "size": 123.45,
  "last_modified": "abc123"
}
```

[Types](#group-Types)

## FilterAWSDateTimeInput

##### Fields

| Input Field | Description |
| --- | --- |
| `lt` - [`AWSDateTime`](#definition-AWSDateTime) |     |
| `gt` - [`AWSDateTime`](#definition-AWSDateTime) |     |
| `between` - [`[AWSDateTime!]`](#definition-AWSDateTime) |     |

##### Example

```json
{
  "lt": AWSDateTime,
  "gt": AWSDateTime,
  "between": [AWSDateTime]
}
```

[Types](#group-Types)

## FilterStringInput

##### Description

Used to filter items based on the value of a string property.

##### Fields

| Input Field | Description |
| --- | --- |
| `eq` - [`String`](#definition-String) | The result set will only include items whose property value matches the filter value. |

##### Example

```json
{"eq": "xyz789"}
```

[Types](#group-Types)

## Float

##### Description

The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).

##### Example

```json
123.45
```

[Types](#group-Types)

## ID

##### Description

The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.

##### Example

```json
4
```

[Types](#group-Types)

## Int

##### Description

The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

##### Example

```json
123
```

[Types](#group-Types)

## ListPOsInput

##### Fields

| Input Field | Description |
| --- | --- |
| `filter` - [`POFilter`](#definition-POFilter) |     |

##### Example

```json
{"filter": POFilter}
```

[Types](#group-Types)

## PO

##### Fields

| Field Name | Description |
| --- | --- |
| `id` - [`ID!`](#definition-ID) |     |
| `airline` - [`String!`](#definition-String) |     |
| `po_name` - [`ID!`](#definition-ID) |     |
| `date_created` - [`AWSDateTime`](#definition-AWSDateTime) |     |
| `date_due` - [`String`](#definition-String) |     |
| `target_system` - [`String`](#definition-String) |     |
| `poitems` - [`[POItem!]!`](#definition-POItem) |     |
| ##### Arguments<br><br>###### `po_item_id` - [`String`](#definition-String) |     |

##### Example

```json
{
  "id": "4",
  "airline": "xyz789",
  "po_name": "4",
  "date_created": AWSDateTime,
  "date_due": "abc123",
  "target_system": "abc123",
  "poitems": [POItem]
}
```

[Types](#group-Types)

## POFilter

##### Description

Input type for filtering Purchase Orders (POs)

##### Fields

| Input Field | Description |
| --- | --- |
| `airline` - [`FilterStringInput`](#definition-FilterStringInput) | Filter POs based on their airline name. |
| `po_name` - [`FilterStringInput`](#definition-FilterStringInput) | Filter POs based on their name. |
| `date_created` - [`FilterAWSDateTimeInput`](#definition-FilterAWSDateTimeInput) | Filter POs based on their creation date. |

##### Example

```json
{
  "airline": FilterStringInput,
  "po_name": FilterStringInput,
  "date_created": FilterAWSDateTimeInput
}
```

[Types](#group-Types)

## POInput

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) | name of the PO, consisting of the organization followed by an underscore and a custom name. |
| `skip_finalize` - [`Boolean!`](#definition-Boolean) | Whether or not to execute the workflow and format specific finalization of the PO. |
| `publish_po_item_ids` - [`[String!]!`](#definition-String) | An array of PO Item IDs that is to be published before the finalization. |

##### Example

```json
{
  "po_name": "xyz789",
  "skip_finalize": false,
  "publish_po_item_ids": ["abc123"]
}
```

[Types](#group-Types)

## POItem

##### Description

A single item in a Purchase Order (PO).

##### Fields

| Field Name | Description |
| --- | --- |
| `id` - [`ID`](#definition-ID) | Unique identifier for the PO item, consisting of the po name and po\_item\_id. |
| `po_item_id` - [`String!`](#definition-String) | Identifier for the PO item within the PO. |
| `customer` - [`String`](#definition-String) | Customer ID associated with the billing for this PO item. |
| `po` - [`PO`](#definition-PO) | The PO that this PO item belongs to. |
| `po_destination` - [`String`](#definition-String) | Destination for final delivery of the PO files. |
| `encodes` - [`[Encode!]!`](#definition-Encode) | Array of files produced to fulfill the PO item. |
| `workflow_process` - [`ProcessPayload`](#definition-ProcessPayload) | Feedback about the process that generated the output files. |
| `publish_process` - [`ProcessPayload`](#definition-ProcessPayload) | Feedback about the process that published the output files. |
| `filename` - [`String!`](#definition-String) | Output filename used to start the workflow, with varying meanings depending on workflow and output format. |
| `input_brefix` - [`String!`](#definition-String) | Internal: S3 bucket/prefix of the media source location. |
| `output_brefix` - [`String!`](#definition-String) | Internal: S3 bucket/prefix of the target location. |
| `watermark` - [`Boolean`](#definition-Boolean) | Indicator of whether to apply a forensic watermark according to APEX specification. |
| `aspect_ratio` - [`String`](#definition-String) | Aspect ratio: 4:3, 16:9, or pass-through (default). |
| `vtk_template` - [`String`](#definition-String) | Identifier of the selected encoding template. |
| `vtk_job` - [`VtkJob`](#definition-VtkJob) | use vtk\_jobs to cater for the possibility of multiple VTK jobs |
| `vtk_jobs` - [`[VtkJob!]!`](#definition-VtkJob) |     |
| `workflow` - [`String!`](#definition-String) | Type of workflow: above\_default, aerq\_default. |
| `tracks` - [`[Track!]!`](#definition-Track) | Array of requested tracks, with the source property populated when a suitable source track is identified. |
| `preview` - [`POItemPreview`](#definition-POItemPreview) | Information about the encode's preview, if available. |
| `format_specific_data` - [`AWSJSON`](#definition-AWSJSON) |     |
| `format_specific_data_json` - [`AWSJSON`](#definition-AWSJSON) |     |
| `metadata_source` - [`String`](#definition-String) |     |
| `wrap_up_workflow` - [`String`](#definition-String) |     |
| `checkpoint_content_uploaded` - [`Boolean`](#definition-Boolean) |     |
| `checkpoint_content_complete` - [`Boolean`](#definition-Boolean) |     |
| `checkpoint_encodes_done` - [`Boolean`](#definition-Boolean) |     |
| `checkpoint_metadata_available` - [`Boolean`](#definition-Boolean) |     |
| `metadata_message` - [`String`](#definition-String) |     |

##### Example

```json
{
  "id": 4,
  "po_item_id": "abc123",
  "customer": "abc123",
  "po": PO,
  "po_destination": "abc123",
  "encodes": [Encode],
  "workflow_process": ProcessPayload,
  "publish_process": ProcessPayload,
  "filename": "xyz789",
  "input_brefix": "xyz789",
  "output_brefix": "xyz789",
  "watermark": false,
  "aspect_ratio": "abc123",
  "vtk_template": "abc123",
  "vtk_job": VtkJob,
  "vtk_jobs": [VtkJob],
  "workflow": "xyz789",
  "tracks": [Track],
  "preview": POItemPreview,
  "format_specific_data": AWSJSON,
  "format_specific_data_json": AWSJSON,
  "metadata_source": "xyz789",
  "wrap_up_workflow": "abc123",
  "checkpoint_content_uploaded": false,
  "checkpoint_content_complete": false,
  "checkpoint_encodes_done": true,
  "checkpoint_metadata_available": false,
  "metadata_message": "xyz789"
}
```

[Types](#group-Types)

## POItemInput

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) | Name of the PO, consisting of the organization followed by an underscore and a custom name. |
| `po_item_id` - [`String!`](#definition-String) | Identifier for the PO item within the PO. |

##### Example

```json
{
  "po_name": "xyz789",
  "po_item_id": "xyz789"
}
```

[Types](#group-Types)

## POItemPreview

##### Description

Preview information for a Purchase Order (PO) item.

##### Fields

| Field Name | Description |
| --- | --- |
| `dash_manifest_url` - [`AWSURL`](#definition-AWSURL) | URL to the Dynamic Adaptive Streaming over HTTP (DASH) manifest, if available. |
| `dash_manifest_last_modified` - [`AWSDateTime`](#definition-AWSDateTime) | Last modified date of the DASH manifest. \[Informational\]. |
| `hls_manifest_url` - [`AWSURL`](#definition-AWSURL) | URL to the HTTP Live Streaming (HLS) master playlist, if available. |
| `hls_manifest_last_modified` - [`AWSDateTime`](#definition-AWSDateTime) | Last modified date of the HLS master playlist. \[Informational\]. |
| `access_token` - [`String`](#definition-String) | Access token for authorization to access encrypted DASH or HLS files and manifests. |
| `ab_token` - [`String`](#definition-String) | Session-specific token that must be included in all segment requests for generating a session-specific forensic watermark. |
| `drmtoday_token` - [`String`](#definition-String) | Short-lived DRMtoday upfront authentication token. |

##### Example

```json
{
  "dash_manifest_url": AWSURL,
  "dash_manifest_last_modified": AWSDateTime,
  "hls_manifest_url": AWSURL,
  "hls_manifest_last_modified": AWSDateTime,
  "access_token": "abc123",
  "ab_token": "abc123",
  "drmtoday_token": "xyz789"
}
```

[Types](#group-Types)

## POsPayload

##### Fields

| Field Name | Description |
| --- | --- |
| `pos` - [`[PO!]!`](#definition-PO) |     |

##### Example

```json
{"pos": [PO]}
```

[Types](#group-Types)

## ProcessPayload

##### Fields

| Field Name | Description |
| --- | --- |
| `id` - [`ID!`](#definition-ID) | A unique identifier for the process. |
| `input` - [`String`](#definition-String) | Input that was used to starrt the process. |
| `state` - [`ProcessStateEnum!`](#definition-ProcessStateEnum) | The current state of the process. |
| `data` - [`String`](#definition-String) | Additional information related to the action performed by the process. This field is typically only set when the process is in a terminal state. |
| `message` - [`String`](#definition-String) | A message indicating the progress of the process. This can be used to provide updates on the process' status to the client. |
| `action` - [`String`](#definition-String) | The type of action being performed by the process. |
| `start_date` - [`AWSDateTime`](#definition-AWSDateTime) | The date and time the process was created. |
| `end_date` - [`AWSDateTime`](#definition-AWSDateTime) | The date and time the process ended. |

##### Example

```json
{
  "id": 4,
  "input": "xyz789",
  "state": "FAILED",
  "data": "abc123",
  "message": "xyz789",
  "action": "abc123",
  "start_date": AWSDateTime,
  "end_date": AWSDateTime
}
```

[Types](#group-Types)

## ProcessStateEnum

##### Values

| Enum Value | Description |
| --- | --- |
| `FAILED` |     |
| `IN_PROGRESS` |     |
| `SUCCESS` |     |
| `ABORTED` |     |

##### Example

```gql
"FAILED"
```

[Types](#group-Types)

## RegisterWebhookInput

##### Description

Input for registering a webhook to a process.

When a process reaches a terminal state, the webhook will be called with a POST request containing the following JSON payload:

```
{
  "process_id": "process_id",
  "state": "state",
  "data": "data",
  "message": "message",
  "action": "action"
}
```

##### Fields

| Input Field | Description |
| --- | --- |
| `process_id` - [`ID!`](#definition-ID) | Unique identifier of the process to attach to. |
| `webhook_url` - [`AWSURL!`](#definition-AWSURL) | URL to call when the process reaches a terminal state. |

##### Example

```json
{
  "process_id": "4",
  "webhook_url": AWSURL
}
```

[Types](#group-Types)

## Source

##### Fields

| Field Name | Description |
| --- | --- |
| `codec_type` - [`String!`](#definition-String) | Type of the selected source track (audio, video, closed\_caption, subtitle, or image). Depending on the workflow, closed captioning may be delivered instead of subtitles. |
| `index` - [`Int!`](#definition-Int) | Index of the selected source track. |
| `key` - [`String!`](#definition-String) | Object key of the selected source file, excluding the bucket. |
| `lang` - [`String`](#definition-String) | Language of the selected track. Depending on the workflow, similar languages may be delivered, such as fr-CA for fr, or es-419 for es-ES. |

##### Example

```json
{
  "codec_type": "xyz789",
  "index": 123,
  "key": "abc123",
  "lang": "abc123"
}
```

[Types](#group-Types)

## StartWorkflowAboveDefaultInput

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) | Name of the PO, consisting of the target organization followed by an underscore and a custom name. Please use a basic character set. |
| `po_item_id` - [`String!`](#definition-String) | Identifier for the PO item within the PO. |
| `po_destination` - [`String`](#definition-String) | Destination for final delivery of the PO files. |
| `filename` - [`String!`](#definition-String) | Output filename used to start the workflow, with varying meanings depending on the workflow and output format. |
| `input_brefix` - [`String!`](#definition-String) | S3 bucket/prefix of the media source location. |
| `watermark` - [`Boolean!`](#definition-Boolean) | Indicator of whether to apply a visual watermark according to APEX specification. |
| `aspect_ratio` - [`String`](#definition-String) | Aspect ratio: 4:3, 16:9, or pass-through (default). |
| `vtk_template` - [`String!`](#definition-String) | Identifier of the encoding template to be used in this PO. |
| `format_specific_data` - [`AWSJSON`](#definition-AWSJSON) | VTK template-specific data structure. |
| `tracks` - [`[TrackInput!]!`](#definition-TrackInput) | Array of tracks to deliver. |
| `email_notification` - [`[AWSEmail!]`](#definition-AWSEmail) | List of email addresses to notify about success or failure of the workflow. |
| `auto_publish` - [`Boolean`](#definition-Boolean) | Publishes the PO item automatically after successful completion of the workflow when set to true. |

##### Example

```json
{
  "po_name": "abc123",
  "po_item_id": "abc123",
  "po_destination": "xyz789",
  "filename": "xyz789",
  "input_brefix": "xyz789",
  "watermark": false,
  "aspect_ratio": "xyz789",
  "vtk_template": "xyz789",
  "format_specific_data": AWSJSON,
  "tracks": [TrackInput],
  "email_notification": [AWSEmail],
  "auto_publish": true
}
```

[Types](#group-Types)

## StartWorkflowAerqDefaultInput

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) |     |
| `po_item_id` - [`String!`](#definition-String) |     |
| `input_brefix` - [`String!`](#definition-String) |     |
| `aerq_airline` - [`String!`](#definition-String) |     |
| `aerq_project` - [`String`](#definition-String) |     |
| `po_destination` - [`String`](#definition-String) |     |
| `filename` - [`String!`](#definition-String) |     |
| `aerq_version` - [`String!`](#definition-String) |     |
| `vtk_template` - [`String!`](#definition-String) |     |
| `format_specific_data` - [`AWSJSON`](#definition-AWSJSON) |     |
| `tracks` - [`[TrackInput!]!`](#definition-TrackInput) |     |

##### Example

```json
{
  "po_name": "abc123",
  "po_item_id": "abc123",
  "input_brefix": "abc123",
  "aerq_airline": "abc123",
  "aerq_project": "abc123",
  "po_destination": "xyz789",
  "filename": "abc123",
  "aerq_version": "abc123",
  "vtk_template": "xyz789",
  "format_specific_data": AWSJSON,
  "tracks": [TrackInput]
}
```

[Types](#group-Types)

## StartWorkflowDefaultInput

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) | Name of the PO, consisting of the airline's 2-letter IATA code followed by an underscore and a custom name. Please use a basic character set. |
| `po_item_id` - [`String!`](#definition-String) | Identifier for the PO item within the PO. |
| `po_destination` - [`String`](#definition-String) | Destination for final delivery of the PO files. |
| `filename` - [`String!`](#definition-String) | Output filename used to start the workflow, with varying meanings depending on the workflow and output format. |
| `content_identifier` - [`String!`](#definition-String) | Identifier of the source content. This is the ID of the content that is to be used as the source for the workflow. |
| `metadata_source` - [`String`](#definition-String) | This is the URL of the metadata source that is to be used for the workflow. |
| `wrap_up_workflow` - [`String`](#definition-String) | This is the URL of the metadata source that is to be used for the workflow. |
| `watermark` - [`Boolean!`](#definition-Boolean) | Indicator of whether to apply a visual watermark according to APEX specification. |
| `aspect_ratio` - [`String`](#definition-String) | Aspect ratio: 4:3, 16:9, or pass-through (default). |
| `vtk_template` - [`String!`](#definition-String) | Identifier of the encoding template to be used in this PO. |
| `format_specific_data` - [`AWSJSON`](#definition-AWSJSON) | VTK template-specific data structure. |
| `tracks` - [`[TrackInput!]!`](#definition-TrackInput) | Array of tracks to deliver. |
| `email_notification` - [`[AWSEmail!]`](#definition-AWSEmail) | List of email addresses to notify about success or failure of the workflow. |
| `auto_publish` - [`Boolean`](#definition-Boolean) | Publishes the PO item automatically after successful completion of the workflow when set to true. |

##### Example

```json
{
  "po_name": "xyz789",
  "po_item_id": "abc123",
  "po_destination": "xyz789",
  "filename": "xyz789",
  "content_identifier": "abc123",
  "metadata_source": "xyz789",
  "wrap_up_workflow": "abc123",
  "watermark": true,
  "aspect_ratio": "abc123",
  "vtk_template": "xyz789",
  "format_specific_data": AWSJSON,
  "tracks": [TrackInput],
  "email_notification": [AWSEmail],
  "auto_publish": false
}
```

[Types](#group-Types)

## StartWorkflowLsyInput

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) |     |
| `po_item_id` - [`String!`](#definition-String) |     |
| `po_destination` - [`String`](#definition-String) |     |
| `filename` - [`String!`](#definition-String) |     |
| `input_brefix` - [`String!`](#definition-String) | S3 bucket/prefix of the media source location. |
| `watermark` - [`Boolean!`](#definition-Boolean) | Indicator of whether to apply a watermark. |
| `aspect_ratio` - [`String`](#definition-String) |     |
| `vtk_template` - [`String!`](#definition-String) |     |
| `format_specific_data` - [`AWSJSON`](#definition-AWSJSON) |     |
| `tracks` - [`[TrackInput!]!`](#definition-TrackInput) |     |
| `email_notification` - [`[AWSEmail!]`](#definition-AWSEmail) |     |

##### Example

```json
{
  "po_name": "xyz789",
  "po_item_id": "abc123",
  "po_destination": "abc123",
  "filename": "xyz789",
  "input_brefix": "abc123",
  "watermark": true,
  "aspect_ratio": "xyz789",
  "vtk_template": "xyz789",
  "format_specific_data": AWSJSON,
  "tracks": [TrackInput],
  "email_notification": [AWSEmail]
}
```

[Types](#group-Types)

## StartWorkflowVodInput

##### Description

Input for the VOD workflow.

##### Fields

| Input Field | Description |
| --- | --- |
| `po_name` - [`String!`](#definition-String) | Name of the PO, prefixed with \[your\_org\_name\]-... . Please stick to a basic character set. |
| `po_item_id` - [`String!`](#definition-String) | Identifier for the PO item within the PO. |
| `input_brefix` - [`String!`](#definition-String) | source bucket/prefix of the media source location. |
| `auto_publish` - [`Boolean!`](#definition-Boolean) | Publishes the PO item automatically after successful completion of the workflow when set to true. |
| `po_destination` - [`String!`](#definition-String) | Destination for final delivery of the PO files. 'vod' is the only supported value at this time. |
| `vtk_template` - [`String!`](#definition-String) | VTK template to use for encode and encryption. 'cmaf-abr' is the only supported value at this time. |
| `format_specific_data` - [`AWSJSON`](#definition-AWSJSON) | VTK template-specific data structure. This JSON structure is specific to the VTK template used. The following keys are supported:<br><br>when `"watermark": "contentarmor/ab"` (vod-default workflow)<br><br>```<br>{<br>  "watermark":  "contentarmor/ab",<br>  "ab_shared_session_key": "[512 Bit base 64 encoded key]",<br>  "ab_payload_size": "4" \| "8" \|  "16" \| "24" \| "32",<br>}<br>```<br><br>when `"watermark": "stardust/sf"` (vod-default & vod-batch workflow)<br><br>```<br>{<br>  "watermark":  "stardust/sf",<br>  "sd_strength": "8",<br>  "sd_payload_size":  "8" \| "13" \|  "16" \| "24" \| "32",<br>  "sd_superpixel_density": [10 - 100],<br>  "sd_pixel_density": [10 -100],<br>  "sd_watermark":  1 <= x <= 2^sd_payload_size,  # for vod-default workflow<br>  "sd_watermarks":  [1 <= x <= 2^sd_payload_size, ..., 1 <= x <= 2^sd_payload_size], # for vod-batch workflow<br>}<br>```<br><br>when `"watermark": "contentarmor/embed"` (vod-batch workflow)<br><br>```<br>{<br>  "watermark": "contentarmor/embed",<br>  "ca_payload_size": "4" \| "8" \|  "16" \| "24" \| "32",<br>  "ca_watermarks": [1 <= x <= 2^sd_payload_size, ..., 1 <= x <= 2^sd_payload_size],<br>}<br>```<br><br>General options<br><br>```<br>"encrypt": true \| false,<br>```<br><br>encrypt and register DRM keys with DRMtoday yes/no<br><br>```<br>"thumbnail": true \| false,<br>```<br><br>generate thumbnails yes/no |
| `email_notification` - [`[AWSEmail!]`](#definition-AWSEmail) | List of email addresses to notify about success or failure of the workflow. |

##### Example

```json
{
  "po_name": "xyz789",
  "po_item_id": "abc123",
  "input_brefix": "xyz789",
  "auto_publish": false,
  "po_destination": "xyz789",
  "vtk_template": "xyz789",
  "format_specific_data": AWSJSON,
  "email_notification": [AWSEmail]
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

## Track

##### Fields

| Field Name | Description |
| --- | --- |
| `codec_type` - [`String!`](#definition-String) | Type of the requested track. Either video, audio, subtitle, closedcaption, or image. |
| `messages` - [`[String]`](#definition-String) | Messages generated for this specific track during workflow execution. |
| `source` - [`Source`](#definition-Source) | Actual source file with some additional information as determined during workflow execution. |
| `lang` - [`String`](#definition-String) | Language of the requested track. |

##### Example

```json
{
  "codec_type": "abc123",
  "messages": ["abc123"],
  "source": Source,
  "lang": "abc123"
}
```

[Types](#group-Types)

## TrackInput

##### Fields

| Input Field | Description |
| --- | --- |
| `codec_type` - [`CodecType!`](#definition-CodecType) |     |
| `lang` - [`String`](#definition-String) | `lang` is required for audio/subtitle/closedcaption tracks. |
| `filename` - [`String`](#definition-String) | `filename` is required for and used only by image tracks. |

##### Example

```json
{
  "codec_type": "video",
  "lang": "xyz789",
  "filename": "abc123"
}
```

[Types](#group-Types)

## VtkJob

##### Fields

| Field Name | Description |
| --- | --- |
| `created` - [`AWSDateTime`](#definition-AWSDateTime) | Creation date of the VTK job in ISO 8601 date string format. |
| `id` - [`String`](#definition-String) | Unique identifier for the VTK job. |
| `organization_id` - [`String`](#definition-String) |     |
| `job_bundle` - [`String`](#definition-String) | Job Bundles are used for grouping jobs together. All jobs in a PO will have the PO's name as the job bundle. |
| `modified` - [`AWSDateTime`](#definition-AWSDateTime) | Modified date of the VTK job in ISO 8601 date string format. |
| `status_text` - [`String!`](#definition-String) |     |
| `tags` - [`[String]`](#definition-String) |     |

##### Example

```json
{
  "created": AWSDateTime,
  "id": "abc123",
  "organization_id": "abc123",
  "job_bundle": "xyz789",
  "modified": AWSDateTime,
  "status_text": "xyz789",
  "tags": ["xyz789"]
}
```

[Documentation by Anvil SpectaQL](https://github.com/anvilco/spectaql)