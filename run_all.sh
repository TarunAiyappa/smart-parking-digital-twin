#!/bin/bash

echo "Starting Smart Parking Digital Twin System..."

# Define variables
DASHBOARD_IP=$(hostname -I | awk '{print $1}')
LOGDIR="./logs"
mkdir -p "$LOGDIR"

# Start FastAPI WebSocket Server
echo "Starting main2.py (FastAPI) on port 8002"
nohup python3 -m uvicorn main2:app --host 0.0.0.0 --port 8002 > $LOGDIR/main2.log 2>&1 &

# Start MQTT Publisher
echo "Starting mqtt_pub.py"
nohup python3 mqtt_pub_auth.py > $LOGDIR/mqtt_pub.log 2>&1 &

# Start Dashboard with correct IP
echo "Starting dashboard.py on http://$DASHBOARD_IP:8060"
nohup python3 dashboard.py --server "$DASHBOARD_IP" --port 8002 > $LOGDIR/dashboard.log 2>&1 &

echo "All components started!"
