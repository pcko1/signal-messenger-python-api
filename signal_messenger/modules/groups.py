"""Groups module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.models import Group, GroupMember
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

    async def get_groups(self, number: str) -> List[Group]:
        """Get all groups for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of groups.
        """
        url = f"{self.base_url}/v1/groups/{number}"
        response = await make_request(self._module_session, "GET", url)

        groups = []
        if isinstance(response, dict) and "groups" in response:
            groups = response["groups"]
        elif isinstance(response, list):
            groups = response
        else:
            groups = [response]

        # Convert groups to Group objects
        result = []
        for group in groups:
            if isinstance(group, dict):
                # Convert any non-string keys to strings
                group_dict = {str(k): v for k, v in group.items()}
                result.append(Group(**group_dict))
            else:
                # Try to convert to Group as is
                result.append(Group(id=str(group)))

        return result

    async def get_group(self, number: str, group_id: str) -> Group:
        """Get a specific group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            The group details.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}"
        response = await make_request(self._module_session, "GET", url)

        if isinstance(response, dict):
            # Convert any non-string keys to strings
            group_dict = {str(k): v for k, v in response.items()}
            return Group(**group_dict)
        else:
            # Try to convert to Group as is
            return Group(id=group_id)

    async def create_group(
        self, number: str, name: str, members: List[str], avatar: Optional[str] = None
    ) -> Group:
        """Create a new group.

        Args:
            number: The registered phone number.
            name: The group name.
            members: The list of member phone numbers.
            avatar: The avatar URL (optional).

        Returns:
            The created group.
        """
        url = f"{self.base_url}/v1/groups/{number}"
        data = {"name": name, "members": members}
        if avatar:
            data["avatar"] = avatar
        response = await make_request(self._module_session, "POST", url, data=data)

        if isinstance(response, dict):
            # Convert any non-string keys to strings
            group_dict = {str(k): v for k, v in response.items()}
            # Add the name and members if not in the response
            if "name" not in group_dict:
                group_dict["name"] = name
            if "members" not in group_dict and members:
                group_dict["members"] = [{"number": m} for m in members]
            return Group(**group_dict)
        else:
            # Try to create a minimal Group object
            return Group(id=str(response), name=name)

    async def update_group(
        self,
        number: str,
        group_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> Group:
        """Update a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.
            name: The new group name (optional).
            description: The new group description (optional).
            avatar: The new avatar URL (optional).

        Returns:
            The updated group.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}"
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if avatar:
            data["avatar"] = avatar
        response = await make_request(self._module_session, "PUT", url, data=data)

        if isinstance(response, dict):
            # Convert any non-string keys to strings
            group_dict = {str(k): v for k, v in response.items()}
            # Add the group_id if not in the response
            if "id" not in group_dict:
                group_dict["id"] = group_id
            # Add the updated fields if not in the response
            if name and "name" not in group_dict:
                group_dict["name"] = name
            if description and "description" not in group_dict:
                group_dict["description"] = description
            if avatar and "avatar" not in group_dict:
                group_dict["avatar"] = avatar
            return Group(**group_dict)
        else:
            # Try to create a minimal Group object
            return Group(id=group_id, name=name, description=description, avatar=avatar)

    async def delete_group(self, number: str, group_id: str) -> Dict[str, Any]:
        """Delete a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            A dictionary containing the deletion status, typically {"deleted": true}.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}"
        return await make_request(self._module_session, "DELETE", url)

    async def add_members(
        self, number: str, group_id: str, members: List[str]
    ) -> Group:
        """Add members to a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.
            members: The list of member phone numbers to add.

        Returns:
            The updated group with new members.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/members"
        data = {"members": members}
        response = await make_request(self._module_session, "POST", url, data=data)

        if isinstance(response, dict):
            # Convert any non-string keys to strings
            group_dict = {str(k): v for k, v in response.items()}
            # Add the group_id if not in the response
            if "id" not in group_dict:
                group_dict["id"] = group_id
            return Group(**group_dict)
        else:
            # Try to create a minimal Group object
            return Group(id=group_id)

    async def remove_members(
        self, number: str, group_id: str, members: List[str]
    ) -> Group:
        """Remove members from a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.
            members: The list of member phone numbers to remove.

        Returns:
            The updated group without the removed members.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/members"
        data = {"members": members}
        response = await make_request(self._module_session, "DELETE", url, data=data)

        if isinstance(response, dict):
            # Convert any non-string keys to strings
            group_dict = {str(k): v for k, v in response.items()}
            # Add the group_id if not in the response
            if "id" not in group_dict:
                group_dict["id"] = group_id
            return Group(**group_dict)
        else:
            # Try to create a minimal Group object
            return Group(id=group_id)

    async def join_group(self, number: str, group_id: str) -> Group:
        """Join a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            The joined group.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/join"
        response = await make_request(self._module_session, "POST", url)

        if isinstance(response, dict):
            # Convert any non-string keys to strings
            group_dict = {str(k): v for k, v in response.items()}
            # Add the group_id if not in the response
            if "id" not in group_dict:
                group_dict["id"] = group_id
            return Group(**group_dict)
        else:
            # Try to create a minimal Group object
            return Group(id=group_id)

    async def leave_group(self, number: str, group_id: str) -> Dict[str, Any]:
        """Leave a group.

        Args:
            number: The registered phone number.
            group_id: The group ID.

        Returns:
            A dictionary containing the leave status, typically {"left": true}.
        """
        url = f"{self.base_url}/v1/groups/{number}/{group_id}/leave"
        return await make_request(self._module_session, "POST", url)
