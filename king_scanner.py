import os
import socket
import requests
import time

# Limpa a tela
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

# Arte em ASCII
def arte_ascii():
    print("\033[92m")
    print("██╗  ██╗██╗███╗   ██╗ ██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ")
    print("██║ ██╔╝██║████╗  ██║██╔═══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗")
    print("█████╔╝ ██║██╔██╗ ██║██║   ██║    ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝")
    print("██╔═██╗ ██║██║╚██╗██║██║   ██║    ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗")
    print("██║  ██╗██║██║ ╚████║╚██████╔╝    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║")
    print("╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝")
    print("\033[0m")
    print("=" * 88)
    print("   Ferramenta educacional de varredura | by KinG\n" + "=" * 88 + "\n")

# Menu do painel
def menu():
    print("\033[92m")
    print(" [1] ESCANEAR PORTAS")
    print(" [2] VERIFICAR HEADERS HTTP")
    print(" [3] TESTAR VULNERABILIDADES (XSS / SQLi)")
    print(" [4] ESCANEAR TUDO")
    print(" [0] SAIR")
    print("\033[0m")

# Escaneia portas comuns
def escanear_portas(host):
    print(f"\n\033[93m[+] ESCANEANDO PORTAS EM: {host}\033[0m\n")
    portas = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]
    for porta in portas:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((host, porta))
            print(f"\033[92m[ABERTA] Porta {porta}\033[0m")
            s.close()
        except:
            pass
    print()

# Verifica headers HTTP
def verificar_headers(url):
    print(f"\n\033[93m[+] HEADERS DE: {url}\033[0m\n")
    try:
        r = requests.get(url, timeout=5)
        for k, v in r.headers.items():
            print(f"\033[96m{k}:\033[0m {v}")
    except:
        print("\033[91mErro ao acessar URL\033[0m")
    print()

# Testa XSS e SQLi simples
def verificar_falhas(url):
    print("\n\033[93m[+] TESTANDO XSS E SQLi:\033[0m\n")
    test_xss = "<script>alert(1)</script>"
    test_sql = "' OR '1'='1"
    testes = [
        f"{url}/?msg={test_xss}",
        f"{url}/login?user=admin&pass={test_sql}"
    ]

    for test in testes:
        try:
            r = requests.get(test, timeout=5)
            if test_xss in r.text:
                print(f"\033[91m[!] XSS DETECTADO:\033[0m {test}")
            elif "sql" in r.text.lower() or "error" in r.text.lower():
                print(f"\033[91m[!] SQL INJECTION DETECTADO:\033[0m {test}")
            else:
                print(f"\033[92m[OK]\033[0m {test}")
        except:
            print(f"\033[91m[ERRO]\033[0m {test}")
    print()

# Painel principal
def painel():
    limpar()
    arte_ascii()
    url = input(">> DIGITE A URL ALVO (ex: https://site.com): ").strip()
    host = url.replace("http://", "").replace("https://", "").split('/')[0]

    while True:
        limpar()
        arte_ascii()
        menu()
        opcao = input("\n>> ESCOLHA UMA OPÇÃO: ").strip()

        if opcao == "1":
            escanear_portas(host)
        elif opcao == "2":
            verificar_headers(url)
        elif opcao == "3":
            verificar_falhas(url)
        elif opcao == "4":
            escanear_portas(host)
            verificar_headers(url)
            verificar_falhas(url)
        elif opcao == "0":
            print("\n\033[91m[!] Encerrando o King Scanner...\033[0m")
            break
        else:
            print("\033[91mOpção inválida.\033[0m")

        input("\n\033[90m[Pressione ENTER para voltar ao painel...]\033[0m")

# Início do script
if __name__ == "__main__":
    painel()
