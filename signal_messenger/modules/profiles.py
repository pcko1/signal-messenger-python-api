"""Profiles module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class ProfilesModule:
    """Profiles module for the Signal Messenger Python API.

    This module provides access to profile management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Profiles module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def get_profile(self, number: str) -> Dict[str, Any]:
        """Get the profile for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            The profile information.
        """
        url = f"{self.base_url}/v1/profiles/{number}"
        return await make_request(self._module_session, "GET", url)

    async def update_profile(
        self,
        number: str,
        name: Optional[str] = None,
        about: Optional[str] = None,
        avatar: Optional[str] = None,
        emoji: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a profile.

        Args:
            number: The registered phone number.
            name: The new profile name (optional).
            about: The new profile about text (optional).
            avatar: The new avatar URL (optional).
            emoji: The new profile emoji (optional).

        Returns:
            The response containing the profile update information.
        """
        url = f"{self.base_url}/v1/profiles/{number}"
        data = {}
        if name is not None:
            data["name"] = name
        if about is not None:
            data["about"] = about
        if avatar is not None:
            data["avatar"] = avatar
        if emoji is not None:
            data["emoji"] = emoji
        return await make_request(self._module_session, "PUT", url, data=data)

    async def get_contact_profile(self, number: str, contact: str) -> Dict[str, Any]:
        """Get the profile of a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.

        Returns:
            The contact's profile information.
        """
        url = f"{self.base_url}/v1/profiles/{number}/contacts/{contact}"
        return await make_request(self._module_session, "GET", url)

    async def get_contacts_profiles(self, number: str) -> List[Dict[str, Any]]:
        """Get the profiles of all contacts.

        Args:
            number: The registered phone number.

        Returns:
            A list of contact profiles.
        """
        url = f"{self.base_url}/v1/profiles/{number}/contacts"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "contacts" in response:
            return response["contacts"]
        elif isinstance(response, list):
            return response
        return [response]

    async def set_profile_sharing(
        self, number: str, contact: str, enabled: bool
    ) -> Dict[str, Any]:
        """Set profile sharing with a contact.

        Args:
            number: The registered phone number.
            contact: The contact's phone number.
            enabled: Whether to enable profile sharing.

        Returns:
            The response containing the profile sharing information.
        """
        url = f"{self.base_url}/v1/profiles/{number}/contacts/{contact}/sharing"
        data = {"enabled": enabled}
        return await make_request(self._module_session, "PUT", url, data=data)
