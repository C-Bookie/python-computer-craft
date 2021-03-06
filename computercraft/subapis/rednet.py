from typing import Any, List
from .base import BaseSubAPI, LuaNum, list_return, nil_return, int_return, bool_return


class RednetAPI(BaseSubAPI):
    _API = 'rednet'

    async def open(self, side: str):
        return nil_return(await self._send('open', side))

    async def close(self, side: str):
        return nil_return(await self._send('close', side))

    async def send(self, receiverID: int, message: Any, protocol: str=None):
        return nil_return(await self._send('send', receiverID, message, protocol))

    async def broadcast(self, message: Any, protocol: str=None):
        return nil_return(await self._send('broadcast', message, protocol))

    async def receive(self, protocolFilter: str=None, timeout: LuaNum=None) -> int:
        return int_return(await self._send('receive', protocolFilter, timeout))

    async def isOpen(self, side: str) -> bool:
        return bool_return(await self._send('isOpen', side))

    async def host(self, protocol: str, hostname: str):
        return nil_return(await self._send('host', protocol, hostname))

    async def unhost(self, protocol: str, hostname: str):
        return nil_return(await self._send('unhost', protocol, hostname))

    async def lookup(self, protocol: str, hostname: str) -> List[int]:
        return list_return(await self._send('lookup', protocol, hostname))
