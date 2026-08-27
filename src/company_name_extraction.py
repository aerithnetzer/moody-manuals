# This file extracts company names from the pages

from itertools import batched
import os
from pathlib import Path
from lift import extract_images
from lift.model import InferenceManager
from PIL import Image
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_PATH = BASE_DIR / "schema.json"
LOG_PATH = BASE_DIR / "logs" / f"{os.getenv("SLURM_JOB_ID")}.log"
logger = logging.getLogger(__name__)

def main():
    
    logging.basicConfig(filename=LOG_PATH)

    logger.info(f"Running compnay extraction on: {DATA_DIR}")
    logger.info(f"Using schema: {SCHEMA_PATH}")
    logger.info(f"Logging to: {LOG_PATH}")

    model = InferenceManager(method="hf")

    for batch in batched(os.scandir(DATA_DIR / "raw"), n=8):
        results = extract_images(images=[Image.open(p) for p in batch], schema=str(SCHEMA_PATH), model=model)
        print(results)
        


if __name__ == "__main__":
    main()
