"""Stickers module for the Signal Messenger Python API."""

from typing import Any, BinaryIO, Dict, List, Optional, Union

import aiohttp

from signal_messenger.utils import make_request


class StickersModule:
    """Stickers module for the Signal Messenger Python API.

    This module provides access to sticker pack management functionality.
    """

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        """Initialize the Stickers module.

        Args:
            base_url: The base URL of the API.
            session: The aiohttp session.
        """
        self.base_url = base_url
        self._module_session = session

    async def get_sticker_packs(self, number: str) -> List[Dict[str, Any]]:
        """Get all sticker packs for a phone number.

        Args:
            number: The registered phone number.

        Returns:
            A list of sticker packs.
        """
        url = f"{self.base_url}/v1/stickers/{number}"
        response = await make_request(self._module_session, "GET", url)
        if isinstance(response, dict) and "stickers" in response:
            return response["stickers"]
        elif isinstance(response, list):
            return response
        return [response]

    async def get_sticker_pack(self, number: str, pack_id: str) -> Dict[str, Any]:
        """Get a specific sticker pack.

        Args:
            number: The registered phone number.
            pack_id: The sticker pack ID.

        Returns:
            The sticker pack details.
        """
        url = f"{self.base_url}/v1/stickers/{number}/{pack_id}"
        return await make_request(self._module_session, "GET", url)

    async def install_sticker_pack(
        self, number: str, pack_id: str, pack_key: str
    ) -> Dict[str, Any]:
        """Install a sticker pack.

        Args:
            number: The registered phone number.
            pack_id: The sticker pack ID.
            pack_key: The sticker pack key.

        Returns:
            The response containing the sticker pack installation information.
        """
        url = f"{self.base_url}/v1/stickers/{number}"
        data = {"packId": pack_id, "packKey": pack_key}
        return await make_request(self._module_session, "POST", url, data=data)

    async def uninstall_sticker_pack(self, number: str, pack_id: str) -> Dict[str, Any]:
        """Uninstall a sticker pack.

        Args:
            number: The registered phone number.
            pack_id: The sticker pack ID.

        Returns:
            The response containing the sticker pack uninstallation information.
        """
        url = f"{self.base_url}/v1/stickers/{number}/{pack_id}"
        return await make_request(self._module_session, "DELETE", url)

    async def upload_sticker_pack(
        self,
        number: str,
        title: str,
        author: str,
        cover: Union[bytes, BinaryIO],
        stickers: List[Dict[str, Union[bytes, BinaryIO, str]]],
    ) -> Dict[str, Any]:
        """Upload a new sticker pack.

        Args:
            number: The registered phone number.
            title: The sticker pack title.
            author: The sticker pack author.
            cover: The cover image data as bytes or a file-like object.
            stickers: The list of stickers, each with 'image' and 'emoji' keys.

        Returns:
            The response containing the sticker pack upload information.
        """
        url = f"{self.base_url}/v1/stickers/{number}/upload"

        # Use aiohttp's FormData to build a multipart request
        from aiohttp import FormData

        data = FormData()
        data.add_field("title", title)
        data.add_field("author", author)
        data.add_field("cover", cover)

        for i, sticker in enumerate(stickers):
            data.add_field(f"sticker_{i}", sticker["image"])
            data.add_field(f"emoji_{i}", sticker["emoji"])

        # Use the session directly for multipart data
        async with self._module_session.post(url, data=data) as response:
            from signal_messenger.utils import handle_response

            return await handle_response(response)
