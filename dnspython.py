import requests as req
import sys

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

def dns_lookup(host :str):
    try:
        response = req.get(host, stream=True)
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
        file = open("dir.txt", "r")
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
                print(f'{bcolors.OKGREEN} [-] Subdomain is empty, skipping... {bcolors.ENDC}')
    except FileNotFoundError:
        print(f'{bcolors.FAIL}[-] File not found!{bcolors.ENDC}')


        
def menu():
    print("===================================================================")
    print("[1] - DNS Lookup")
    print("[2] - Website recon")
    print("[3] - Website dir bruteforce")
    print("[0] - Exit")
    print("===================================================================")
    choice = int(input("Choice an option: "))
    return choice

def handle_user_choice(choice :int, host :str):
    if choice == 1:
        dns_lookup(host)
    elif choice == 2:
        print("")
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
        choice = menu()
        host = sys.argv[1]
        handle_user_choice(choice, host)
main()