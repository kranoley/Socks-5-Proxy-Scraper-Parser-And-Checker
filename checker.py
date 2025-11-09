import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
from typing import List, Set, Tuple
from config import TEST_URLS, TIMEOUT, CONCURRENT_CHECKS

async def check_proxy(proxy: str, semaphore: asyncio.Semaphore) -> Tuple[str, bool]:
    async with semaphore:
        for test_url in TEST_URLS:
            try:
                connector = ProxyConnector.from_url(f'socks5://{proxy}')
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as response:
                        if response.status == 200:
                            return proxy, True
            except Exception:
                continue
        return proxy, False


async def check_proxies(proxies: Set[str]) -> List[str]:
    semaphore = asyncio.Semaphore(CONCURRENT_CHECKS)
    tasks = [check_proxy(proxy, semaphore) for proxy in proxies]
    
    results = []
    total = len(tasks)
    completed = 0
    
    for coro in asyncio.as_completed(tasks):
        proxy, is_alive = await coro
        completed += 1
        
        if is_alive:
            results.append(proxy)
            print(f'[✓] {proxy} | Alive: {len(results)} | Progress: {completed}/{total}')
        else:
            print(f'[✗] {proxy} | Progress: {completed}/{total}', end='\r')
    
    return results
