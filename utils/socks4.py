import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
from typing import Tuple
from config import TEST_URLS, TIMEOUT


async def check_socks4_proxy(proxy: str, semaphore: asyncio.Semaphore) -> Tuple[str, bool]:
    async with semaphore:
        for test_url in TEST_URLS:
            try:
                connector = ProxyConnector.from_url(f'socks4://{proxy}')
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(
                        test_url, 
                        timeout=aiohttp.ClientTimeout(total=TIMEOUT)
                    ) as response:
                        if response.status == 200:
                            return proxy, True
            except (
                aiohttp.ClientError,
                asyncio.TimeoutError,
                Exception
            ):
                continue
        
        return proxy, False