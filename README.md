# arac-hne

Threaded DNS subdomain enumerator. Brute-forces subdomains from a wordlist with `socket.gethostbyname`.

## Usage

```bash
arac-hne <domain> -w words.txt
arac-hne example.com -w words.txt -t 50 -o hits.txt
```

## What I learned

- DNS A-record lookups with socket.gethostbyname / socket.gaierror
- Building hostnames from a wordlist (sub.domain)
- Threading I/O-bound DNS with ThreadPoolExecutor
- Writing found results to a CSV file (-o)

## Legal

Only use on domains you own or have explicit permission to test.
