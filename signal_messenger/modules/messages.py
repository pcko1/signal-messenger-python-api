"""Messages module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional, Union

import aiohttp

from signal_messenger.models import Message, MessageType, Reaction, Receipt, ReceiptType
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
    ) -> Message:
        """Send a message to one or more recipients.

        Args:
            number: The sender's phone number.
            message: The message text.
            recipients: The list of recipient phone numbers.
            attachments: The list of attachment IDs (optional).
            mention_recipients: The list of mention recipients (optional).
            quote: The quote information (optional).

        Returns:
            The sent message object.
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
        response = await make_request(self._module_session, "POST", url, data=data)

        # Create a Message object from the response
        msg_data = {
            "message": message,
            "source": number,
            "type": MessageType.OUTGOING,
        }

        # Add any additional data from the response
        if isinstance(response, dict):
            msg_data.update({str(k): v for k, v in response.items()})

        return Message(**msg_data)

    async def send_typing_indicator(
        self, number: str, recipient: str, stop: bool = False
    ) -> Dict[str, Any]:
        """Send a typing indicator to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            stop: Whether to stop the typing indicator (default: False).

        Returns:
            A dictionary containing the typing indicator status, typically {"sent": true}.
        """
        url = f"{self.base_url}/v1/typing-indicator/{number}/{recipient}"
        data = {"stop": stop}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def send_read_receipt(
        self, number: str, recipient: str, timestamps: List[int]
    ) -> Receipt:
        """Send a read receipt to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            timestamps: The list of message timestamps to mark as read.

        Returns:
            The receipt object.
        """
        url = f"{self.base_url}/v1/receipts/{number}/{recipient}/read"
        data = {"timestamps": timestamps}
        response = await make_request(self._module_session, "PUT", url, data=data)
        return Receipt(
            type=ReceiptType.READ,
            sender=number,
            sender_uuid=None,
            sender_device=None,
            timestamp=timestamps[0] if timestamps else None,
            when=None,
            **response,
        )

    async def send_viewed_receipt(
        self, number: str, recipient: str, timestamps: List[int]
    ) -> Receipt:
        """Send a viewed receipt to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            timestamps: The list of message timestamps to mark as viewed.

        Returns:
            The receipt object.
        """
        url = f"{self.base_url}/v1/receipts/{number}/{recipient}/viewed"
        data = {"timestamps": timestamps}
        response = await make_request(self._module_session, "PUT", url, data=data)
        return Receipt(
            type=ReceiptType.VIEWED,
            sender=number,
            sender_uuid=None,
            sender_device=None,
            timestamp=timestamps[0] if timestamps else None,
            when=None,
            **response,
        )

    async def send_delivery_receipt(
        self, number: str, recipient: str, timestamps: List[int]
    ) -> Receipt:
        """Send a delivery receipt to a recipient.

        Args:
            number: The sender's phone number.
            recipient: The recipient's phone number.
            timestamps: The list of message timestamps to mark as delivered.

        Returns:
            The receipt object.
        """
        url = f"{self.base_url}/v1/receipts/{number}/{recipient}/delivery"
        data = {"timestamps": timestamps}
        response = await make_request(self._module_session, "PUT", url, data=data)
        return Receipt(
            type=ReceiptType.DELIVERY,
            sender=number,
            sender_uuid=None,
            sender_device=None,
            timestamp=timestamps[0] if timestamps else None,
            when=None,
            **response,
        )

    async def get_messages(
        self, number: str, limit: Optional[int] = None
    ) -> List[Message]:
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

        messages = []
        if isinstance(response, dict) and "messages" in response:
            messages = response["messages"]
        elif isinstance(response, list):
            messages = response
        else:
            messages = [response]

        # Convert messages to Message objects
        result = []
        for msg in messages:
            if isinstance(msg, dict):
                # Convert any non-string keys to strings
                msg_dict = {str(k): v for k, v in msg.items()}
                result.append(Message(**msg_dict))
            elif isinstance(msg, str):
                # Handle case where message is a string
                result.append(Message(message=msg))
            else:
                # Try to convert to Message as is
                result.append(Message(**{"message": str(msg)}))

        return result

    async def delete_message(self, number: str, message_id: str) -> Dict[str, Any]:
        """Delete a message.

        Args:
            number: The registered phone number.
            message_id: The message ID.

        Returns:
            A dictionary containing the deletion status, typically {"deleted": true}.
        """
        url = f"{self.base_url}/v1/messages/{number}/{message_id}"
        return await make_request(self._module_session, "DELETE", url)
