import socket
import subprocess
import platform
from colorama import Fore, Style, init
import threading
from queue import Queue

init()

port_queue = Queue()

def detect_own_ip_and_port():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip, port = s.getsockname()
            print(f"{Fore.YELLOW}🧭 IP locale : {Fore.GREEN}{ip}")
            print(f"{Fore.YELLOW}🔌 Port source local utilisé : {Fore.GREEN}{port}{Style.RESET_ALL}\n")
            return ip, port
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur IP/port : {e}{Style.RESET_ALL}")
        return None, None

def detect_local_ips(base_ip="192.168.1", start=1, end=254):
    print(f"{Fore.YELLOW}🔎 Scan du réseau local sur {base_ip}.0/24...{Style.RESET_ALL}")
    active_hosts = []
    threads = []

    def ping_host(ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", "-W", "1", ip]
        result = subprocess.run(command, stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            print(f"{Fore.GREEN}[+] Actif : {ip}{Style.RESET_ALL}")
            active_hosts.append(ip)

    for i in range(start, end + 1):
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=ping_host, args=(ip,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return active_hosts

def grab_banner(sock):
    try:
        sock.settimeout(2)
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return None

def worker(host):
    while not port_queue.empty():
        port = port_queue.get()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                if result == 0:
                    banner = grab_banner(sock)
                    if banner:
                        print(f"{Fore.GREEN}[+] Port {port} ouvert - {banner}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}[+] Port {port} ouvert - (pas de bannière){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.MAGENTA}⚠️ Erreur port {port} : {e}{Style.RESET_ALL}")
        finally:
            port_queue.task_done()

def scan_ports_threaded(host, start_port, end_port, thread_count=50):
    print(f"\n{Fore.CYAN}🚀 Scan de ports sur {host} ({start_port}-{end_port}) avec détection de services...{Style.RESET_ALL}")

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(host,))
        t.daemon = True
        t.start()
        threads.append(t)

    port_queue.join()

if __name__ == "__main__":
    detect_own_ip_and_port()

    base_ip = input(f"{Fore.BLUE}Entrez la base IP (ex: 192.168.1) : {Style.RESET_ALL}") or "192.168.1"
    hosts = detect_local_ips(base_ip)

    if not hosts:
        print(f"{Fore.RED}❌ Aucun hôte actif trouvé.{Style.RESET_ALL}")
        exit()

    print(f"\n{Fore.CYAN}Hôtes détectés :{Style.RESET_ALL}")
    for i, ip in enumerate(hosts):
        print(f"  [{i}] {ip}")

    try:
        idx = int(input(f"\n{Fore.BLUE}Choisissez l'index d’un hôte : {Style.RESET_ALL}"))
        target_ip = hosts[idx]
    except:
        print(f"{Fore.RED}❌ Sélection invalide{Style.RESET_ALL}")
        exit()

    start_port = input(f"{Fore.BLUE}Port de début (défaut 20) : {Style.RESET_ALL}") or "20"
    end_port = input(f"{Fore.BLUE}Port de fin (défaut 1024) : {Style.RESET_ALL}") or "1024"

    scan_ports_threaded(target_ip, int(start_port), int(end_port))


