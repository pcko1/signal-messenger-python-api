"""Attachments module for the Signal Messenger Python API."""

from typing import Any, BinaryIO, Dict, List, Optional, Union

import aiohttp

from signal_messenger.utils import make_request


class AttachmentsModule:
    """Attachments module for the Signal Messenger Python API.

    This module provides access to attachment management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Attachments module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def upload_attachment(
        self, number: str, file_data: Union[bytes, BinaryIO], content_type: str
    ) -> Dict[str, Any]:
        """Upload an attachment.

        Args:
            number: The registered phone number.
            file_data: The file data as bytes or a file-like object.
            content_type: The content type of the file.

        Returns:
            The response containing the attachment ID.
        """
        url = f"{self.base_url}/v1/attachments/{number}"
        headers = {"Content-Type": content_type}

        # Use the session directly for binary data
        async with self._module_session.post(
            url, data=file_data, headers=headers
        ) as response:
            from signal_messenger.utils import handle_response

            return await handle_response(response)

    async def get_attachment(self, number: str, attachment_id: str) -> bytes:
        """Get an attachment.

        Args:
            number: The registered phone number.
            attachment_id: The attachment ID.

        Returns:
            The attachment data as bytes.
        """
        url = f"{self.base_url}/v1/attachments/{number}/{attachment_id}"
        async with self._module_session.get(url) as response:
            if response.status != 200:
                # Handle error response
                error_data = await response.json()
                error_message = error_data.get("error", "Unknown error")
                raise Exception(f"Failed to get attachment: {error_message}")
            return await response.read()

    async def delete_attachment(
        self, number: str, attachment_id: str
    ) -> Dict[str, Any]:
        """Delete an attachment.

        Args:
            number: The registered phone number.
            attachment_id: The attachment ID.

        Returns:
            The response containing the attachment deletion information.
        """
        url = f"{self.base_url}/v1/attachments/{number}/{attachment_id}"
        return await make_request(self._module_session, "DELETE", url)

    async def get_attachment_info(
        self, number: str, attachment_id: str
    ) -> Dict[str, Any]:
        """Get information about an attachment.

        Args:
            number: The registered phone number.
            attachment_id: The attachment ID.

        Returns:
            The attachment information.
        """
        url = f"{self.base_url}/v1/attachments/{number}/{attachment_id}/info"
        return await make_request(self._module_session, "GET", url)

    async def get_attachments(self, number: str) -> List[Dict[str, Any]]:
        """Get all attachments for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of attachments.
        """
        url = f"{self.base_url}/v1/attachments/{number}"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "attachments" in response:
            return response["attachments"]
        elif isinstance(response, list):
            return response
        return [response]
