import argparse
import os
from datetime import datetime
import agents.gpt_batch_agents as gpt
import agents.claude_batch_agents as claude
import agents.qwen_batch_agents as qwen
from utils import read_jsonl

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(    
        "-d", "--dataset",
        type=str,
        help="The path of the dataset."
    )

    parser.add_argument(    
        "-p", "--prompt_style",
        choices = ["base", "cot"],
        required=True,
        help="Select prompt style."
    )
    
    parser.add_argument(    
        "-a", "--agent",
        type=str,
        default="gpt",
        help="The LLM agent to solve the task."
    )
    
    parser.add_argument(    
        "-m", "--model",
        default="gpt-4o",
        help="Specify model version."
    )

    args = parser.parse_args()
    dataset = read_jsonl(args.dataset)
    
    docs = {}
    
    match args.agent:
        case "gpt":
            agent = gpt
        case "claude":
            agent = claude
        case "qwen":
            agent = qwen

    match args.prompt_style:
        case "base":
            with open(f"bucket_sort/prompts/ss.txt", 'r') as file:
                prompt = file.read().strip()
        case "cot":
            with open(f"bucket_sort/prompts/ss.cot.txt", 'r') as file:
                prompt = file.read().strip()
    for line in dataset:
        docs[str(line["id"])] = prompt.replace("{{list}}", str(list(line["string"])))
        

    agent.create_requests(docs=docs, prompt="{doc}", model=args.model)
    batch_id = agent.send_requests()
    print(f"Requests sent to evaluate ability of GPT for cycle navigation task.\nPlease download the batch_output file from the OpenAI API dashboard, or retrieve the result using the batch id {batch_id}.\nBatch request details will be saved to batch_history.txt for future reference.")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('batch_history.txt', 'a') as file:
        file.write(f"{current_time} - {os.path.splitext(os.path.basename(args.dataset))[0]} - {args.agent} - {args.model} - {args.prompt_style} - {batch_id}\n")