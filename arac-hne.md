# arac-hne — Cheat Sheet

> Threaded DNS **subdomain** brute-forcer (`socket.gethostbyname` + `ThreadPoolExecutor`).
> Repo: <https://github.com/BBARIBEAU1/arac-hne> · Only domains you own or are authorized to test.

## Install / run
```bash
# source: ~/projects/subenum/arac-hne.py
chmod +x ~/projects/subenum/arac-hne.py
ln -sf ~/projects/subenum/arac-hne.py ~/.local/bin/arac-hne
arac-hne -h
```

## Syntax
```text
arac-hne <domain> -w WORDLIST [-t THREADS] [-o FILE]
```

| Flag | Long | Default | Meaning |
|---|---|---|---|
| `domain` | — | *(required)* | Base domain, e.g. `example.com` |
| `-w` | `--wordlist` | *(required)* | Subdomain words, one per line (`#` lines skipped) |
| `-t` | `--threads` | `50` | Worker threads |
| `-o` | `--output` | none | Write hits as CSV `host,ip` |
| `-h` | `--help` | — | Usage |

## Examples
```bash
arac-hne example.com -w ~/projects/subenum/words.txt                 # practice list
arac-hne example.com -w words.txt -t 20 -o hits.txt                  # save CSV
# offline lab: fake names via /etc/hosts (gethostbyname honors it)
echo "127.0.0.1 dev.lab.local api.lab.local" | sudo tee -a /etc/hosts
arac-hne lab.local -w words.txt
arac-hne example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 100
cut -d, -f1 hits.txt                                                  # just hostnames
```

## Output
```text
[*] Enumerating example.com with 50 threads
[*] 8 names to check
[+] www.example.com -> 93.184.x.x
[*] Wrote 1 results to hits.txt
[*] Done. 1 subdomain(s) found.
```

## Workflow
1. `arac-hne` → `hits.txt` (`host,ip`).
2. Feed IPs to **taran-tula**, web hosts to **ara-gog** (`http://<host>`).

## Gotchas
- **A records only, first IPv4 only.** No AAAA, CNAME chain, MX, TXT, or zone transfer.
- Uses the **system resolver** → `/etc/hosts`, local cache, and your DNS server's quirks all apply.
- **Wildcard DNS** (`*.domain`) makes every word "resolve". Sanity-check with a junk name first.
- `-o` writes only if something was found, and **overwrites** the file.
- Results print in wordlist order (`pool.map`), not finish order — so slow lookups hold the line.
- High `-t` on a big list can trip resolver rate limits → silent misses (failures look like "not found").
