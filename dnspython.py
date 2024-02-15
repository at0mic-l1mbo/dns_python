import requests as req
import sys
import re
from fake_useragent import UserAgent

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show_logo():
    texto = '''
    ____           ____                      
   / __ \\__  __   / __ \\___  _________  ____ 
  / /_/ / / / /  / /_/ / _ \\/ ___/ __ \\/ __ \\
 / ____/ /_/ /  / _, _/  __/ /__/ /_/ / / / /
/_/    \\__, /  /_/ |_|\\___/\\___/\\____/_/ /_/ 
      /____/                                 
'''
    print(f'{bcolors.OKBLUE}{texto}{bcolors.ENDC}')

def web_recon(host :str):
    try:
        # You can use TOR proxies to make recon
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        ua = UserAgent(os="macos")
        headers = {
            'User-Agent': ua.random,
        }
        # add proxies=proxies to use TOR
        response = req.get(host, headers=headers)
        if response.status_code == 200:
            print(f'{bcolors.OKGREEN}[+] Response from {host}{bcolors.ENDC}')
            headers = str(response.headers)
            html = str(response._content)
            matches = re.findall(r'href="(http[s]?://[^"]+)"', html)
            file = open("host_links.txt", "w+")
            for link in matches:
                file.write(f'{link}\n')
            file.close()
            if 'Server' in headers:
                print(f'{bcolors.OKGREEN}[+] Server info has got!{bcolors.ENDC}')
            file = open("host_headers.txt", "w+")
            file.write(headers)
            file.close()
    except req.RequestException as e:
        print(f'{bcolors.FAIL}[-] An exception has ocurred: {e}{bcolors.ENDC}')

def dns_lookup(host :str):
    try:
        # You can use TOR to make recon
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        ua = UserAgent(os="macos")
        headers = {
            'User-Agent': ua.random,
        }
        # add proxies=proxies to use TOR
        response = req.get(host, stream=True, headers=headers)
        if response.status_code == 200:
            print(f'{bcolors.OKGREEN}[+] Host found!{bcolors.ENDC}')
            print(f'IP: {response.raw._connection.sock.getsockname()[0]}\nPort: {response.raw._connection.sock.getsockname()[1]}')
        else:
            print(f'{bcolors.FAIL}[-] Host not found!{bcolors.ENDC}')
    except req.RequestException as ex:
        print(f'{bcolors.FAIL}[-] An exception has ocurred: {ex}{bcolors.ENDC}') 

def discover_url_prefix(host :str):
    if 'http://' in host:
        res = host.split("http://")
        return ['http://', res[1]]
    elif 'https://' in host:
        res = host.split("https://")
        return ['https://', res[1]]
    else:
        print(f'{bcolors.FAIL}[-] An error has ocurred with your url!{bcolors.ENDC}')
        sys.exit(1)


def dir_bruteforce(host: str):
    try:
        file = open("wordlist_medium.txt", "r")
        answer = discover_url_prefix(host)
        print(f'{bcolors.OKGREEN}[+] Starting, could take a minute!{bcolors.ENDC}')
        for subdomain in file:
            subdomain = subdomain.strip() 
            if subdomain:  
                if answer[0].startswith('https://'):
                    full_host_brutedomain = f'{answer[0]}{subdomain}{answer[1]}'
                else:
                    full_host_brutedomain = f'{answer[0]}{subdomain}{answer[1]}'
                try:
                    res = req.get(full_host_brutedomain, timeout=30)
                    if res.status_code == 200:
                        print(f'{bcolors.OKGREEN}[+] Host found {full_host_brutedomain}{bcolors.ENDC}')
                except Exception as e:
                    pass
            else:
                print(f'{bcolors.FAIL} [-] Subdomain is empty, skipping... {bcolors.ENDC}')
    except FileNotFoundError:
        print(f'{bcolors.FAIL}[-] File not found!{bcolors.ENDC}')


        
def menu():
    print(f'{bcolors.OKCYAN}===================================================================')
    print("[1] - DNS Lookup")
    print("[2] - Website recon")
    print("[3] - Website dir bruteforce")
    print("[0] - Exit")
    print(f'==================================================================={bcolors.ENDC}')
    choice = int(input("Choice an option: "))
    return choice

def handle_user_choice(choice :int, host :str):
    if choice == 1:
        dns_lookup(host)
    elif choice == 2:
        web_recon(host)
    elif choice == 3:
        dir_bruteforce(host)
    else:
        print(f'{bcolors.OKGREEN}[+] Exiting.... Good Bye!{bcolors.ENDC}')
        sys.exit(0)


def main():
    if len(sys.argv) < 2:
        print(f'\n{bcolors.FAIL}[-] Invalid usage mode!{bcolors.ENDC}')
        print("Usage mode: python dnspython.py https://www.google.com")
    else:
        show_logo()
        while True:
            choice = menu()
            host = sys.argv[1]
            handle_user_choice(choice, host)
            user_wish = str(input("Do you want to continue? Y or n: "))
            if user_wish.lower() == 'n':
                print(f'{bcolors.OKGREEN}[+] Exiting.... Good Bye!{bcolors.ENDC}')
                break;
main()