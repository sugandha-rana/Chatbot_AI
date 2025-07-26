# FastAPI Basic Setup

This is a basic FastAPI project setup.

## Installation

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running the app

Run the FastAPI app using Uvicorn:

```bash
uvicorn main:app --reload
```

The app will be available at http://127.0.0.1:8000
