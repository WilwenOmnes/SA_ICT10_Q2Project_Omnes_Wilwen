from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

clubs = {
    "robotics": {"Name": "Robotics Club", "Description": "We build robots.", "Meeting Time": "No day :<", "Location": "Room 211", "Club Moderator": "Ms. Nazuna", "Number of Members": 0},
    "science": {"Name": "Science Club", "Description": "Exploring science experiments.", "Meeting Time": "Fridays at 4 PM", "Location": "Science Lab", "Club Moderator": "Mr. Lucena", "Number of Members": 6},
    "art": {"Name": "Music / Arts Club", "Description": "Drawing, painting, and showcasing art.", "Meeting Time": "Wednesdays", "Location": "Music Room", "Club Moderator": "Ms. Llanes", "Number of Members": 7},
    "sports": {"Name": "Sports Club", "Description": "Team sports and athletics.", "Meeting Time": "Thursdays", "Location": "Quadrangle", "Club Moderator": "Mr. Mariano", "Number of Members": 10}
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/get_club":
            club_name = query.get("name", [""])[0]
            club = clubs.get(club_name)
            if club:
                content = f"""
                <h2>{club['Name']}</h2>
                <p><strong>Description:</strong> {club['Description']}</p>
                <p><strong>Meeting Time:</strong> {club['Meeting Time']}</p>
                <p><strong>Location:</strong> {club['Location']}</p>
                <p><strong>Club Moderator:</strong> {club['Club Moderator']}</p>
                <p><strong>Number of Members:</strong> {club['Number of Members']}</p>
                """
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Club not found.")
        else:
            file_path = path.lstrip("/")
            if file_path == "":
                file_path = "index.html"
            full_path = os.path.join(BASE_DIR, file_path)
            if os.path.isfile(full_path):
                self.send_response(200)
                if full_path.endswith(".html"):
                    self.send_header("Content-type", "text/html")
                elif full_path.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                else:
                    self.send_header("Content-type", "text/plain")
                self.end_headers()
                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found.")

port = 8000
print(f"Server running at http://localhost:{port}")
httpd = HTTPServer(("localhost", port), Handler)
httpd.serve_forever()