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


---

### 🛠️ Quick Setup

```bash
# Clone or Download the Repository

git clone https://github.com/kranoley/Proxy-Scraper-Parser-And-Checker.git

cd Proxy-Scraper-Parser-And-Checker

pip install -r requirements.txt

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
<img width="1105" height="383" alt="mg1" src="https://github.com/user-attachments/assets/0ef8077f-263a-4f45-90fc-3051fc40cf96" />
<img width="1136" height="239" alt="mg2" src="https://github.com/user-attachments/assets/ef7c327b-6c4a-4f71-b607-636105220dd0" />
<img width="1308" height="138" alt="mg3" src="https://github.com/user-attachments/assets/a55d8a2f-ec73-4960-8774-4e05f340ba4d" />








</div>
