import openai
import json
import os
from sklearn.model_selection import KFold
from dotenv import load_dotenv

def load_dataset(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def generate_prompt(labeled_data, unlabeled_data):
    prompt = "Label the unlabeled examples based on the rule demonstrated in the labeled examples:\n\n"
    prompt += "LABELED EXAMPLES\n```\n" + "\n".join(labeled_data) + "\n```\n\n"
    prompt += "UNLABELED EXAMPLES\n```\n" + "\n".join(unlabeled_data) + "\n```"
    return prompt

def query_openai_api(prompt, model="text-davinci-003"):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    openai.api_key = api_key
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()

def save_response(response, filename):
    with open(filename, 'w') as file:
        file.write(response)

def k_fold_cross_validation(dataset, k=5):
    kf = KFold(n_splits=k)
    for fold, (train_index, test_index) in enumerate(kf.split(dataset)):
        labeled_data = [json.dumps(dataset[i]) for i in train_index]
        unlabeled_data = [json.dumps(dataset[i]) for i in test_index]
        prompt = generate_prompt(labeled_data, unlabeled_data)
        response = query_openai_api(prompt)
        response_filename = f"fold_{fold}_response.txt"
        save_response(response, response_filename)

def main():
    dataset_filename = 'path_to_dataset.json'
    dataset = load_dataset(dataset_filename)
    k_fold_cross_validation(dataset)

if __name__ == '__main__':
    main()
