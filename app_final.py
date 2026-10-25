import logging
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Calculator")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
PRECISION = int(os.getenv("PRECISION", "4"))

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("calculator")
logger.info("service_configured name=%s version=%s (precision=%d)", APP_NAME, APP_VERSION, PRECISION)

app = FastAPI(title=APP_NAME, version=APP_VERSION)

OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b,
    "power": lambda a, b: a**b,
    "root": lambda a, b: a**(1/b),
}


@app.get("/")
def root():
    logger.info(f"Root listing")
    return {"service": APP_NAME, "operations": list(OPERATIONS)}


@app.get("/health")
def health():
    logger.info(f"Health check")
    return {"status": "ok"}


@app.get("/version")
def version():
    logger.info(f"Version check")
    return {"name": APP_NAME, "version": APP_VERSION}


@app.get("/{operation}")
def calculate(operation: str, a: float, b: float):
    if operation not in OPERATIONS:
        logger.warning(f"Unknown operation {operation}")
        raise HTTPException(status_code=404, detail=f"Неизвестная операция '{operation}'")
    if operation == "divide" and b == 0:
        logger.warning("Division by zero")
        raise HTTPException(status_code=400, detail="Деление на ноль")
    if operation == "root" and b == 0:
        logger.warning("Zeroth root")
        raise HTTPException(status_code=400, detail="Нулевой корень")

    result = round(OPERATIONS[operation](a, b), PRECISION)
    logger.info(f"Calculated: {operation}({a}, {b}) = {result}")
    return {"operation": operation, "a": a, "b": b, "result": result}
