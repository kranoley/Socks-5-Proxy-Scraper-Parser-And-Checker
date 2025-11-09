import asyncio
import aiohttp
from typing import List
from config import FETCH_TIMEOUT

async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=FETCH_TIMEOUT)) as response:
            return await response.text()
    except Exception:
        return ''


async def fetch_all_sources(urls: List[str]) -> str:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return '\n'.join(results)
