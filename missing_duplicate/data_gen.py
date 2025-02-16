import argparse
import random
import json

def generate_binary_string(len: int) -> str:
    sample = ''.join(random.choice("01") for _ in range(len))
    return sample

def main():
    parser = argparse.ArgumentParser(description="Generate dataset for bucket sort task.")
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
        help="Length of the binary string."
    )
    args = parser.parse_args()
    dataset = []
    for i in range(args.num):
        s = generate_binary_string(int(args.length * 0.5)) * 2
        pos = random.randint(0, len(s) - 1)
        s_new = s[:pos] + "2" + s[pos + 1:]
        dataset.append({"id": i, "string": s_new, "missed": s[pos]})
    out_file = f"missing_duplicate/datasets/md_{args.length}.jsonl"
    with open(out_file, "w") as file:
        for item in dataset:
            file.write(json.dumps(item) + '\n')
            
    print(f"Dataset successfully saved to {out_file}")
    
if __name__ == "__main__":
    main()