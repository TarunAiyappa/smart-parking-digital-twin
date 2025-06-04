import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import threading
import time
import websocket
import datetime
import argparse

# --- Parse CLI arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("--server", type=str, default="localhost", help="WebSocket server IP or hostname")
parser.add_argument("--port", type=int, default=8002, help="WebSocket server port")
args = parser.parse_args()
ws_url = f"ws://{args.server}:{args.port}/ws"
print(f"Connecting to WebSocket at {ws_url}")

# Global sensor data
sensor_statuses = {str(i): "No Data" for i in range(1, 5)}
sensor_logs = []

# WebSocket Listener
def ws_listener():
    global sensor_statuses, sensor_logs
    while True:
        try:
            ws = websocket.WebSocket()
            ws.connect(ws_url)
            while True:
                message = ws.recv()
                parts = message.split(",")
                if len(parts) == 2:
                    sensor_id = parts[0].strip()
                    status = parts[1].strip()
                    sensor_statuses[sensor_id] = status
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_entry = f"[{timestamp}] Sensor {sensor_id}: {status}"
                    sensor_logs.append(log_entry)
                    if len(sensor_logs) > 100:
                        sensor_logs.pop(0)
        except Exception as e:
            print(f"WebSocket error: {e}")
            time.sleep(2)

# Background WebSocket Thread
threading.Thread(target=ws_listener, daemon=True).start()

# Dash App
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Smart Parking Digital Twin Dashboard"),

    html.Div(id="grid-container", style={
        "display": "grid",
        "gridTemplateColumns": "repeat(2, 1fr)",
        "gridGap": "10px",
        "margin": "20px"
    }),

    html.H2("Sensor Logs (Last 100 entries)"),
    html.Div(id="log-container", style={
        "border": "1px solid gray",
        "padding": "10px",
        "height": "300px",
        "overflowY": "scroll",
        "backgroundColor": "#f0f0f0"
    }),

    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
])

def generate_grid():
    cells = []
    for i in range(1, 5):
        status = sensor_statuses.get(str(i), "No Data")
        if status.lower() == "available":
            bg_color = "green"
        elif status.lower() == "occupied":
            bg_color = "red"
        else:
            bg_color = "lightgray"

        cell = html.Div(
            f"Sensor {i}: {status}",
            style={
                "border": "1px solid black",
                "padding": "20px",
                "textAlign": "center",
                "backgroundColor": bg_color,
                "fontSize": "20px",
                "color": "white"
            }
        )
        cells.append(cell)
    return cells

@app.callback(
    [Output("grid-container", "children"),
     Output("log-container", "children")],
    Input("interval-component", "n_intervals")
)
def update_dashboard(n):
    grid = generate_grid()
    log_content = [html.Div(log) for log in reversed(sensor_logs)]
    return grid, log_content

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8060)
