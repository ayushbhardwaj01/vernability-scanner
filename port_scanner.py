import socket
import threading
from queue import Queue

MAX_THREADS = 200
lock = threading.Lock()

def scan_port(target, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            if s.connect_ex((target, port)) == 0:
                with lock:
                    open_ports.append(port)
    except:
        pass

def worker(target, queue, open_ports):
    while not queue.empty():
        port = queue.get()
        scan_port(target, port, open_ports)
        queue.task_done()

def scan_ports(target, start_port=0, end_port=1024):
    open_ports = []
    queue = Queue()
    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(MAX_THREADS):
        t = threading.Thread(target=worker, args=(target, queue, open_ports))
        t.daemon = True
        t.start()

    queue.join()
    return sorted(open_ports)
