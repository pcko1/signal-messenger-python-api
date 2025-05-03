"""Messages module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional, Union

import aiohttp

from signal_messenger.utils import make_request


class MessagesModule:
    """Messages module for the Signal Messenger Python API.

    This module provides access to message sending and receiving functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Messages module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def send_message(
        self,
        number: str,
        message: str,
        recipients: List[str],
        attachments: Optional[List[str]] = None,
        mention_recipients: Optional[List[Dict[str, Any]]] = None,
        quote: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a message to one or more recipients.

        Args:
            number: The sender's phone number.
            message: The message text.
            recipients: The list of recipient phone numbers.
            attachments: The list of attachment IDs (optional).
            mention_recipients: The list of mention recipients (optional).
            quote: The quote information (optional).

        Returns:
            The response containing the message sending information.
        """
        url = f"{self.base_url}/v2/send"
        data = {
            "number": number,
            "message": message,
            "recipients": recipients,
        }
        if attachments:
            data["attachments"] = attachments
        if mention_recipients:
            data["mention"] = mention_recipients
        if quote:
            data["quote"] = quote
        return await make_request(self._module_session, "POST", url, data=data)

    async def send_typing_indicator(
        self, number: str, recipient: str, stop: bool = False
    ) -> Dict[str, Any]:
        """Send a typing indicator to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            stop: Whether to stop the typing indicator (default: False).

        Returns:
            The response containing the typing indicator information.
        """
        url = f"{self.base_url}/v1/typing-indicator/{number}/{recipient}"
        data = {"stop": stop}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def send_read_receipt(
        self, number: str, recipient: str, timestamps: List[int]
    ) -> Dict[str, Any]:
        """Send a read receipt to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            timestamps: The list of message timestamps to mark as read.

        Returns:
            The response containing the read receipt information.
        """
        url = f"{self.base_url}/v1/receipts/{number}/{recipient}/read"
        data = {"timestamps": timestamps}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def send_viewed_receipt(
        self, number: str, recipient: str, timestamps: List[int]
    ) -> Dict[str, Any]:
        """Send a viewed receipt to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            timestamps: The list of message timestamps to mark as viewed.

        Returns:
            The response containing the viewed receipt information.
        """
        url = f"{self.base_url}/v1/receipts/{number}/{recipient}/viewed"
        data = {"timestamps": timestamps}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def send_delivery_receipt(
        self, number: str, recipient: str, timestamps: List[int]
    ) -> Dict[str, Any]:
        """Send a delivery receipt to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            timestamps: The list of message timestamps to mark as delivered.

        Returns:
            The response containing the delivery receipt information.
        """
        url = f"{self.base_url}/v1/receipts/{number}/{recipient}/delivery"
        data = {"timestamps": timestamps}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def get_messages(
        self, number: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get messages for a phone number.

        Args:
            number: The registered phone number.
            limit: The maximum number of messages to return (optional).

        Returns:
            A list of messages.
        """
        url = f"{self.base_url}/v1/receive/{number}"
        params = {}
        if limit is not None:
            params["limit"] = limit
        response = await make_request(self._module_session, "GET", url, params=params)
        if isinstance(response, dict) and "messages" in response:
            return response["messages"]
        elif isinstance(response, list):
            return response
        return [response]

    async def delete_message(self, number: str, message_id: str) -> Dict[str, Any]:
        """Delete a message.

        Args:
            number: The registered phone number.
            message_id: The message ID.

        Returns:
            The response containing the message deletion information.
        """
        url = f"{self.base_url}/v1/messages/{number}/{message_id}"
        return await make_request(self._module_session, "DELETE", url)
