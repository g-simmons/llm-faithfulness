import openai
import json
import os
from sklearn.model_selection import KFold
from dotenv import load_dotenv
from owain_app.catalog import Catalog

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

def k_fold_cross_validation(catalog, dataset, k=5):
    kf = KFold(n_splits=k)
    for fold, (train_index, test_index) in enumerate(kf.split(dataset)):
        labeled_data = [json.dumps(dataset[i]) for i in train_index]
        unlabeled_data = [json.dumps(dataset[i]) for i in test_index]

        prompt = generate_prompt(labeled_data, unlabeled_data)
        response = query_openai_api(prompt)

        # Use catalog to save the response
        response_filename = f"fold_{fold}_response.txt"
        catalog.save_response(response, response_filename)

def main():
    dataset_filename = 'path_to_dataset.json'

    # Initialize Catalog
    catalog = Catalog()  # Assuming Catalog is set up with the correct base_path

    # Load dataset using Catalog
    dataset = catalog.load_dataset(dataset_filename)

    # Perform k-fold cross-validation
    k_fold_cross_validation(catalog, dataset, k=5)

if __name__ == '__main__':
    main()
