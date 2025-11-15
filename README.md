<div align="center">

# 🔵 Proxy Tool

### *Advanced Proxy Checker & Scraper*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python)](https://www.python.org)
[![Async](https://img.shields.io/badge/Async-aiohttp-cyan.svg?style=flat)](https://docs.aiohttp.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)
[![Rich](https://img.shields.io/badge/UI-Rich-magenta.svg?style=flat)](https://rich.readthedocs.io)

Modern proxy collection and validation tool with beautiful CLI interface



---

</div>

## ✨ Features

<table>
<tr>
<td>

- 🎨 **Beautiful Interface**
- ⚡ **Async Checking**
- 🔄 **4 Protocols** - SOCKS5, SOCKS4, HTTP, HTTPS
- 📊 **Live Statistics**

</td>
<td>

- 🗂️ **Organized Output**
- 🎯 **Auto Detection**
- 🔧 **Configurable**
- 💾 **Auto Save**

</td>
</tr>
</table>

---

## 🚀 Installation

### Prerequisites

```bash
Python 3.8+
```

### Quick Setup

```bash
# Clone repository
git clone https://github.com/kranoley/Proxy-Scraper-Parser-And-Checker
cd proxy-tool

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```




---

## ⚙️ Configuration

### `config.py` Settings

```python
# Performance
TIMEOUT = 5                 # Proxy check timeout (seconds)
FETCH_TIMEOUT = 30          # Source fetch timeout (seconds)
CONCURRENT_CHECKS = 1000    # Parallel check limit

# Sources per protocol
PROXY_SOURCES = {
    'socks5': [...],
    'socks4': [...],
    'http': [...],
    'https': [...]
}
```

### Adding Custom Sources

```python
PROXY_SOURCES = {
    'socks5': [
        'https://domain.com/proxies.txt',
    ]
}
```

---



## 🎨 UI Preview

<div align="center">




</div>
