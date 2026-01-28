import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

def main():
    base_dir = Path(__file__).resolve().parent  # folder containing serve_map.py
    blocks_path = base_dir / "blocks.geojson"
    index_path = base_dir / "index.html"

    if not blocks_path.exists():
        raise FileNotFoundError(f"{blocks_path} not found.")
    if not index_path.exists():
        raise FileNotFoundError(f"{index_path} not found.")

    # Serve files FROM the script folder
    handler = lambda *args, **kwargs: CORSRequestHandler(*args, directory=str(base_dir), **kwargs)

    url = f"http://localhost:{PORT}/index.html"
    print(f"Serving at {url}")
    webbrowser.open(url)

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    main()
