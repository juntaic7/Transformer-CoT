import argparse
from datetime import datetime
import os
from utils import read_jsonl
from agents.gpt_batch_agents import create_requests, send_requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(    
        "-d", "--dataset",
        type=str,
        required=True,
        help="The path to load the dataset."
    )
    parser.add_argument(    
        "-p", "--prompt_style",
        choices = ["base", "cot"],
        required=True,
        help="Select prompt style."
    )
    parser.add_argument(
        "-m", "--model",
        default="gpt-4o",
        help="Specify the version of the foundation model."
    )
    
    args = parser.parse_args()
    dataset = read_jsonl(args.dataset)
    docs = {}
            
    match args.prompt_style:
        case "base":
            with open(f"duplicate_string/prompts/ds.txt", 'r') as file:
                prompt = file.read().strip()
        case "cot":
            with open(f"duplicate_string/prompts/ds.cot.txt", 'r') as file:
                prompt = file.read().strip()
    for line in dataset:
        docs[str(line["id"])] = prompt.replace("{{string}}", line["string"])
        

    create_requests(docs=docs, prompt="{doc}", model=args.model)
    batch_id = send_requests()
    
    print(f"Requests sent to evaluate ability of GPT in duplicate string.\nPlease download the batch_output file from the OpenAI API dashboard, or retrieve the result using the batch id {batch_id}.\nBatch request details will be saved to batch_history.txt for future reference.")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('batch_history.txt', 'a') as file:
        file.write(f"{current_time} - {os.path.splitext(os.path.basename(args.dataset))[0]} - {args.model} - {args.prompt_style} - {batch_id}\n")
if __name__ == "__main__":
    main()