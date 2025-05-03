"""Tests for the Groups module."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from signal_messenger.modules.groups import GroupsModule


@pytest.fixture
def groups_module():
    """Create a GroupsModule instance for testing."""
    session = AsyncMock()
    return GroupsModule("http://localhost:8080", session)


@pytest.mark.asyncio
async def test_get_groups(groups_module):
    """Test the get_groups method."""
    # Mock response data
    response_data = {
        "groups": [
            {"id": "group1", "name": "Group 1", "members": ["+1234567890"]},
            {
                "id": "group2",
                "name": "Group 2",
                "members": ["+1234567890", "+0987654321"],
            },
        ]
    }

    # Mock the make_request function
    with patch(
        "signal_messenger.modules.groups.make_request", return_value=response_data
    ):
        # Call the method
        result = await groups_module.get_groups("+1234567890")

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "group1"
        assert result[0]["name"] == "Group 1"
        assert result[1]["id"] == "group2"
        assert result[1]["name"] == "Group 2"


@pytest.mark.asyncio
async def test_get_groups_list_response(groups_module):
    """Test the get_groups method with a list response."""
    # Mock response data
    response_data = [
        {"id": "group1", "name": "Group 1", "members": ["+1234567890"]},
        {"id": "group2", "name": "Group 2", "members": ["+1234567890", "+0987654321"]},
    ]

    # Mock the make_request function
    with patch(
        "signal_messenger.modules.groups.make_request", return_value=response_data
    ):
        # Call the method
        result = await groups_module.get_groups("+1234567890")

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "group1"
        assert result[0]["name"] == "Group 1"
        assert result[1]["id"] == "group2"
        assert result[1]["name"] == "Group 2"


@pytest.mark.asyncio
async def test_get_groups_single_response(groups_module):
    """Test the get_groups method with a single group response."""
    # Mock response data
    response_data = {"id": "group1", "name": "Group 1", "members": ["+1234567890"]}

    # Mock the make_request function
    with patch(
        "signal_messenger.modules.groups.make_request", return_value=response_data
    ):
        # Call the method
        result = await groups_module.get_groups("+1234567890")

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == "group1"
        assert result[0]["name"] == "Group 1"


@pytest.mark.asyncio
async def test_get_group(groups_module):
    """Test the get_group method."""
    # Mock response data
    response_data = {"id": "group1", "name": "Group 1", "members": ["+1234567890"]}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.get_group("+1234567890", "group1")

        # Verify the result
        assert result["id"] == "group1"
        assert result["name"] == "Group 1"
        assert result["members"] == ["+1234567890"]

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "GET",
            "http://localhost:8080/v1/groups/+1234567890/group1",
        )


@pytest.mark.asyncio
async def test_create_group(groups_module):
    """Test the create_group method."""
    # Mock response data
    response_data = {"success": True, "groupId": "new_group_id"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.create_group(
            "+1234567890", "New Group", ["+0987654321"]
        )

        # Verify the result
        assert result["success"] is True
        assert result["groupId"] == "new_group_id"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "POST",
            "http://localhost:8080/v1/groups/+1234567890",
            data={"name": "New Group", "members": ["+0987654321"]},
        )


@pytest.mark.asyncio
async def test_create_group_with_avatar(groups_module):
    """Test the create_group method with avatar."""
    # Mock response data
    response_data = {"success": True, "groupId": "new_group_id"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.create_group(
            "+1234567890", "New Group", ["+0987654321"], "avatar_url"
        )

        # Verify the result
        assert result["success"] is True
        assert result["groupId"] == "new_group_id"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "POST",
            "http://localhost:8080/v1/groups/+1234567890",
            data={
                "name": "New Group",
                "members": ["+0987654321"],
                "avatar": "avatar_url",
            },
        )


@pytest.mark.asyncio
async def test_update_group(groups_module):
    """Test the update_group method."""
    # Mock response data
    response_data = {"success": True, "message": "Group updated"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.update_group(
            "+1234567890", "group1", name="Updated Group", description="New description"
        )

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Group updated"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "PUT",
            "http://localhost:8080/v1/groups/+1234567890/group1",
            data={"name": "Updated Group", "description": "New description"},
        )


@pytest.mark.asyncio
async def test_delete_group(groups_module):
    """Test the delete_group method."""
    # Mock response data
    response_data = {"success": True, "message": "Group deleted"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.delete_group("+1234567890", "group1")

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Group deleted"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "DELETE",
            "http://localhost:8080/v1/groups/+1234567890/group1",
        )


@pytest.mark.asyncio
async def test_add_members(groups_module):
    """Test the add_members method."""
    # Mock response data
    response_data = {"success": True, "message": "Members added"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.add_members(
            "+1234567890", "group1", ["+0987654321", "+5555555555"]
        )

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Members added"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "POST",
            "http://localhost:8080/v1/groups/+1234567890/group1/members",
            data={"members": ["+0987654321", "+5555555555"]},
        )


@pytest.mark.asyncio
async def test_remove_members(groups_module):
    """Test the remove_members method."""
    # Mock response data
    response_data = {"success": True, "message": "Members removed"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.remove_members(
            "+1234567890", "group1", ["+0987654321"]
        )

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Members removed"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "DELETE",
            "http://localhost:8080/v1/groups/+1234567890/group1/members",
            data={"members": ["+0987654321"]},
        )


@pytest.mark.asyncio
async def test_join_group(groups_module):
    """Test the join_group method."""
    # Mock response data
    response_data = {"success": True, "message": "Joined group"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.join_group("+1234567890", "group1")

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Joined group"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "POST",
            "http://localhost:8080/v1/groups/+1234567890/group1/join",
        )


@pytest.mark.asyncio
async def test_leave_group(groups_module):
    """Test the leave_group method."""
    # Mock response data
    response_data = {"success": True, "message": "Left group"}

    # Mock the make_request function
    make_request_mock = AsyncMock(return_value=response_data)
    with patch("signal_messenger.modules.groups.make_request", make_request_mock):
        # Call the method
        result = await groups_module.leave_group("+1234567890", "group1")

        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Left group"

        # Verify the make_request call
        make_request_mock.assert_called_once_with(
            groups_module._module_session,
            "POST",
            "http://localhost:8080/v1/groups/+1234567890/group1/leave",
        )
