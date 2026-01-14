import time
from datetime import datetime, timedelta
from logging import getLogger
from typing import List, Optional

from .client import Client
from .repository import StorageLocation

logger = getLogger("castlabs.workflow")


class Workflow:
    """
    The Workflows class exposes functionality directly related to the workflow and encoding jobs
    on the ContentPlatform. The class will be initialized by the contentPlatformSDK. It should not be necessary
    to do this manually.
    """

    def __init__(self, client: Client):
        self.client = client

    def create_vod_encoding(
        self,
        storage_location: StorageLocation,
        origin_folder: str,
        group_name: str,
        process_name: str,
        destination: str = "vod",
        template: str = "cmaf-abr",
        format_specific_data: dict = "{}",
        auto_publish: bool = True,
        webhook_url: Optional[str] = None,
        wait_timeout: int = 10,
    ):
        """
        You can create a workflow based on a folder in your repository. The workflow will try to detect a master
        video file and corresponding side-car files and create an appropriate output.
        In the case of a standard VOD/CMAF-abr workflow a streamable output distributed by cloudfront will be created.
        In a second step you can attach a web-hook to the workflow to be alerted to status changes.

        :param storage_location: :func:~contentPlatformSDK.storage.StorageLocation object`
        :param origin_folder: Path to the title origin folder
        :param group_name: Name of the group in which the process is categorized
        :param process_name: Name of the specific encoding process of a title
        :param destination: (Optional) Per default this is the cloudfront origin for VOD streaming
        :param template: (Optional) Per default this is the VOD streaming template
        :param format_specific_data: (Optional) Provide extra parameters for the encoding workflow
        :param auto_publish: (Optional) Per default a workflow publishes automatically to the destination. In case QC
        of the encoded files is necessary this can be set to 'False'. A preview can be requested and publishing can be
        triggered manually.
        :param webhook_url: (Optional) The webhook URL to notify events to your backend
        :return: :func:`~contentPlatformSDK/workflow/process/Process`
        """
        logger.info(f"Creating VOD encoding for {origin_folder}")
        self.client._query_api_dict(
            "workflow",
            query={
                "operationName": "start_workflow_vod_default",
                "variables": {
                    "input_brefix": storage_location.get_location_with_path(origin_folder, True)[5:],  # no s3://
                    "po_item_id": process_name,
                    "po_name": f"{self.client.organization_urn}_{group_name}",
                    "po_destination": destination,
                    "vtk_template": template,
                    "auto_publish": auto_publish,
                    "format_specific_data": format_specific_data,
                },
                "query": """
                    mutation start_workflow_vod_default(
                    $po_item_id: String!,
                    $po_name: String!,
                    $input_brefix: String!,
                    $po_destination: String!,
                    $auto_publish: Boolean!,
                    $vtk_template: String!,
                    $format_specific_data: AWSJSON!,
                    $email_notification: [AWSEmail!]) {
                        start_workflow_vod_default(
                            input: {
                                po_name: $po_name,
                                po_item_id: $po_item_id,
                                input_brefix: $input_brefix,
                                po_destination: $po_destination,
                                auto_publish: $auto_publish,
                                email_notification: $email_notification,
                                vtk_template: $vtk_template,
                                format_specific_data: $format_specific_data
                            }) {
                            state
                            message
                            input
                            data
                            action
                            id
                            start_date
                            end_date
                            __typename
                        }
                    }""",
            },
            content_key="start_workflow_vod_default",
        )

        # Wait for the process to be created
        timeout = datetime.now() + timedelta(seconds=wait_timeout)
        process = None
        while datetime.now() < timeout and process is None:
            try:
                process = self.get_process(group_name, process_name)
            except KeyError:  # pragma: no cover
                time.sleep(1)

        if not process:  # pragma: no cover
            raise Exception("Timed out waiting for process to be created")

        if webhook_url:
            process.register_webhook(webhook_url)
            return process
        else:  # pragma: no cover
            # We don't test this option as running the process is a long running operation
            # and we don't want to run it twice
            return process

    def get_groups(self) -> List[str]:
        logger.info("Getting groups")
        response_data = self.client._query_api_dict(
            "workflow",
            query={
                "operationName": "GetPOs",
                "variables": {"airline": self.client.organization_urn},
                "query": """
                    query GetPOs($airline: String!) {
                        list_POs(input: {filter: {airline: {eq: $airline}}}) {
                            pos {
                                id
                                airline
                                po_name
                                date_due
                                date_created
                                target_system
                                __typename
                            }
                          __typename
                        }
                    }""",
            },
            content_key="list_POs",
            method="POST",
        )
        return [po["po_name"].replace(f"{self.client.organization_urn}_", "") for po in response_data["pos"]]

    def get_processes(self, group_name: str) -> List["Process"]:
        logger.info(f"Getting processes for group {group_name}")
        response_data = self.client._query_api_dict(
            "workflow",
            query={
                "operationName": "PoItemListFull",
                "variables": {
                    "po_name": f"{self.client.organization_urn}_{group_name}",
                },
                "query": """
                    query PoItemListFull($po_name: String!) {
                        list_POs(input: {filter: {po_name: {eq: $po_name}}}) {
                            pos {
                                id
                                poitems {
                                    input_brefix
                                    filename
                                    id
                                    po_item_id
                                    po_destination
                                    output_brefix
                                    po {
                                        po_name
                                    }
                                    publish_process {
                                        id
                                        state
                                        data
                                        message
                                        start_date
                                        end_date
                                    }
                                    workflow_process {
                                        id
                                        state
                                        data
                                        message
                                        start_date
                                        end_date
                                    }
                                    watermark
                                    workflow
                                    aspect_ratio
                                    format_specific_data
                                    preview {
                                        dash_manifest_last_modified
                                        dash_manifest_url
                                        hls_manifest_url
                                        hls_manifest_last_modified
                                    }
                                    tracks {
                                        codec_type
                                        messages
                                        source {
                                            codec_type
                                            index
                                            key
                                            lang
                                        }
                                        lang
                                    }
                                    checkpoint_content_uploaded
                                    checkpoint_content_complete
                                    checkpoint_encodes_done
                                    checkpoint_metadata_available
                                }
                            }
                        }
                    }""",
            },
            content_key="list_POs",
        )
        return (
            [Process(process_data, self.client).refresh_state() for process_data in response_data["pos"][0]["poitems"]]
            if response_data["pos"]
            else []
        )

    # TODO: create a better query
    def get_process(self, group_name: str, process_name: str) -> "Process":
        """
        Returns a process based on the group and process_name

        :param group_name: Name of the group you have specified
        :param process_name: Name of the encoding process
        :return: :func:`~contentPlatformSDK.workflow.Process`
        """
        processes = [process for process in self.get_processes(group_name) if process.pk == process_name]
        if processes:
            return processes[0]

        raise KeyError("Process not found")


