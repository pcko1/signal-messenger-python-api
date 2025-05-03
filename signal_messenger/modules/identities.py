"""Identities module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class IdentitiesModule:
    """Identities module for the Signal Messenger Python API.

    This module provides access to identity management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Identities module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def get_identities(self, number: str) -> List[Dict[str, Any]]:
        """Get all identities for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of identities.
        """
        url = f"{self.base_url}/v1/identities/{number}"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "identities" in response:
            return response["identities"]
        elif isinstance(response, list):
            return response
        return [response]

    async def get_identity(self, number: str, recipient: str) -> Dict[str, Any]:
        """Get the identity for a specific recipient.

        Args:
            number: The registered phone number.
            recipient: The recipient's phone number.

        Returns:
            The identity information.
        """
        url = f"{self.base_url}/v1/identities/{number}/{recipient}"
        return await make_request(self._module_session, "GET", url)

    async def trust_identity(
        self,
        number: str,
        recipient: str,
        trust_level: str,
        verified_safety_number: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Trust an identity.

        Args:
            number: The registered phone number.
            recipient: The recipient's phone number.
            trust_level: The trust level (TRUSTED, UNTRUSTED).
            verified_safety_number: The verified safety number (optional).

        Returns:
            The response containing the trust information.
        """
        url = f"{self.base_url}/v1/identities/{number}/{recipient}"
        data = {"trustLevel": trust_level}
        if verified_safety_number:
            data["verifiedSafetyNumber"] = verified_safety_number
        return await make_request(self._module_session, "PUT", url, data=data)

    async def verify_identity(
        self, number: str, recipient: str, safety_number: str
    ) -> Dict[str, Any]:
        """Verify an identity.

        Args:
            number: The registered phone number.
            recipient: The recipient's phone number.
            safety_number: The safety number to verify.

        Returns:
            The response containing the verification information.
        """
        url = f"{self.base_url}/v1/identities/{number}/{recipient}/verify"
        data = {"safetyNumber": safety_number}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def reset_identity_session(
        self, number: str, recipient: str
    ) -> Dict[str, Any]:
        """Reset an identity session.

        Args:
            number: The registered phone number.
            recipient: The recipient's phone number.

        Returns:
            The response containing the session reset information.
        """
        url = f"{self.base_url}/v1/identities/{number}/{recipient}/session"
        return await make_request(self._module_session, "DELETE", url)
