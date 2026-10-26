import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from collections import deque, Counter

from fastapi import FastAPI, HTTPException

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Calculator")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
PRECISION = int(os.getenv("PRECISION", "4"))
HISTORY_SIZE = int(os.getenv("HISTORY_SIZE", "10"))

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("calculator")
logger.info("service_configured name=%s version=%s (precision=%d, history_size=%d)", APP_NAME, APP_VERSION, PRECISION, HISTORY_SIZE)

app = FastAPI(title=APP_NAME, version=APP_VERSION)

OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b,
    "power": lambda a, b: a**b,
    "root": lambda a, b: a**(1/b),
}

history = deque(maxlen=HISTORY_SIZE)

stats = {
    "operations": Counter(),
    "errors": Counter(),
    "session_start": datetime.now().isoformat(timespec="seconds"),
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


@app.get("/history")
def get_history():
    logger.info(f"History check")
    items = list(reversed(history))
    return {"count": len(items), "max_size": HISTORY_SIZE, "items": items}


@app.get("/stats")
def get_stats():
    operations = stats["by_operation"]
    errors = stats["errors"]
    most_used = operations.most_common(1)
    return {
        "started_at": stats["session_start"],
        "total": sum(operations.values()),
        "by_operation": dict(sorted(operations.items())),
        "most_used": most_used[0][0] if most_used else None,
        "errors": sum(errors.values()),
        "errors_by_type": dict(sorted(errors.items())),
    }


@app.get("/{operation}")
def calculate(operation: str, a: float, b: float):
    if operation not in OPERATIONS:
        logger.warning(f"Unknown operation {operation}")
        stats["errors"]["unknown_operation"] += 1
        raise HTTPException(status_code=404, detail=f"Неизвестная операция '{operation}'")
    if operation == "divide" and b == 0:
        logger.warning("Division by zero")
        stats["errors"]["division_by_zero"] += 1
        raise HTTPException(status_code=400, detail="Деление на ноль")
    if operation == "root" and b == 0:
        logger.warning("Zeroth root")
        stats["errors"]["zeroth_root"] += 1
        raise HTTPException(status_code=400, detail="Нулевой корень")

    result = round(OPERATIONS[operation](a, b), PRECISION)
    history.append({"operation": operation, "a": a, "b": b, "result": result, "time": datetime.now().isoformat(timespec="seconds")})
    stats["operations"][operation] += 1
    logger.info(f"Calculated: {operation}({a}, {b}) = {result}")
    return {"operation": operation, "a": a, "b": b, "result": result}
