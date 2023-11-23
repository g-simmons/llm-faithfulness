import openai
import os
import json
import click


def load_prompt(filename):
    with open(filename, 'r') as file:
        return file.read()

def query_openai_api(prompt, model="text-davinci-003", api_key="YOUR_API_KEY"):
    openai.api_key = api_key
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()

def save_response(response, filename):
    with open(filename, 'w') as file:
        file.write(response)

@click.command()
@click.option('--prompt_dir', default='path_to_prompt_files', help='Directory containing prompt files')
@click.option('--response_dir', default='path_to_save_responses', help='Directory to save response files')
def main(prompt_dir, response_dir):
    os.makedirs(response_dir, exist_ok=True)

    for filename in os.listdir(prompt_dir):
        prompt_path = os.path.join(prompt_dir, filename)
        prompt = load_prompt(prompt_path)
        response = query_openai_api(prompt)
        response_filename = f"response_{filename}"
        save_response(response, os.path.join(response_dir, response_filename))

if __name__ == '__main__':
    main()


