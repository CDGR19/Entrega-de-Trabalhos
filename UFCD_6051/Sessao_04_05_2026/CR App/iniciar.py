"""
iniciar.py - Lança os 3 servidores da demo em simultâneo
Uso: python iniciar.py

Abre automaticamente o browser no CR App.
Para parar: Ctrl+C
"""
import subprocess, sys, time, webbrowser, os, threading

BASE = os.path.dirname(os.path.abspath(__file__))

def run_server(folder, port, name):
    path = os.path.join(BASE, folder)
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=path,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print(f"  {name} iniciado na porta {port} (PID {proc.pid})")
    return proc

def serve_cr_app():
    import http.server, socketserver
    os.chdir(os.path.join(BASE, "cr-app"))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None  # Silence logs
    with socketserver.TCPServer(("", 5000), handler) as httpd:
        httpd.serve_forever()

print("\n" + "="*50)
print("  CR App Demo")
print("="*50)
print("\nA iniciar servidores...")

# Start CR App static server in thread
t = threading.Thread(target=serve_cr_app, daemon=True)
t.start()
print("  CR App iniciado na porta 5000")

# Start Flask apps
procs = [
    run_server("mundotextil", 5001, "MundoTextil"),
    run_server("bp", 5002, "BP"),
]

print("\nAguarda 2 segundos para inicializar...")
time.sleep(2)

webbrowser.open("http://localhost:5000")

print("\n" + "="*50)
print("  Acesso:")
print("  CR App     -> http://localhost:5000")
print("  MundoTextil -> http://localhost:5001")
print("  BP         -> http://localhost:5002")
print("="*50)
print("\nPara parar: Ctrl+C\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nA encerrar...")
    for p in procs:
        p.terminate()
