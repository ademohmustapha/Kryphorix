import sys

class UI:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def supports_color():
    return sys.stdout.isatty()


def color(text, code):
    if supports_color():
        return f"{code}{text}{UI.END}"
    return text


def banner():
    print(color(UI.BOLD + UI.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", UI.CYAN))
    print(color("        Kryphorix Scanner     ", UI.CYAN))
    print(color("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", UI.CYAN))


def section(title):
    print(color(f"\n[ {title} ]", UI.BLUE))


def info(msg):
    print(color("[*] " + msg, UI.CYAN))


def good(msg):
    print(color("[+] " + msg, UI.GREEN))


def warn(msg):
    print(color("[!] " + msg, UI.YELLOW))


def bad(msg):
    print(color("[-] " + msg, UI.RED))

