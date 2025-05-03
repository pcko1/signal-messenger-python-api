"""Contacts module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class ContactsModule:
    """Contacts module for the Signal Messenger Python API.

    This module provides access to contact management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Contacts module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def get_contacts(self, number: str) -> List[Dict[str, Any]]:
        """Get all contacts for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of contacts.
        """
        url = f"{self.base_url}/v1/contacts/{number}"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "contacts" in response:
            return response["contacts"]
        elif isinstance(response, list):
            return response
        return [response]

    async def get_contact(self, number: str, contact: str) -> Dict[str, Any]:
        """Get a specific contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.

        Returns:
            The contact details.
        """
        url = f"{self.base_url}/v1/contacts/{number}/{contact}"
        return await make_request(self._module_session, "GET", url)

    async def add_contact(
        self,
        number: str,
        contact: str,
        name: Optional[str] = None,
        expiration: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Add a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.
            name: The contact's name (optional).
            expiration: The message expiration time in seconds (optional).

        Returns:
            The response containing the contact addition information.
        """
        url = f"{self.base_url}/v1/contacts/{number}"
        data = {"contact": contact}
        if name is not None:
            data["name"] = name
        if expiration is not None:
            data["expiration"] = str(expiration)
        return await make_request(self._module_session, "POST", url, data=data)

    async def update_contact(
        self,
        number: str,
        contact: str,
        name: Optional[str] = None,
        expiration: Optional[int] = None,
        blocked: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.
            name: The new contact name (optional).
            expiration: The new message expiration time in seconds (optional).
            blocked: Whether the contact is blocked (optional).

        Returns:
            The response containing the contact update information.
        """
        url = f"{self.base_url}/v1/contacts/{number}/{contact}"
        data = {}
        if name is not None:
            data["name"] = name
        if expiration is not None:
            data["expiration"] = str(expiration)
        if blocked is not None:
            data["blocked"] = blocked
        return await make_request(self._module_session, "PUT", url, data=data)

    async def delete_contact(self, number: str, contact: str) -> Dict[str, Any]:
        """Delete a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.

        Returns:
            The response containing the contact deletion information.
        """
        url = f"{self.base_url}/v1/contacts/{number}/{contact}"
        return await make_request(self._module_session, "DELETE", url)

    async def block_contact(self, number: str, contact: str) -> Dict[str, Any]:
        """Block a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.

        Returns:
            The response containing the contact blocking information.
        """
        url = f"{self.base_url}/v1/contacts/{number}/{contact}/block"
        return await make_request(self._module_session, "PUT", url)

    async def unblock_contact(self, number: str, contact: str) -> Dict[str, Any]:
        """Unblock a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.

        Returns:
            The response containing the contact unblocking information.
        """
        url = f"{self.base_url}/v1/contacts/{number}/{contact}/unblock"
        return await make_request(self._module_session, "PUT", url)

    async def get_blocked_contacts(self, number: str) -> List[Dict[str, Any]]:
        """Get all blocked contacts for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of blocked contacts.
        """
        url = f"{self.base_url}/v1/contacts/{number}/blocked"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "contacts" in response:
            return response["contacts"]
        elif isinstance(response, list):
            return response
        return [response]
