# LUNA Smart Agent

## Overview

LUNA Smart Agent is an intelligent system designed to optimize the operation of LUNA 2000 battery storage systems. It uses real-time data about energy prices, photovoltaic production, and facility consumption to make smart decisions that maximize energy savings while ensuring battery health and longevity.

## Architecture

The agent is built on a modular architecture:

1. **Core Agent**: Built with the `openai-agents-python` framework, providing the decision-making capabilities.

2. **Modbus Interface**: Connects directly to the LUNA 2000 battery and Huawei SUN2000 inverter using the Modbus TCP protocol.

3. **Economic Optimization**: Uses real-time PUN (Italian electricity market price) to make economically optimal decisions.

4. **FastAPI Service**: Provides REST API endpoints for monitoring and manual control.

## Decision Logic

The agent follows a prioritized set of rules:

1. **Battery Health**: Maintains State of Charge (SoC) between 25% and 85%
2. **Economic Discharge**: When price > 0.25 €/kWh AND SoC > 40%, discharge up to 2 kW
3. **Economic Charge**: When price < 0.12 €/kWh OR surplus production > 0.5 kW, charge up to 2 kW
4. **Evening Reserve**: Maintains at least 20% SoC reserve after 18:00

## Integration Points

- **Modbus TCP**: Direct communication with battery and inverter hardware
- **Energy Market API**: Real-time electricity price data
- **REST API**: User control and monitoring

## Safety Features

The agent implements multiple safety checks:
- SoC limits (never below 25% or above 95%)
- Power limits (±2 kW maximum)
- Automatic standby mode when conditions are unsafe

## Development

This project was developed to serve as a reference implementation for intelligent energy management systems that can optimize storage operation based on real-time market prices and local energy conditions.

The code has been designed with readability and extensibility in mind, allowing for easy adaptation to different battery models or additional optimization strategies. 