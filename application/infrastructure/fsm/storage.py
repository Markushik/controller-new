from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional, cast

import lz4.frame
import ormsgpack
from aiogram import Bot
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import DEFAULT_DESTINY, BaseStorage, StateType, StorageKey
from nats.js.errors import KeyNotFoundError
from ormsgpack.ormsgpack import packb, unpackb

from .adapter import NatsAdapter


class KeyBuilder(ABC):
    @abstractmethod
    def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> str:
        pass


class DefaultKeyBuilder(KeyBuilder):
    def __init__(
            self,
            *,
            prefix: str = "fsm",
            separator: str = ":",
            with_bot_id: bool = False,
            with_destiny: bool = False,
    ) -> None:
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_destiny = with_destiny

    def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> str:
        parts = [self.prefix]
        if self.with_bot_id:
            parts.append(str(key.bot_id))
        parts.extend([str(key.chat_id), str(key.user_id)])
        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(
                "Nats key builder is not configured to use key destiny "
                "other the default.\n"
                "\n"
                "Probably, you should set `with_destiny=True` in "
                "for DefaultKeyBuilder.\n"
                "E.g: `NatsStorage(adapter, "
                "key_builder=DefaultKeyBuilder(with_destiny=True))`"
            )
        parts.append(part)
        return self.separator.join(parts)


class NatsStorage(BaseStorage):
    def __init__(self, adapter: NatsAdapter, key_builder: Optional[KeyBuilder] = None):
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.adapter = adapter
        self.key_builder = key_builder

    async def close(self) -> None:
        await self.adapter.close()

    async def set_state(self, bot: Bot, key: StorageKey, state: StateType = None) -> None:
        nats_key = self.key_builder.build(key, "state")
        if state is None:
            await self.adapter.state_kv.delete(nats_key)
        else:
            if isinstance(state, State):
                state = state.state
            await self.adapter.state_kv.put(nats_key, ormsgpack.packb(state))

    async def get_state(self, bot: Bot, key: StorageKey) -> Optional[str]:
        nats_key = self.key_builder.build(key, "state")
        try:
            entry = await self.adapter.state_kv.get(nats_key)
        except KeyNotFoundError:
            value = None
        else:
            value = entry.value
        if value is not None:
            return cast(str, ormsgpack.unpackb(value))
        return value

    async def set_data(self, bot: Bot, key: StorageKey, data: Dict[str, Any]) -> None:
        nats_key = self.key_builder.build(key, "data")
        if not data:
            await self.adapter.data_kv.delete(nats_key)
        await self.adapter.data_kv.put(nats_key, ormsgpack.packb(data))

    async def get_data(self, bot: Bot, key: StorageKey) -> Dict[str, Any]:
        nats_key = self.key_builder.build(key, "data")
        try:
            entry = await self.adapter.data_kv.get(nats_key)
        except KeyNotFoundError:
            value = None
        else:
            value = entry.value
        if value is None:
            return {}
        return cast(Dict[str, Any], ormsgpack.unpackb(value))
