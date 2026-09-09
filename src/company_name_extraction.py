# This file extracts company names from the pages

from itertools import batched
import json
import os
from pathlib import Path
from lift import extract_images
from lift.model import InferenceManager
from PIL import Image
import logging
from dataclasses import asdict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_PATH = BASE_DIR / "schema.json"
LOG_PATH = BASE_DIR / "logs" / f"{os.getenv("SLURM_JOB_ID")}.log"
logger = logging.getLogger(__name__)

def main():
    Path(LOG_PATH).touch()
    logging.basicConfig(filename=LOG_PATH)

    logger.info(f"Running compnay extraction on: {DATA_DIR}")
    logger.info(f"Using schema: {SCHEMA_PATH}")
    logger.info(f"Logging to: {LOG_PATH}")

    model = InferenceManager(method="hf")
    i = 0
    for batch in batched(os.scandir(DATA_DIR / "raw"), n=1):
        results = extract_images(images=[Image.open(p) for p in batch], schema=str(SCHEMA_PATH), model=model)
        with open(DATA_DIR / "extracted_data" / f"{batch[0].name}.json", "w") as f:
            f.writelines(json.dumps(asdict(results), indent=4))

        logger.info(f"Completed iteration {i}")
        i += 1


if __name__ == "__main__":
    main()
