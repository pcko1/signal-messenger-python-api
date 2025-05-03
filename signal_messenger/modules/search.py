"""Search module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class SearchModule:
    """Search module for the Signal Messenger Python API.

    This module provides access to search functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Search module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def search_messages(
        self, number: str, query: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search messages for a phone number.

        Args:
            number: The registered phone number.
            query: The search query.
            limit: The maximum number of messages to return (optional).

        Returns:
            A list of matching messages.
        """
        url = f"{self.base_url}/v1/search/{number}/messages"
        params = {"query": query}
        if limit is not None:
            params["limit"] = str(limit)
        response = await make_request(self._module_session, "GET", url, params=params)
        if isinstance(response, dict) and "messages" in response:
            return response["messages"]
        elif isinstance(response, list):
            return response
        return [response]

    async def search_contacts(
        self, number: str, query: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search contacts for a phone number.

        Args:
            number: The registered phone number.
            query: The search query.
            limit: The maximum number of contacts to return (optional).

        Returns:
            A list of matching contacts.
        """
        url = f"{self.base_url}/v1/search/{number}/contacts"
        params = {"query": query}
        if limit is not None:
            params["limit"] = str(limit)
        response = await make_request(self._module_session, "GET", url, params=params)
        if isinstance(response, dict) and "contacts" in response:
            return response["contacts"]
        elif isinstance(response, list):
            return response
        return [response]

    async def search_groups(
        self, number: str, query: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search groups for a phone number.

        Args:
            number: The registered phone number.
            query: The search query.
            limit: The maximum number of groups to return (optional).

        Returns:
            A list of matching groups.
        """
        url = f"{self.base_url}/v1/search/{number}/groups"
        params = {"query": query}
        if limit is not None:
            params["limit"] = str(limit)
        response = await make_request(self._module_session, "GET", url, params=params)
        if isinstance(response, dict) and "groups" in response:
            return response["groups"]
        elif isinstance(response, list):
            return response
        return [response]

    async def search_all(
        self, number: str, query: str, limit: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Search all entities for a phone number.

        Args:
            number: The registered phone number.
            query: The search query.
            limit: The maximum number of results to return per entity type (optional).

        Returns:
            A dictionary containing lists of matching messages, contacts, and groups.
        """
        url = f"{self.base_url}/v1/search/{number}"
        params = {"query": query}
        if limit is not None:
            params["limit"] = str(limit)
        response = await make_request(self._module_session, "GET", url, params=params)

        result = {"messages": [], "contacts": [], "groups": []}

        if isinstance(response, dict):
            if "messages" in response:
                result["messages"] = response["messages"]
            if "contacts" in response:
                result["contacts"] = response["contacts"]
            if "groups" in response:
                result["groups"] = response["groups"]

        return result
