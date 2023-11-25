import json
from owain_app.catalog import Catalog
from pathlib import Path
import json
from dataclasses import asdict
from tqdm import tqdm
from loguru import logger

MODEL_NAME = "gpt-4"


def main():
    catalog = Catalog()
    datapath = Path(catalog.data_path / "prompts/")
    # for file in datapath.glob("**/*.jsonl"):
    files = list(datapath.glob("**/*.jsonl"))

    for file in tqdm(files):
        logger.info(f"Processing {file}")
        with open(file, "r") as f:
            prompts = [json.loads(line) for line in f.readlines()]

            prompt_path = Path(
                catalog.data_path
                / ("prompts_for_requests/" + file.relative_to(datapath).as_posix())
            )
            if not prompt_path.parent.exists():
                prompt_path.parent.mkdir(parents=True)

            if prompt_path.exists():
                prompt_path.unlink()

            for prompt in tqdm(prompts):
                output = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "user", "content": prompt["prompt"]},
                    ],
                    "metadata": prompt,
                }
                with open(prompt_path, "a") as f:
                    f.write(json.dumps(output) + "\n")


if __name__ == "__main__":
    main()
