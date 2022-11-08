import os
import sys
from io import BytesIO

import uvicorn
import numpy as np

from loguru import logger
from fastapi import FastAPI, Response, status, File, UploadFile

from src.base.model import CNNModel


# Set up logger
logger.remove()
logger.add(sys.stderr, level="WARNING")
logger.add(sys.stdout, filter=lambda record: record["level"].no < 40, level="INFO")

# Create the App
app = FastAPI(title="Meat Quality Assessment")

# Initialise global parameters to be filled at startup
global_items = {}

# Run at startup - load the model
@app.on_event("startup")
def startup() -> None:
    """Load and initialise the model.
    """
    path = "notebooks/output/model"
    logger.info(f"Loading model files from {path}.")
    global_items["model"] = CNNModel.load_model(path)
    logger.info("Model loaded successfully.")


@app.get('/health')
async def health_check() -> None:
    """Endpoint for health check.
    """
    if "model" in global_items and global_items["model"] is not None:
        return Response("healthy", status_code=status.HTTP_200_OK)
    else:
        return Response("not healthy", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


def read_image(image_payload) -> np.ndarray:
    """Read an encoded image into a Numpy array.

    Args:
        image_payload: The encoded image as it comes from
            the request payload

    Returns:
        np.ndarray: The decoded image
    """
    stream = BytesIO(image_payload)
    image = np.asarray(bytearray(stream.read), dtype=np.uint8)


@app.post("/predict")
async def prediction(image: UploadFile=File(...)) -> dict:
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        dict: _description_
    """
    try:
        pass
    except Exception as error:
        response = {"error": f"{error}"}
    finally:
        return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False, log_level="info")
