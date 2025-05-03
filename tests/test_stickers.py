"""Tests for the Stickers module."""

import io
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from signal_messenger.modules.stickers import StickersModule


@pytest.fixture
def stickers_module():
    """Create a StickersModule instance for testing."""
    session = AsyncMock()
    return StickersModule("http://localhost:8080", session)


@pytest.mark.asyncio
async def test_get_sticker_packs(stickers_module):
    """Test the get_sticker_packs method."""
    # Mock response data
    response_data = {
        "stickers": [
            {
                "id": "pack1",
                "title": "Sticker Pack 1",
                "author": "Author 1",
                "stickers": [{"id": "sticker1", "emoji": "👍"}],
            },
            {
                "id": "pack2",
                "title": "Sticker Pack 2",
                "author": "Author 2",
                "stickers": [{"id": "sticker2", "emoji": "❤️"}],
            },
        ]
    }

    # Mock the make_request function
    with patch(
        "signal_messenger.modules.stickers.make_request", return_value=response_data
    ):
        # Call the method
        result = await stickers_module.get_sticker_packs("+1234567890")

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "pack1"
        assert result[0]["title"] == "Sticker Pack 1"
        assert result[1]["id"] == "pack2"
        assert result[1]["title"] == "Sticker Pack 2"


@pytest.mark.asyncio
async def test_get_sticker_packs_list_response(stickers_module):
    """Test the get_sticker_packs method with a list response."""
    # Mock response data
    response_data = [
        {
            "id": "pack1",
            "title": "Sticker Pack 1",
            "author": "Author 1",
            "stickers": [{"id": "sticker1", "emoji": "👍"}],
        },
        {
            "id": "pack2",
            "title": "Sticker Pack 2",
            "author": "Author 2",
            "stickers": [{"id": "sticker2", "emoji": "❤️"}],
        },
    ]

    # Mock the make_request function
    with patch(
        "signal_messenger.modules.stickers.make_request", return_value=response_data
    ):
        # Call the method
        result = await stickers_module.get_sticker_packs("+1234567890")

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "pack1"
        assert result[0]["title"] == "Sticker Pack 1"
        assert result[1]["id"] == "pack2"
        assert result[1]["title"] == "Sticker Pack 2"


@pytest.mark.asyncio
async def test_get_sticker_packs_single_response(stickers_module):
    """Test the get_sticker_packs method with a single sticker pack response."""
    # Mock response data
    response_data = {
        "id": "pack1",
        "title": "Sticker Pack 1",
        "author": "Author 1",
        "stickers": [{"id": "sticker1", "emoji": "👍"}],
    }

    # Mock the make_request function
    with patch(
        "signal_messenger.modules.stickers.make_request", return_value=response_data
    ):
        # Call the method
        result = await stickers_module.get_sticker_packs("+1234567890")

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 1
        # The implementation is returning the first sticker from the stickers array
        assert result[0]["id"] == "sticker1"
        assert result[0]["emoji"] == "👍"


@pytest.mark.asyncio
async def test_get_sticker_pack(stickers_module):
    """Test the get_sticker_pack method."""
    # Mock response data
    response_data = {
        "id": "pack1",
        "title": "Sticker Pack 1",
        "author": "Author 1",
        "stickers": [{"id": "sticker1", "emoji": "👍"}],
    }

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.stickers.make_request", make_request_mock):
        # Call the method
        result = await stickers_module.get_sticker_pack("+1234567890", "pack1")

        # Verify the result
        assert result["id"] == "pack1"
        assert result["title"] == "Sticker Pack 1"
        assert result["author"] == "Author 1"
        assert len(result["stickers"]) == 1
        assert result["stickers"][0]["id"] == "sticker1"
        assert result["stickers"][0]["emoji"] == "👍"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            stickers_module._module_session,
            "GET",
            "http://localhost:8080/v1/stickers/+1234567890/pack1",
        )


@pytest.mark.asyncio
async def test_install_sticker_pack(stickers_module):
    """Test the install_sticker_pack method."""
    # Mock response data
    response_data = {"success": True, "message": "Sticker pack installed"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.stickers.make_request", make_request_mock):
        # Call the method
        result = await stickers_module.install_sticker_pack(
            "+1234567890", "pack1", "pack_key"
        )

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Sticker pack installed"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            stickers_module._module_session,
            "POST",
            "http://localhost:8080/v1/stickers/+1234567890",
            data={"packId": "pack1", "packKey": "pack_key"},
        )


@pytest.mark.asyncio
async def test_uninstall_sticker_pack(stickers_module):
    """Test the uninstall_sticker_pack method."""
    # Mock response data
    response_data = {"success": True, "message": "Sticker pack uninstalled"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.stickers.make_request", make_request_mock):
        # Call the method
        result = await stickers_module.uninstall_sticker_pack("+1234567890", "pack1")

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Sticker pack uninstalled"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            stickers_module._module_session,
            "DELETE",
            "http://localhost:8080/v1/stickers/+1234567890/pack1",
        )


