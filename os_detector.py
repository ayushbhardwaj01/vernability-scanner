import subprocess
from scapy.all import IP, ICMP, sr1

def detect_os(target):
    try:
        print(f"[*] Running Nmap OS detection on {target}...")
        result = subprocess.run(
            ["sudo", "nmap", "-O", "-sV", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        output = result.stdout
        os_info = []

        for line in output.splitlines():
            if "OS details" in line or "Running:" in line:
                os_info.append(line.strip())
            elif "Aggressive OS guesses" in line:
                os_info.append(line.strip())
            elif line.strip().startswith("Service Info:"):
                os_info.append(line.strip())

        if os_info:
            return "\n".join(os_info)
        else:
            print("[!] Nmap gave no OS details. Trying fallback...")
            return ttl_os_guess(target)

    except subprocess.CalledProcessError as e:
        print(f"[!] Nmap failed: {e.stderr.strip()}")
        return ttl_os_guess(target)

def ttl_os_guess(target):
    try:
        pkt = IP(dst=target) / ICMP()
        resp = sr1(pkt, timeout=2, verbose=0)
        if resp:
            ttl = resp.ttl
            if ttl >= 128:
                return f"Guessed OS: Windows (TTL={ttl})"
            elif ttl >= 64:
                return f"Guessed OS: Linux/Unix (TTL={ttl})"
            else:
                return f"Guessed OS: Unknown (TTL={ttl})"
        else:
            return "No ICMP response received for TTL analysis."
    except Exception as e:
        return f"TTL fallback failed: {e}"
