from typing import List

def save_proxies(proxies: List[str], filename: str) -> None:
    with open(filename, 'w') as f:
        f.write('\n'.join(sorted(proxies)))


def load_proxies(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