class Process:
    """
    A Process manages a specific content operation, composed of encoding (content-preparation) and publishing
    """

    def __init__(self, data: dict, client: Client) -> None:
        self.pk = data["po_item_id"]
        self.encoding_process = data.get("workflow_process", {})
        self.publish_process = data.get("publish_process", {})

        self.raw_data = data
        self._client = client

    @property
    def state(self):
        """
        Determines the state based on the encoding and publishing process

        :return: state of Process
        """
        # TODO: Check if failure state is correct
        if self.encoding_process.get("state", None) not in ("SUCCESS", "ERROR"):
            return f"ENCODING_{self.encoding_process.get('state')}"
        return f"PUBLISH_{self.publish_process.get('state')}"

    @property
    def content_url(self):
        """
        Returns a Cloudfront content URL to use in your player

        :return: URL
        """
        return (
            "/".join(self.raw_data.get("output_brefix", None).split("/")[:-2]).replace(
                "content-repo-prod-output-castlabs-vod/castlabs-vod", "https://vod.cp.castlabs.com"
            )
            + "/"
        )

    def refresh_state(self) -> "Process":
        """
        Since the Processes are ASYNC of nature the status can be pulled. Remember that you can also register
        a webhook in order to receive event updates
        """
        if self.encoding_process.get("state") != "SUCCESS":
            process_id = self.encoding_process.get("id")
        # TODO: Delete this or write unit tests for this
        # elif self.publish_process.get("state") != "SUCCESS":
        #     process_id = self.publish_process.get("id")
        else:
            return self

        logger.info(f"Refreshing state for process {process_id}")
        response_data = self._client._query_api_dict(
            "workflow",
            query={
                "operationName": "GetProcess",
                "variables": {"id": process_id},
                "query": """
                        query GetProcess($id: ID!) {
                            process(id: $id) {
                                action
                                data
                                id
                                message
                                state
                                start_date
                                end_date
                            }
                        }""",
            },
            content_key="process",
        )
        if response_data.get("action") == "start_workflow_vod_default":
            setattr(self, "encoding_process", response_data)
        # TODO: Delete this or write unit tests for this
        # elif response_data.get("action") == "publishPo":
        #     setattr(self, "publish_process", response_data)
        else:  # pragma: no cover
            raise NotImplementedError("Unknown action")

        return self

    def register_webhook(self, url):
        """
        Registers a webhook (POST) for updates on final (SUCCESS and ERROR) encoding and publishing events

        :param url:
        """
        for sub_process in (self.encoding_process, self.publish_process):
            if not sub_process:
                logger.warning("Skipping webhook registration: sub_process is missing or None.")
                continue

            process_id = sub_process.get('id')
            if not process_id:
                logger.warning("Skipping webhook registration: sub_process exists but has no 'id'.")
                continue

            logger.info(f"Registering webhook for process {process_id}")

            self._client._query_api(
                "workflow",
                query={
                    "operationName": "registerWebhook",
                    "variables": {"input": {"process_id": process_id, "webhook_url": url}},
                    "query": """
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
                        }""",
                },
                content_key="registerWebhook",
            )
