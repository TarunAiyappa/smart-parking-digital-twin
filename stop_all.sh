#!/bin/bash
pkill -f uvicorn
pkill -f mqtt_pub.py
pkill -f dashboard.py
echo "All Smart Parking processes stopped"
