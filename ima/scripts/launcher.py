import urllib.request
import json
import sys
import time
import subprocess
import os
import argparse

try:
    import websocket
except ImportError:
    print("Error: websocket-client module not found.")
    print("Please ensure 'websocket-client' is installed in the python environment.")
    sys.exit(1)

CDP_HOST = "127.0.0.1"
CDP_PORT = 8315

POSSIBLE_PATHS = [
    "/Applications/ima.copilot.app/Contents/MacOS/ima.copilot",
    os.path.expanduser("~/Applications/ima.copilot.app/Contents/MacOS/ima.copilot")
]
APP_PATH = None
for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        APP_PATH = p
        break

def is_port_open(host, port):
    """Check if CDP port is open"""
    try:
        url = f"http://{host}:{port}/json/version"
        with urllib.request.urlopen(url, timeout=1) as response:
            return response.status == 200
    except:
        return False

def launch_app():
    """Launch the ima app with debugging port enabled"""
    if not APP_PATH:
        print("Error: ima.copilot application not found.")
        sys.exit(1)
        
    # print(f"Launching ima from {APP_PATH}...")
    # Add --remote-allow-origins=* to fix 403 Forbidden issues on newer electron/chrome
    subprocess.Popen([APP_PATH, f"--remote-debugging-port={CDP_PORT}", "--remote-allow-origins=*"], 
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL)
    
    # Wait for port
    for _ in range(15):
        time.sleep(1)
        if is_port_open(CDP_HOST, CDP_PORT):
            return True
    return False

def create_new_tab():
    """Create a new tab via HTTP CDP endpoint"""
    url = f"http://{CDP_HOST}:{CDP_PORT}/json/new"
    try:
        req = urllib.request.Request(url, method='PUT')
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error creating tab: {e}")
        sys.exit(1)

def run_search(query):
    # 1. Ensure app is running
    if not is_port_open(CDP_HOST, CDP_PORT):
        print("Starting ima.copilot...")
        if not launch_app():
            print("Failed to launch ima.copilot or connect to CDP port.")
            sys.exit(1)
    
    # 2. Create tab
    tab_info = create_new_tab()
    ws_url = tab_info.get('webSocketDebuggerUrl')
    
    if not ws_url:
        print("Error: Could not get WebSocket URL.")
        sys.exit(1)

    # 3. Construct URL
    target_url = f"https://ima.qq.com/ai-search?query={urllib.parse.quote(query)}"
    
    # 4. Navigate via WebSocket
    try:
        ws = websocket.create_connection(ws_url)
        
        # Navigate
        nav_command = {
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": target_url}
        }
        ws.send(json.dumps(nav_command))
        ws.recv() # Wait for ack
        
        print(f"Successfully opened search for: {query}")
        ws.close()
        
    except Exception as e:
        print(f"WebSocket communication error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control ima.copilot via CDP")
    parser.add_argument("query", help="Search query string")
    args = parser.parse_args()
    
    run_search(args.query)
