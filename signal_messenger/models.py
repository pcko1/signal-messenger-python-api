"""Data models for the Signal Messenger Python API."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LoggingConfig(BaseModel):
    """Logging configuration model."""

    level: str = ""
    Level: str = ""

    def __init__(self, **data):
        """Initialize the logging configuration model.

        This handles both 'level' and 'Level' fields from the API.
        """
        super().__init__(**data)
        if not self.level and self.Level:
            self.level = self.Level


class Configuration(BaseModel):
    """API configuration model."""

    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    Logging: Optional[LoggingConfig] = None

    def __init__(self, **data):
        """Initialize the configuration model.

        This handles both 'logging' and 'Logging' fields from the API.
        """
        super().__init__(**data)
        if not self.logging.level and self.Logging:
            self.logging = self.Logging


class Capabilities(BaseModel):
    """API capabilities model."""

    model_config = ConfigDict(extra="allow")


class About(BaseModel):
    """API information model."""

    build: int
    capabilities: Dict[str, List[str]] = Field(default_factory=dict)
    mode: str
    version: str
    versions: List[str]


class AccountSettings(BaseModel):
    """Account settings model."""

    trust_mode: str


# Account Models
class AccountRegistrationResponse(BaseModel):
    """Account registration response model."""

    model_config = ConfigDict(extra="allow")

    captcha_required: Optional[bool] = None
    verification_required: Optional[bool] = None


class AccountVerificationResponse(BaseModel):
    """Account verification response model."""

    model_config = ConfigDict(extra="allow")

    uuid: Optional[str] = None
    number: Optional[str] = None
    registered: Optional[bool] = None


class AccountDetails(BaseModel):
    """Account details model."""

    model_config = ConfigDict(extra="allow")

    uuid: Optional[str] = None
    number: Optional[str] = None
    registered: Optional[bool] = None


# Device Models
class DeviceType(str, Enum):
    """Device type enum."""

    MOBILE = "mobile"
    DESKTOP = "desktop"
    UNKNOWN = "unknown"


class Device(BaseModel):
    """Device model."""

    model_config = ConfigDict(extra="allow")

    id: int
    name: Optional[str] = None
    created: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    type: Optional[DeviceType] = DeviceType.UNKNOWN


class LinkedDevice(Device):
    """Linked device model."""

    linked: bool = True


# Message Models
class MessageType(str, Enum):
    """Message type enum."""

    INCOMING = "incoming"
    OUTGOING = "outgoing"
    SYNC = "sync"


class MessageAttachment(BaseModel):
    """Message attachment model."""

    model_config = ConfigDict(extra="allow")

    id: str
    content_type: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None


class MessageMention(BaseModel):
    """Message mention model."""

    model_config = ConfigDict(extra="allow")

    uuid: str
    start: int
    length: int


class MessageQuote(BaseModel):
    """Message quote model."""

    model_config = ConfigDict(extra="allow")

    id: int
    author: str
    text: str
    attachments: List[MessageAttachment] = Field(default_factory=list)


class Message(BaseModel):
    """Message model."""

    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    type: Optional[MessageType] = None
    source: Optional[str] = None
    source_uuid: Optional[str] = None
    source_device: Optional[int] = None
    timestamp: Optional[int] = None
    server_timestamp: Optional[int] = None
    server_delivered_timestamp: Optional[int] = None
    has_legacy_message: Optional[bool] = None
    unidentified_sender: Optional[bool] = None
    message: Optional[str] = None
    expiration: Optional[int] = None
    is_view_once: Optional[bool] = None
    is_story: Optional[bool] = None
    attachments: List[MessageAttachment] = Field(default_factory=list)
    mentions: List[MessageMention] = Field(default_factory=list)
    quote: Optional[MessageQuote] = None
    reactions: List["Reaction"] = Field(default_factory=list)
    sticker: Optional["Sticker"] = None
    group_info: Optional["GroupInfo"] = None


# Group Models
class GroupRole(str, Enum):
    """Group role enum."""

    ADMINISTRATOR = "ADMINISTRATOR"
    DEFAULT = "DEFAULT"


class GroupMember(BaseModel):
    """Group member model."""

    model_config = ConfigDict(extra="allow")

    uuid: Optional[str] = None
    number: Optional[str] = None
    role: Optional[GroupRole] = GroupRole.DEFAULT


class GroupInfo(BaseModel):
    """Group info model."""

    model_config = ConfigDict(extra="allow")

    group_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    members: List[GroupMember] = Field(default_factory=list)
    pending_members: List[GroupMember] = Field(default_factory=list)
    requesting_members: List[GroupMember] = Field(default_factory=list)
    admins: List[GroupMember] = Field(default_factory=list)
    active: Optional[bool] = None
    blocked: Optional[bool] = None
    permission_add_member: Optional[str] = None
    permission_edit_details: Optional[str] = None
    permission_send_message: Optional[str] = None
    link: Optional[str] = None
    message_expiration_time: Optional[int] = None


class Group(BaseModel):
    """Group model."""

    model_config = ConfigDict(extra="allow")

    id: str
    internal_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None
    members: List[GroupMember] = Field(default_factory=list)
    pending_members: List[GroupMember] = Field(default_factory=list)
    requesting_members: List[GroupMember] = Field(default_factory=list)
    admins: List[GroupMember] = Field(default_factory=list)
    active: Optional[bool] = None
    blocked: Optional[bool] = None
    permission_add_member: Optional[str] = None
    permission_edit_details: Optional[str] = None
    permission_send_message: Optional[str] = None
    link: Optional[str] = None
    message_expiration_time: Optional[int] = None


# Attachment Models
class Attachment(BaseModel):
    """Attachment model."""

    model_config = ConfigDict(extra="allow")

    id: str
    content_type: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None
    stored_filename: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    voice_note: Optional[bool] = None
    caption: Optional[str] = None
    preview: Optional[Dict[str, Any]] = None


# Profile Models
class Profile(BaseModel):
    """Profile model."""

    model_config = ConfigDict(extra="allow")

    uuid: Optional[str] = None
    number: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    about: Optional[str] = None
    about_emoji: Optional[str] = None
    avatar: Optional[str] = None
    color: Optional[str] = None
    profile_sharing: Optional[bool] = None
    capabilities: List[str] = Field(default_factory=list)


# Identity Models
class TrustLevel(str, Enum):
    """Trust level enum."""

    TRUSTED_UNVERIFIED = "TRUSTED_UNVERIFIED"
    TRUSTED_VERIFIED = "TRUSTED_VERIFIED"
    UNTRUSTED = "UNTRUSTED"


class Identity(BaseModel):
    """Identity model."""

    model_config = ConfigDict(extra="allow")

    uuid: Optional[str] = None
    number: Optional[str] = None
    trust_level: Optional[TrustLevel] = None
    added: Optional[datetime] = None
    fingerprint: Optional[str] = None
    safety_number: Optional[str] = None
    scanned_safety_number: Optional[str] = None


# Reaction Models
class Reaction(BaseModel):
    """Reaction model."""

    model_config = ConfigDict(extra="allow")

    emoji: str
    author: Optional[str] = None
    author_uuid: Optional[str] = None
    target_author: Optional[str] = None
    target_author_uuid: Optional[str] = None
    timestamp: Optional[int] = None
    received_timestamp: Optional[int] = None


# Receipt Models
class ReceiptType(str, Enum):
    """Receipt type enum."""

    READ = "read"
    VIEWED = "viewed"
    DELIVERY = "delivery"


class Receipt(BaseModel):
    """Receipt model."""

    model_config = ConfigDict(extra="allow")

    type: ReceiptType
    sender: Optional[str] = None
    sender_uuid: Optional[str] = None
    sender_device: Optional[int] = None
    timestamp: Optional[int] = None
    when: Optional[int] = None


# Search Models
class SearchResult(BaseModel):
    """Search result model."""

    model_config = ConfigDict(extra="allow")

    results: List[Any] = Field(default_factory=list)
    query: Optional[str] = None


# Sticker Models
class Sticker(BaseModel):
    """Sticker model."""

    model_config = ConfigDict(extra="allow")

    id: int
    emoji: Optional[str] = None
    pack_id: Optional[str] = None
    pack_key: Optional[str] = None
    attachment: Optional[Attachment] = None


class StickerPack(BaseModel):
    """Sticker pack model."""

    model_config = ConfigDict(extra="allow")

    id: str
    key: str
    title: Optional[str] = None
    author: Optional[str] = None
    stickers: List[Sticker] = Field(default_factory=list)
    cover: Optional[Sticker] = None
    installed: Optional[bool] = None


# Contact Models
class Contact(BaseModel):
    """Contact model."""

    model_config = ConfigDict(extra="allow")

    uuid: Optional[str] = None
    number: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    color: Optional[str] = None
    profile_key: Optional[str] = None
    blocked: Optional[bool] = None
    expiration: Optional[int] = None
