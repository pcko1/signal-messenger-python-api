"""Accounts module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class AccountsModule:
    """Accounts module for the Signal Messenger Python API.

    This module provides access to account management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Accounts module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def register_account(
        self, number: str, captcha: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register a new Signal account.

        Args:
            number: The phone number to register.
            captcha: The captcha token (if required).

        Returns:
            The response containing the registration information.
        """
        url = f"{self.base_url}/v1/accounts/{number}"
        data = {}
        if captcha:
            data["captcha"] = captcha
        return await make_request(self._module_session, "POST", url, data=data)

    async def verify_account(
        self, number: str, verification_code: str
    ) -> Dict[str, Any]:
        """Verify a registered Signal account.

        Args:
            number: The registered phone number.
            verification_code: The verification code.

        Returns:
            The response containing the verification information.
        """
        url = f"{self.base_url}/v1/accounts/{number}/verify/{verification_code}"
        return await make_request(self._module_session, "POST", url)

    async def get_account_details(self, number: str) -> Dict[str, Any]:
        """Get details about a registered Signal account.

        Args:
            number: The registered phone number.

        Returns:
            The response containing the account details.
        """
        url = f"{self.base_url}/v1/accounts/{number}"
        return await make_request(self._module_session, "GET", url)

    async def update_account(
        self,
        number: str,
        registration_id: Optional[int] = None,
        pni_registration_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update a registered Signal account.

        Args:
            number: The registered phone number.
            registration_id: The registration ID.
            pni_registration_id: The PNI registration ID.

        Returns:
            The response containing the update information.
        """
        url = f"{self.base_url}/v1/accounts/{number}"
        data = {}
        if registration_id is not None:
            data["registrationId"] = registration_id
        if pni_registration_id is not None:
            data["pniRegistrationId"] = pni_registration_id
        return await make_request(self._module_session, "PUT", url, data=data)

    async def delete_account(self, number: str) -> Dict[str, Any]:
        """Delete a registered Signal account.

        Args:
            number: The registered phone number.

        Returns:
            The response containing the deletion information.
        """
        url = f"{self.base_url}/v1/accounts/{number}"
        return await make_request(self._module_session, "DELETE", url)

    async def set_pin(self, number: str, pin: str) -> Dict[str, Any]:
        """Set a PIN for a registered Signal account.

        Args:
            number: The registered phone number.
            pin: The PIN to set.

        Returns:
            The response containing the PIN setting information.
        """
        url = f"{self.base_url}/v1/accounts/{number}/pin"
        data = {"pin": pin}
        return await make_request(self._module_session, "PUT", url, data=data)

    async def remove_pin(self, number: str) -> Dict[str, Any]:
        """Remove the PIN from a registered Signal account.

        Args:
            number: The registered phone number.

        Returns:
            The response containing the PIN removal information.
        """
        url = f"{self.base_url}/v1/accounts/{number}/pin"
        return await make_request(self._module_session, "DELETE", url)
