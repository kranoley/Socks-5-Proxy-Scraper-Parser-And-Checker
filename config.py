PROXY_SOURCES = [
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
]
TEST_URLS = [
    'http://httpbin.org/ip',
]

TIMEOUT = 5
FETCH_TIMEOUT = 30
CONCURRENT_CHECKS = 1000
OUTPUT_FILE = 'live_proxy.txt'
