# LUNA Smart Controller

Intelligent system for controlling the LUNA 2000 battery with economic optimization.

## Features

- **Real-time monitoring** of energy prices, photovoltaic production, and consumption
- **Intelligent decisions** to maximize energy savings
- **Manual control** via API
- **Safety limits** to protect the battery

## Installation

1. Create the virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Startup

To start the server:
```bash
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

## Testing with simulator

To test without a physical battery:
```bash
docker run -d -p 502:502 --name fake-luna mbosvd/modbus-server \
  -a 47040:uint16:60 -a 47006:uint16:0 -a 47011:int16:0
```

Modify the IP address in `main.py` to `127.0.0.1`.

## Usage

### API

- **POST /chat** - Send commands to the agent
  ```json
  { "message": "Carica la batteria a 1kW" }
  ```

- **GET /status** - Get the current system status

### Useful commands

- "Qual è lo stato attuale?"
- "Carica la batteria a 0.5 kW"
- "Scarica la batteria a 1 kW"
- "Metti la batteria in standby" 