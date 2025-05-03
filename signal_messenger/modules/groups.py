"""Groups module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class GroupsModule:
    """Groups module for the Signal Messenger Python API.

    This module provides access to group management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Groups module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def get_groups(self, number: str) -> List[Dict[str, Any]]:
        """Get all groups for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of groups.
        """
        url = f"{self.base_url}/v1/groups/{number}"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "groups" in response:
            return response["groups"]
        elif isinstance(response, list):
            return response
        return [response]

    async def get_group(self, number: str, group_id: str) -> Dict[str, Any]:
        """Get a specific group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            The group details.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}"
        return await make_request(self._module_session, "GET", url)

    async def create_group(
        self, number: str, name: str, members: List[str], avatar: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new group.

        Args:
            number: The registered phone number.
            name: The group name.
            members: The list of member phone numbers.
            avatar: The avatar URL (optional).

        Returns:
            The response containing the group creation information.
        """
        url = f"{self.base_url}/v1/groups/{number}"
        data = {"name": name, "members": members}
        if avatar:
            data["avatar"] = avatar
        return await make_request(self._module_session, "POST", url, data=data)

    async def update_group(
        self,
        number: str,
        group_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.
            name: The new group name (optional).
            description: The new group description (optional).
            avatar: The new avatar URL (optional).

        Returns:
            The response containing the group update information.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}"
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if avatar:
            data["avatar"] = avatar
        return await make_request(self._module_session, "PUT", url, data=data)

    async def delete_group(self, number: str, group_id: str) -> Dict[str, Any]:
        """Delete a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            The response containing the group deletion information.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}"
        return await make_request(self._module_session, "DELETE", url)

    async def add_members(
        self, number: str, group_id: str, members: List[str]
    ) -> Dict[str, Any]:
        """Add members to a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.
            members: The list of member phone numbers to add.

        Returns:
            The response containing the member addition information.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/members"
        data = {"members": members}
        return await make_request(self._module_session, "POST", url, data=data)

    async def remove_members(
        self, number: str, group_id: str, members: List[str]
    ) -> Dict[str, Any]:
        """Remove members from a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.
            members: The list of member phone numbers to remove.

        Returns:
            The response containing the member removal information.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/members"
        data = {"members": members}
        return await make_request(self._module_session, "DELETE", url, data=data)

    async def join_group(self, number: str, group_id: str) -> Dict[str, Any]:
        """Join a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            The response containing the group join information.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/join"
        return await make_request(self._module_session, "POST", url)

    async def leave_group(self, number: str, group_id: str) -> Dict[str, Any]:
        """Leave a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            The response containing the group leave information.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/leave"
        return await make_request(self._module_session, "POST", url)
