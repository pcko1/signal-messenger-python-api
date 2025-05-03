"""Devices module for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

import aiohttp

from signal_messenger.utils import make_request


class DevicesModule:
    """Devices module for the Signal Messenger Python API.

    This module provides access to device registration and linking functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Devices module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def get_linked_devices(self, number: str) -> List[Dict[str, Any]]:
        """Get linked devices for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of linked devices.
        """
        url = f"{self.base_url}/v1/devices/{number}"
        response = await make_request(self._module_session, "GET", url)
        # The API returns a dictionary with a 'devices' key containing the list of devices
        if isinstance(response, dict) and "devices" in response:
            return response["devices"]
        # If the response is already a list, return it
        elif isinstance(response, list):
            return response
        # Otherwise, wrap the response in a list
        return [response]

    async def link_device(self, number: str, device_name: str) -> Dict[str, Any]:
        """Link another device to this device.

        Args:
            number: The registered phone number.
            device_name: The name of the device to link.

        Returns:
            The response containing the linking information.
        """
        url = f"{self.base_url}/v1/devices/{number}"
        data = {"name": device_name}
        return await make_request(self._module_session, "POST", url, data=data)

    async def get_qr_code_link(self, device_name: str = "") -> Dict[str, Any]:
        """Get a QR code link for device linking.

        Args:
            device_name: The name of the device to link.

        Returns:
            The response containing the QR code link.
        """
        url = f"{self.base_url}/v1/qrcodelink"
        params = {}
        if device_name:
            params["name"] = device_name
        return await make_request(self._module_session, "GET", url, params=params)

    async def register_device(self, number: str) -> Dict[str, Any]:
        """Register a phone number.

        Args:
            number: The phone number to register.

        Returns:
            The response containing the registration information.
        """
        url = f"{self.base_url}/v1/register/{number}"
        return await make_request(self._module_session, "POST", url)

    async def verify_device(self, number: str, token: str) -> Dict[str, Any]:
        """Verify a registered phone number.

        Args:
            number: The registered phone number.
            token: The verification token.

        Returns:
            The response containing the verification information.
        """
        url = f"{self.base_url}/v1/register/{number}/verify/{token}"
        return await make_request(self._module_session, "POST", url)
