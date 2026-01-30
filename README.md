# Tor Bridges Collector & Archive

This repository automatically collects, validates, and archives Tor bridges. A GitHub Action runs every 3 hours to fetch new bridges from the official Tor Project.

It maintains two types of lists:
1.  **Full Archive:** An accumulative list of all bridges ever found.
2.  **Fresh List:** A specific list containing only bridges discovered in the last 24 hours.

## 🔥 Fresh Bridges (Last 24h)

This file contains **all protocols** (obfs4, webtunnel, vanilla) found within the last day. Use this if you need the most active candidates.

*   [**recent_bridges_24h.txt**](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/recent_bridges_24h.txt)

## 🔥 Full Archive (Categorized)

These files contain the history of all collected bridges. New entries are appended, and duplicates are removed.

| Transport Type | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **obfs4** | [obfs4.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/obfs4.txt) | [obfs4_ipv6.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/obfs4_ipv6.txt) |
| **WebTunnel** | [webtunnel.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/webtunnel.txt) | [webtunnel_ipv6.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/webtunnel_ipv6.txt) |
| **Vanilla** | [vanilla.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/vanilla.txt) | [vanilla_ipv6.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges-Collector/refs/heads/main/vanilla_ipv6.txt) |

## 🔥 Automation Logic

-   **Schedule:** Runs every 3 hours via GitHub Actions.
-   **Source:** `bridges.torproject.org`
-   **Tracking:** A `bridge_history.json` file tracks the timestamp of when each bridge was first seen to generate the 24h list accurately.

## 🔥 Disclaimer

This project is for educational and archival purposes. I am not affiliated with the Tor Project. Please use these bridges responsibly to bypass censorship.
