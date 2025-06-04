# Smart Parking Digital Twin

A secure IoT-based Smart Parking Digital Twin system designed with real-time threat simulation, MQTT-based messaging, a FastAPI backend, and live sensor data visualization. This system was developed as part of a graduate thesis at Purdue University to study and address the security challenges faced in modern Digital Twin infrastructures.

---

## 🔍 Overview

This project emulates a smart parking environment in which ultrasonic sensors detect vehicle presence in parking spaces. Sensor data is transmitted using the MQTT protocol, processed via a FastAPI backend, and visualized on a real-time dashboard developed using Plotly Dash. The architecture accommodates both physical sensors and simulated input, with support for multiple adversarial attack scenarios to evaluate system resilience.

---

## ⚙️ Features

* Real-time parking occupancy detection using ultrasonic sensors
* Authenticated MQTT communication to ensure message integrity
* Interactive dashboard for live system monitoring and state tracking
* Integrated simulation of adversarial threats:

  * Denial of Service (DoS)
  * Sensor Spoofing
  * Unauthorized Publish/Subscribe
  * Passive Man-in-the-Middle (MitM)
* Modular deployment on local (Raspberry Pi) and cloud-hosted environments (AWS EC2)
* CSV-based logging and performance benchmarking for security evaluation

---

## 📁 Repository Structure

| File               | Description                                                                        |
| ------------------ | ---------------------------------------------------------------------------------- |
| `mqtt_pub_auth.py` | Publishes sensor data (real or simulated) to MQTT broker with authentication       |
| `main2.py`         | FastAPI backend responsible for processing and validating incoming MQTT messages   |
| `dashboard.py`     | Plotly Dash dashboard to visualize parking status, system logs, and health metrics |
| `sensor_utils.py`  | Provides hardware abstraction for ultrasonic sensor data collection or simulation  |
| `run_all.sh`       | Orchestrates the simultaneous execution of all system components                   |
| `stop_all.sh`      | Gracefully terminates the services started by `run_all.sh`                         |
| `LICENSE`          | MIT License for open-source distribution                                           |
| `README.md`        | This documentation file                                                            |

---

## 🚀 Running the Project

### Requirements

* Python 3.8 or higher
* Local Mosquitto MQTT broker (port 1883)
* Install dependencies:

  ```
  pip install fastapi dash paho-mqtt uvicorn plotly pandas
  ```

### Execution Instructions

```bash
bash run_all.sh
```

To stop all components:

```bash
bash stop_all.sh
```

---

## 🧪 Threat Simulation

The system supports simulation of adversarial behaviors through auxiliary scripts or manual terminal input. All anomalies are logged to:

* `spoof_log.csv` – Records detection of spoofed sensor data
* `sensor_log.csv` – Comprehensive sensor data history
* `message_rate.csv` – Message frequency tracking for anomaly detection

Supported attack scenarios include:

* `mqtt_dos.py` – MQTT message flooding for DoS simulation
* `mqtt_spoof.py` – Injection of manipulated sensor values
* `unauthorized_pub.py` – Attempts to publish data to protected topics
* `unauthorized_sub.py` – Subscription to restricted MQTT topics
* `mqtt_ghost_client.py` – Emulates client ID spoofing (ghost client injection)
* `tcpdump_sniffer.sh` – Passive sniffing of unencrypted MQTT traffic (MitM)

For deployments on cloud platforms, refer to:

* `cloud-ec2/` – AWS EC2-based deployment with replicated configuration
* `aws-iot-core/` – Implementation adapted for AWS IoT Core and Shadow Services

---

## 📄 Academic Note

This system was developed in partial fulfillment of the requirements for the Master of Science in Computer and Information Technology at Purdue University (2025). The research investigates Digital Twin security in IoT contexts, with particular focus on MQTT vulnerabilities, edge-cloud resilience, and DevSecOps-informed mitigation strategies.

Thesis Title: **"Security Evaluation of IoT-Based Digital Twin Systems: A Case Study on Smart Parking Infrastructure"**

Full citation:

> Aiyappa, Tarun (2025). *Security Analysis of Digital Twins for IoT: A Smart Parking Use Case with Attack Simulation and Cloud Comparison*. Purdue University Graduate School. Thesis. [https://doi.org/10.25394/PGS.28900883.v1](https://doi.org/10.25394/PGS.28900883.v1)

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for detailed terms.

