# Gambler's Ruin Simulation

A Python project that simulates various gambling scenarios and calculates probabilities using different models of the Gambler's Ruin problem.

## Features

- Basic Gambler's Ruin simulation
- Generalized model with customizable parameters
- Credit line support
- Variable bet sizes
- Maximum bet limits
- Interactive web interface using Streamlit
- REST API using FastAPI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LeoVershel1/gamblers-ruin-simulation.git
cd gamblers-ruin-simulation
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface
To run the Streamlit web interface:
```bash
streamlit run frontend.py
```

### API Server
To run the FastAPI server:
```bash
uvicorn api:app --reload
```

## Project Structure

- `frontend.py`: Streamlit web interface
- `api.py`: FastAPI REST API
- `ruin.py`: Core simulation logic
- `requirements.txt`: Project dependencies

## API Documentation

Once the API server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 