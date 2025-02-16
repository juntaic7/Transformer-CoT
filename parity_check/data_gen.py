import argparse
import random
import json


def generate_samples(length: int, num: int) -> list[str]:
    """Generates num unique random strings with target length."""
    samples = set()
    
    while len(samples) < num:
        sample = ''.join(random.choice('ab') for _ in range(length))
        samples.add(sample)
        
    return list(samples)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate dataset of random strings of 'a' and 'b' with parity information.")
    
    parser.add_argument(
        "-n", "--num",
        type=int,
        help="Number of samples to generate."
    )

    parser.add_argument(
        "-l", "--length",
        type=int,
        help="The length of samples."
    )
    
    args = parser.parse_args()
    random.seed(42)
    samples = generate_samples(length=args.length, num=args.num)

    dataset = []
    for i, sample in enumerate(samples):
        dataset.append({
            "id": i,
            "string": sample,
            "a": sample.count('a') % 2 == 0,
            "b": sample.count('b') % 2 == 0
        })

    output_file = f"parity_check/datasets/pc_{args.length}.jsonl"
    with open(output_file, "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")

    print(f"Dataset saved to {output_file}.")
    path = output_file