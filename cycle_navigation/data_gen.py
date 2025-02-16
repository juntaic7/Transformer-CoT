import argparse
import json
import random

def generate_sample(length: int) -> str:
    sample = ''.join(random.choice('012') for _ in range(length))
    return sample

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--num",
        type=int,
        required=True,
        help="Number of samples to generate." 
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        required=True,
        help="Length of the samples."
    )
    
    args = parser.parse_args()
    dataset = []
    
    for i in range(args.num):
        seq = generate_sample(args.length)
        dataset.append({"id": i, "string": seq, "state": (seq.count('1')-seq.count('2'))%5})
    out_file = f"cycle_navigation/datasets/cn_{args.length}.jsonl"
    
    with open(out_file, "w") as file:
        for item in dataset:
            file.write(json.dumps(item) + '\n')
            
    print(f"Dataset successfully saved to {out_file}")
            
if __name__ == "__main__":
    main()