import socket
import re
import concurrent.futures
import ssl
from datetime import datetime, timedelta

# ... سایر import ها و توابع مشابه کد اول ...

def test_connection(bridge_line):
    """
    تست اتصال برای انواع مختلف پل‌ها
    """
    if not bridge_line or len(bridge_line) < 8:
        return False
    
    try:
        # تشخیص نوع پل بر اساس محتوای آن
        bridge_lower = bridge_line.lower()
        
        # 1. WebTunnel (HTTPS)
        if "webtunnel" in bridge_lower or "https" in bridge_lower:
            return test_webtunnel_connection(bridge_line)
        
        # 2. OBFS4 یا Vanilla (اتصال TCP ساده)
        else:
            return test_tcp_connection(bridge_line)
            
    except Exception:
        return False

def test_webtunnel_connection(bridge_line):
    """
    تست اتصال WebTunnel با HTTPS
    """
    for attempt in range(MAX_RETRIES):
        try:
            # استخراج آدرس و پورت
            match = re.search(r'https://([^/:]+)(?::(\d+))?', bridge_line, re.IGNORECASE)
            if not match:
                # اگر فرمت استاندارد نیست، سعی کن آدرس را پیدا کنی
                match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3}):(\d+)', bridge_line)
                if not match:
                    match = re.search(r'\[([0-9a-fA-F:]+)\]:(\d+)', bridge_line)
                    if not match:
                        return False
            
            host = match.group(1)
            port = int(match.group(2)) if match.group(2) else 443
            
            # برای WebTunnel، یک اتصال TLS برقرار کن
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # ابتدا اتصال TCP
            sock = socket.create_connection((host, port), timeout=CONNECTION_TIMEOUT)
            
            # سپس ارتقا به TLS
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            ssl_sock.close()
            
            return True
            
        except (socket.timeout, socket.error, ssl.SSLError, Exception) as e:
            if attempt == MAX_RETRIES - 1:
                continue
            time.sleep(0.5)  # تأخیر کوتاه بین تلاش‌ها
    
    return False

def test_tcp_connection(bridge_line):
    """
    تست اتصال TCP برای OBFS4 و Vanilla
    """
    for attempt in range(MAX_RETRIES):
        try:
            ip, port = extract_ip_port(bridge_line)
            if not ip or not port:
                return False
            
            sock = socket.create_connection((ip, port), timeout=CONNECTION_TIMEOUT)
            sock.close()
            return True
            
        except (socket.timeout, socket.error, Exception):
            if attempt == MAX_RETRIES - 1:
                continue
            time.sleep(0.5)  # تأخیر کوتاه بین تلاش‌ها
    
    return False

def extract_ip_port(line):
    """
    استخراج IP و پورت از خط پل با قابلیت تشخیص انواع
    """
    # 1. IPv6 در براکت
    ipv6_match = re.search(r'\[(.*?)\]:(\d+)', line)
    if ipv6_match:
        return ipv6_match.group(1), int(ipv6_match.group(2))
    
    # 2. IPv4 استاندارد
    ipv4_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)', line)
    if ipv4_match:
        return ipv4_match.group(1), int(ipv4_match.group(2))
    
    # 3. آدرس دامنه (برای WebTunnel)
    domain_match = re.search(r'https?://([^/:]+)(?::(\d+))?', line, re.IGNORECASE)
    if domain_match:
        host = domain_match.group(1)
        port = int(domain_match.group(2)) if domain_match.group(2) else 443
        return host, port
    
    # 4. فرمت ساده (آدرس:پورت بدون پروتکل)
    simple_match = re.search(r'([^:\s]+):(\d+)', line)
    if simple_match:
        return simple_match.group(1), int(simple_match.group(2))
    
    return None, None

def check_connection(bridge_line):
    """
    تابع اصلی تست اتصال - با backward compatibility
    """
    return test_connection(bridge_line)

# در تابع main، جایگزین کردن بخش تست:
# از این:
"""
log(f"Testing connectivity for {filename} ({len(all_bridges)} bridges)...")
tested_bridges = []
if all_bridges:
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_bridge = {executor.submit(check_connection, bridge): bridge for bridge in all_bridges}
        for future in concurrent.futures.as_completed(future_to_bridge):
            bridge = future_to_bridge[future]
            try:
                if future.result():
                    tested_bridges.append(bridge)
            except Exception:
                pass
"""

# به این:
def test_all_bridges(bridge_list, transport_type):
    """
    تست تمام پل‌ها با استراتژی مناسب برای هر نوع
    """
    tested_bridges = []
    
    if not bridge_list:
        return tested_bridges
    
    log(f"Testing connectivity for {transport_type} ({len(bridge_list)} bridges)...")
    
    # انتخاب استراتژی تست بر اساس نوع انتقال
    if transport_type.lower() == "webtunnel":
        test_func = test_webtunnel_connection
    else:
        test_func = test_tcp_connection
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_bridge = {executor.submit(test_func, bridge): bridge for bridge in bridge_list}
        
        completed = 0
        for future in concurrent.futures.as_completed(future_to_bridge):
            completed += 1
            if completed % 50 == 0:
                log(f"   Progress: {completed}/{len(bridge_list)} bridges tested")
            
            bridge = future_to_bridge[future]
            try:
                if future.result():
                    tested_bridges.append(bridge)
            except Exception:
                pass
    
    log(f"   → {len(tested_bridges)} bridges passed connectivity test.")
    return tested_bridges

# و در حلقه اصلی:
"""
tested_bridges = test_all_bridges(list(all_bridges), target["type"])

if tested_bridges:
    with open(tested_filename, "w", encoding="utf-8") as f:
        for bridge in sorted(tested_bridges):
            f.write(bridge + "\n")
else:
    with open(tested_filename, "w", encoding="utf-8") as f:
        f.write("")
"""
