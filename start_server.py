import http.server
import socketserver
import socket
import os
import sys

PORT = 8080
DIRECTORY = "site"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    # Change to the site directory
    if os.path.exists(DIRECTORY):
        os.chdir(DIRECTORY)
    else:
        print(f"Error: Directory '{DIRECTORY}' not found. Make sure you run this from the project root.")
        input("Press Enter to exit...")
        sys.exit(1)

    Handler = http.server.SimpleHTTPRequestHandler
    
    # Allow address reuse to prevent "Address already in use" errors on restart
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            ip = get_local_ip()
            print("="*60)
            print(f"Server started successfully!")
            print(f"Local Access:     http://localhost:{PORT}/")
            print(f"Network Access:   http://{ip}:{PORT}/  <-- Use this for QR Codes")
            print("="*60)
            print("Press Ctrl+C to stop the server.")
            print("\nNOTE: If you cannot access the site from your phone:")
            print("1. Make sure your phone is on the SAME WiFi network.")
            print("2. Check your Windows Firewall settings and allow Python.")
            print("="*60)
            httpd.serve_forever()
    except OSError as e:
        print(f"Error: Could not start server on port {PORT}. It might be in use.")
        print(f"Details: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped.")

def print_qr(url):
    try:
        import qrcode
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.make(fit=True)
        print("\nScan this QR code to test connection:")
        qr.print_ascii(invert=True)
        print(f"URL: {url}")
    except ImportError:
        print("\n(Install 'qrcode' library to see a QR code here)")

if __name__ == "__main__":
    # Quick hack to make sure we have the IP before starting
    ip = get_local_ip()
    url = f"http://{ip}:{PORT}/"
    print_qr(url)
    main()
