"""Small normalized boundary around the Databricks Genie Conversation API.

The rest of the application consumes these value objects rather than SDK
response shapes.  This module deliberately does not parse control JSON or
execute query attachments; those responsibilities belong to the protocol and
trusted-query boundaries.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class MessageState(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class ConversationRef:
    conversation_id: str
    message_id: str


@dataclass(frozen=True)
class NormalizedMessage:
    conversation_id: str
    message_id: str
    state: MessageState
    text: str = ""
    raw: Any = None


class GenieClient(Protocol):
    """Normalized operations required by orchestration."""

    def start_conversation(self, *, space_id: str, content: str) -> ConversationRef: ...

    def continue_conversation(self, *, conversation_id: str, content: str) -> ConversationRef: ...

    def get_message(self, *, conversation_id: str, message_id: str) -> NormalizedMessage: ...


class GenieClientError(RuntimeError):
    """Recoverable boundary error; callers decide retry/fallback policy."""


class CanonicalGenieBoundary:
    """Canonical application boundary around a transport implementation.

    The transport is injected so the domain layer depends on this module's
    stable interface rather than on Databricks SDK or legacy route objects.
    """

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    @property
    def enabled(self) -> bool:
        return bool(getattr(self._transport, "enabled", False))

    def start(self, case_id: str) -> dict[str, Any]:
        return self._transport.start(case_id)

    def next(self, conversation_id: str, context: str, case_id: str) -> dict[str, Any]:
        return self._transport.next(conversation_id, context, case_id)

    def ask(self, conversation_id: str, content: str) -> str:
        return self._transport.ask(conversation_id, content)


def normalize_message(response: Any, *, conversation_id: str | None = None, message_id: str | None = None) -> NormalizedMessage:
    """Convert an SDK message-like object into a bounded internal value."""
    cid = conversation_id or str(getattr(response, "conversation_id", ""))
    mid = message_id or str(getattr(response, "message_id", ""))
    if not cid or not mid:
        raise GenieClientError("Genie response is missing conversation/message identity")
    raw_state_value = getattr(response, "status", getattr(response, "state", "PENDING"))
    raw_state = str(getattr(raw_state_value, "value", raw_state_value)).upper()
    try:
        state = MessageState(raw_state)
    except ValueError as exc:
        raise GenieClientError(f"unknown Genie message state: {raw_state}") from exc
    text = getattr(response, "content", "") or ""
    return NormalizedMessage(cid, mid, state, str(text), response)