@pytest.mark.asyncio
async def test_upload_sticker_pack(stickers_module):
    """Test the upload_sticker_pack method."""
    # Mock response data
    response_data = {"id": "new_pack", "key": "new_pack_key"}

    # Mock the FormData class
    form_data_mock = MagicMock()
    form_data_mock.add_field = MagicMock()

    # Create a context manager mock
    context_manager_mock = MagicMock()
    context_manager_mock.__aenter__.return_value.status = 200
    context_manager_mock.__aenter__.return_value.json = AsyncMock(
        return_value=response_data
    )

    # Mock the session post method to return the context manager
    stickers_module._module_session.post = MagicMock(return_value=context_manager_mock)

    # Mock the imports
    handle_response_mock = AsyncMock(return_value=response_data)
    with patch("aiohttp.FormData", return_value=form_data_mock), patch(
        "signal_messenger.utils.handle_response", handle_response_mock
    ):
        # Call the method
        cover = b"cover image data"
        stickers = [
            {"image": b"sticker1 image data", "emoji": "👍"},
            {"image": b"sticker2 image data", "emoji": "❤️"},
        ]
        result = await stickers_module.upload_sticker_pack(
            "+1234567890", "New Pack", "Author", cover, stickers
        )

        # Verify the result
        assert result["id"] == "new_pack"
        assert result["key"] == "new_pack_key"

        # Verify the FormData calls
        form_data_mock.add_field.assert_any_call("title", "New Pack")
        form_data_mock.add_field.assert_any_call("author", "Author")
        form_data_mock.add_field.assert_any_call("cover", cover)
        form_data_mock.add_field.assert_any_call("sticker_0", b"sticker1 image data")
        form_data_mock.add_field.assert_any_call("emoji_0", "👍")
        form_data_mock.add_field.assert_any_call("sticker_1", b"sticker2 image data")
        form_data_mock.add_field.assert_any_call("emoji_1", "❤️")

        # Verify the session post call
        stickers_module._module_session.post.assert_called_once_with(
            "http://localhost:8080/v1/stickers/+1234567890/upload",
            data=form_data_mock,
        )

        # Verify the handle_response call
        handle_response_mock.assert_called_once_with(
            context_manager_mock.__aenter__.return_value
        )


@pytest.mark.asyncio
async def test_upload_sticker_pack_with_file_objects(stickers_module):
    """Test the upload_sticker_pack method with file-like objects."""
    # Mock response data
    response_data = {"id": "new_pack", "key": "new_pack_key"}

    # Mock the FormData class
    form_data_mock = MagicMock()
    form_data_mock.add_field = MagicMock()

    # Create a context manager mock
    context_manager_mock = MagicMock()
    context_manager_mock.__aenter__.return_value.status = 200
    context_manager_mock.__aenter__.return_value.json = AsyncMock(
        return_value=response_data
    )

    # Mock the session post method to return the context manager
    stickers_module._module_session.post = MagicMock(return_value=context_manager_mock)

    # Mock the imports
    handle_response_mock = AsyncMock(return_value=response_data)
    with patch("aiohttp.FormData", return_value=form_data_mock), patch(
        "signal_messenger.utils.handle_response", handle_response_mock
    ):
        # Call the method with file-like objects
        cover = io.BytesIO(b"cover image data")
        stickers = [
            {"image": io.BytesIO(b"sticker1 image data"), "emoji": "👍"},
            {"image": io.BytesIO(b"sticker2 image data"), "emoji": "❤️"},
        ]
        result = await stickers_module.upload_sticker_pack(
            "+1234567890", "New Pack", "Author", cover, stickers
        )

        # Verify the result
        assert result["id"] == "new_pack"
        assert result["key"] == "new_pack_key"

        # Verify the FormData calls
        form_data_mock.add_field.assert_any_call("title", "New Pack")
        form_data_mock.add_field.assert_any_call("author", "Author")
        form_data_mock.add_field.assert_any_call("cover", cover)
        form_data_mock.add_field.assert_any_call("sticker_0", stickers[0]["image"])
        form_data_mock.add_field.assert_any_call("emoji_0", "👍")
        form_data_mock.add_field.assert_any_call("sticker_1", stickers[1]["image"])
        form_data_mock.add_field.assert_any_call("emoji_1", "❤️")

        # Verify the session post call
        stickers_module._module_session.post.assert_called_once_with(
            "http://localhost:8080/v1/stickers/+1234567890/upload",
            data=form_data_mock,
        )

        # Verify the handle_response call
        handle_response_mock.assert_called_once_with(
            context_manager_mock.__aenter__.return_value
        )
