# quick-share

Quick Share is a lightweight, Flask-based tool for fast text and file sharing over a local network. It provides a simple browser interface for posting shared text and uploading files between devices on the same LAN.

---

## Features
- Shared text box
- File uploads with automatic download links  
- Accessible from any device on your local network  
- Extremely lightweight — only requires **Flask**  
- Simple UI, no setup, no accounts, no external services

Note: this tool is meant to be as efficient as possible, not as secure as possible. Do not upload sensitive data to quick share.

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/quick-share.git
cd quick-share
```

2. **Install Flask:**
```bash
pip install Flask
```

3. **Run the Server:**
```bash
python app.py
```

4. **Connect to the Server:**
```bash
http://<server-ip>:<port>
```
The port is 5000 by default, but can be changed in the app.py file
