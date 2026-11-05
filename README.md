# Cold Chain — ESP8266 DHT11 & Django REST API

IoT telemetry project for temperature and humidity monitoring using an **ESP8266 (NodeMCU)** with a **DHT11** sensor and a **Django REST Framework** backend.

## Architecture

`ESP8266 + DHT11` → `Wi-Fi (HTTP POST JSON)` → `Django REST API` → `SQLite` → `HTTP GET /list/`

## 1. Backend Setup (Django REST API)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### API Endpoints
- **`GET /list/`**: Retrieve all recorded temperature & humidity measurements.
- **`POST /post/`**: Record a new measurement (`{"temperature": 24.5, "humidity": 54.0}`).
- **`/admin/`**: Django administration interface.

## 2. Firmware Setup (ESP8266 NodeMCU)

1. Copy [`esp8266_dht11/secrets.example.h`](esp8266_dht11/secrets.example.h) to `esp8266_dht11/secrets.h`:
   ```bash
   cp esp8266_dht11/secrets.example.h esp8266_dht11/secrets.h
   ```
2. Edit `esp8266_dht11/secrets.h` with your Wi-Fi SSID, password, and server endpoint.
3. Open [`esp8266_dht11/esp8266_dht11.ino`](esp8266_dht11/esp8266_dht11.ino) in Arduino IDE, select **NodeMCU 1.0 (ESP-12E Module)**, and upload.
