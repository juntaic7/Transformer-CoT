import argparse
import os
from datetime import datetime
import agents.gpt_batch_agents as gpt
import agents.claude_batch_agents as claude
import agents.qwen_batch_agents as qwen
from utils import read_jsonl


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parity check experiment.")

    parser.add_argument(    
        "-d", "--dataset",
        type=str,
        help="The path to load the dataset."
    )
    

    parser.add_argument(    
        "-l", "--letter",
        type=str,
        choices=["a", "b"],
        required=True,
        help="The letter (substring) to evaluate."
    )
    
    parser.add_argument(    
        "-a", "--agent",
        type=str,
        default="gpt",
        help="The LLM agent to solve the task."
    )
    
    parser.add_argument(    
        "-p", "--prompt_style",
        type=str,
        choices=["base", "cot"],
        required=True,
        help="The type of prompt."
    )

    
    parser.add_argument(    
        "-m", "--model",
        default="gpt-4o",
        help="Specify model version."
    )

    args = parser.parse_args()
    
    dataset = read_jsonl(args.dataset)
    path = args.dataset

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
            with open(f"parity_check/prompts/pc.txt", 'r') as file:
                prompt = file.read().strip()
        case "cot":
            with open(f"parity_check/prompts/pc.cot.txt", 'r') as file:
                prompt = file.read().strip()
    for line in dataset:
        docs[str(line["id"])] = prompt.replace("{{list}}", str(list(line["string"]))).replace("{{letter}}", args.letter)

    agent.create_requests(docs=docs, prompt="{doc}", model=args.model)
    batch_id = agent.send_requests()
    print(f"Requests sent to evaluate ability of GPT in parity checking.\nPlease download the batch_output file from the OpenAI API dashboard, or retrieve the result using the batch id {batch_id}.\nBatch request details will be saved to batch_history.txt for future reference.")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('batch_history.txt', 'a') as file:
        file.write(f"{current_time} - {os.path.splitext(os.path.basename(path))[0]} - {args.agent} - {args.model} - {args.prompt_style} - {args.letter} - {batch_id}\n")