#!/usr/bin/env python3
import socket
from pathlib import Path

SOCKET = Path.home() / ".local/state/lilced/lilced.sock"

def request(text):
    if not SOCKET.exists():
        return "CORE_OFFLINE"
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect(str(SOCKET))
            s.sendall((text.rstrip("\n") + "\n").encode())
            chunks = []
            while True:
                b = s.recv(65536)
                if not b:
                    break
                chunks.append(b)
            return b"".join(chunks).decode(errors="replace").rstrip()
    except Exception as e:
        return f"CORE_OFFLINE: {e}"

def main():
    print("Lil Ced v0.8 alpha | private terminal | /status /brain /memory /tools /receipts /mit /hash /read /write /freeze /resume /exit")
    while True:
        try:
            line = input("LILCED > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line == "/exit":
            break
        print(request(line))

if __name__ == "__main__":
    main()