PROXY_SOURCES = [
    'https://sockslist.us/Raw',
    'https://proxymania.su/free-proxy?type=SOCKS5',
    'https://proxyverity.com/proxies-by-types/socks5/',
    'https://www.freeproxy.world/?type=socks5',
    'https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt',
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/watchttvv/free-proxy-list/refs/heads/main/proxy.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt",
]
TEST_URLS = [
    'http://httpbin.org/ip',
]

TIMEOUT = 5
FETCH_TIMEOUT = 30
CONCURRENT_CHECKS = 1000
OUTPUT_FILE = 'live_proxy.txt'
