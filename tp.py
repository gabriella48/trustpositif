import requests
import os
import threading
import time
import hashlib
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

BASE_RAW_URLS = [
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_blacklist.txt",
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_blacklist_complete.txt",
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_blacklist_complete_v2.txt",
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_blacklist_v2.txt",
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_gambling.txt",
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/alsyundawy_gambling_v2.txt",
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/gambling-onlydomains.txt"
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/gambling_indonesia_001.txt"
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/gambling_indonesia_002.txt"
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/gambling_indonesia_003.txt"
    "https://raw.githubusercontent.com/alsyundawy/TrustPositif/refs/heads/main/gambling_indonesia_domainonly.txt"
]

# Spinner
spinner_running = False
def spinner(message="Mengecek..."):
    spinner_chars = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    i = 0
    while spinner_running:
        print(f"\r{Fore.YELLOW}{spinner_chars[i % len(spinner_chars)]} {message}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(0.1)
        i += 1

# Hash penyimpanan isi terakhir tiap URL
previous_hashes = {}

def get_file_hash(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return hashlib.sha256(resp.content).hexdigest(), resp.text
        return None, ""
    except:
        return None, ""

def check_domain_in_file(domain, file_url):
    file_hash, content = get_file_hash(file_url)
    if file_hash is None:
        return False

    # Deteksi perubahan isi
    if file_url not in previous_hashes:
        previous_hashes[file_url] = file_hash
    elif previous_hashes[file_url] != file_hash:
        print(f"\n{Fore.MAGENTA}[🔄] File dari URL berikut telah diperbarui: {file_url}{Style.RESET_ALL}")
        previous_hashes[file_url] = file_hash

    return domain.lower() in content.lower()

def check_domain(domain):
    for url in BASE_RAW_URLS:
        if check_domain_in_file(domain, url):
            return True
    return False

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + "=" * 60)
    print(Fore.CYAN + "🔎 CEK DOMAIN DI TRUSTPOSITIF 🔒".center(60))
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

def monitor(domains, interval=600):  # 10 menit
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{Fore.BLUE}[🕒] Mulai pengecekan pada {now}\n")
        for domain in domains:
            global spinner_running
            spinner_running = True
            t = threading.Thread(target=spinner, args=(f"Mengecek {domain}...",))
            t.start()

            result = check_domain(domain)

            spinner_running = False
            t.join()
            print("\r", end="")

            if result:
                print(f"{Fore.RED}❌ {domain}: DIBLOKIR (ditemukan di daftar)")
            else:
                print(f"{Fore.GREEN}✅ {domain}: TIDAK DIBLOKIR")

        print(f"\n{Fore.YELLOW}[⏳] Menunggu {interval//60} menit sebelum pengecekan ulang...\n")
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}[🛑] Dihentikan oleh pengguna.")
            break

def main():
    print_banner()
    print(Fore.YELLOW + "Masukkan hingga 10 domain (tekan ENTER kosong untuk berhenti):\n")

    domains = []
    for i in range(10):
        d = input(f"  {Fore.CYAN}- Domain {i+1}: {Style.RESET_ALL}").strip()
        if not d:
            break
        domains.append(d.lower())

    if not domains:
        print(f"{Fore.RED}[!] Tidak ada domain dimasukkan.")
        return

    monitor(domains, interval=600)

if __name__ == "__main__":
    main()
