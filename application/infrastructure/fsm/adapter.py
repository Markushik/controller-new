from abc import abstractmethod
from datetime import timedelta
from typing import Literal, Optional, TypeAlias

from nats.aio.client import Client
from nats.js.errors import BadRequestError
from nats.js.kv import KeyValue
from pathvalidate import is_valid_filename

ExpiryT: TypeAlias = float | timedelta


class KvNameBuilder:
    @abstractmethod
    def build(self, part: Literal["state", "data"]) -> str:
        pass


class DefaultKvNameBuilder(KvNameBuilder):
    def __init__(self, prefix: str = "fsm", separator: str = "_"):
        self.prefix = prefix
        self.separator = separator

        if not is_valid_filename(self.build("state")):  # build key for validate
            raise ValueError(
                "Invalid kv builder "
                f"prefix or separator ({self.prefix!r}, "
                f"{self.separator!r})"
            )

    def build(self, part: Literal["state", "data"]) -> str:
        return f"{self.prefix}{self.separator}{part}"


class NatsAdapter:
    def __init__(
            self,
            client: Client,
            kv_name_builder: Optional[KvNameBuilder] = None,
            state_ttl: Optional[ExpiryT] = None,
            data_ttl: Optional[ExpiryT] = None,
    ):
        if kv_name_builder is None:
            kv_name_builder = DefaultKvNameBuilder()
        self.client = client
        self.kv_name_builder = kv_name_builder
        self._state_kv: Optional[KeyValue] = None
        self._data_kv: Optional[KeyValue] = None
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl

    @property
    def state_kv(self) -> KeyValue:
        if self._state_kv is None:
            raise RuntimeError("'state_kv' is not created")
        return self._state_kv

    @property
    def data_kv(self) -> KeyValue:
        if self._data_kv is None:
            raise RuntimeError("'data_kv' is not created")
        return self._data_kv

    async def close(self) -> None:
        await self.client.close()

    async def create_kv(self) -> None:
        js = self.client.jetstream()
        state_kv = self.kv_name_builder.build("state")
        data_kv = self.kv_name_builder.build("data")

        try:
            self._state_kv = await js.create_key_value(bucket=state_kv, ttl=self.state_ttl)
        except BadRequestError:
            self._state_kv = await js.key_value(bucket=state_kv)

        try:
            self._data_kv = await js.create_key_value(bucket=data_kv, ttl=self.data_ttl)
        except BadRequestError:
            self._data_kv = await js.key_value(bucket=data_kv)
