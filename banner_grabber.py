import socket

def grab_banners(target, ports):
    banners = {}
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target, port))
                banner = s.recv(1024).decode(errors='ignore').strip()
                banners[port] = banner if banner else "No banner"
        except:
            banners[port] = "Unknown"
    return banners
    print(grab_banners)