import asyncio
import aiohttp
from typing import Tuple
from config import TEST_URLS, TIMEOUT


async def check_http_proxy(proxy: str, semaphore: asyncio.Semaphore) -> Tuple[str, bool]:
    async with semaphore:
        for test_url in TEST_URLS:
            try:
                proxy_url = f'http://{proxy}'
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        test_url,
                        proxy=proxy_url,
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