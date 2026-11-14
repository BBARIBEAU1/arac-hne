#!/usr/bin/env python3
import argparse
import concurrent.futures
import socket

from banner import print_banner

def resolve(hostname):
    """Return (hostname, ip) if it resolves, else None."""
    # we'll fill this in next
    try:
        ip = socket.gethostbyname(hostname)
        return (hostname, ip)
    except socket.gaierror:
        return None

def main():
    parser = argparse.ArgumentParser(description="Threaded DNS subdomain enumerator")
    parser.add_argument("domain", help="Base domain, e.g. example.com")
    parser.add_argument("-w", "--wordlist", required=True, help="Subdomain wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Worker threads (default 50)")
    parser.add_argument("-o", "--output", help="Write found hostnames to this file")
    parser.add_argument("--no-banner", action="store_true", help="Skip the startup banner")
    args = parser.parse_args()
    if not args.no_banner:
        print_banner("arac-hne", "subdomain enumerator")
    print(f"[*] Enumerating {args.domain} with {args.threads} threads")

    with open(args.wordlist) as f:
        words = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    hostnames = [f"{word}.{args.domain}" for word in words]
    print(f"[*] {len(hostnames)} names to check")

    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as pool:
        for result in pool.map(resolve, hostnames):
            if result:
                host, ip = result
                print(f"[+] {host} -> {ip}")
                found.append(result)
    if args.output and found:
        with open(args.output, "w") as out:
            for host, ip in found:
                out.write(f"{host},{ip}\n")
        print(f"[*] Wrote {len(found)} results to {args.output}")
    print(f"[*] Done. {len(found)} subdomain(s) found.")

if __name__ == "__main__":
    main()
