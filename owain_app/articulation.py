import openai
import os
import json
import click
from owain_app.catalog import Catalog
from dotenv import load_dotenv

load_dotenv()


def query_openai_api(prompt, model="text-davinci-003"):
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()


@click.command()
@click.option(
    "--prompt_dir",
    default="path_to_prompt_files",
    help="Directory containing prompt files",
)
@click.option(
    "--response_dir",
    default="path_to_save_responses",
    help="Directory to save response files",
)
def main(prompt_dir, response_dir):
    catalog = Catalog()

    for filename in os.listdir(os.path.join(catalog.base_path, prompt_dir)):
        prompt_path = os.path.join(catalog.base_path, prompt_dir, filename)
        prompt = catalog.load_prompt(prompt_path)
        response = query_openai_api(prompt)
        response_filename = f"response_{filename}"
        catalog.save_response_interaction(
            response, os.path.join(response_dir, response_filename)
        )


if __name__ == "__main__":
    main()
