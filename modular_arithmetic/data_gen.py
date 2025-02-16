import argparse
import random
import json
from typing import List, Tuple

def generate_expression(target_length: int) -> Tuple[str, int]:
    """Generate an expression of exact target length and its result modulo 5."""
    
    while True:
        # For target_length=20, we need exactly 10 numbers and 9 operators
        # to get a valid expression of correct length
        numbers_needed = (target_length + 1) // 2
        operators_needed = numbers_needed - 1
        
        if numbers_needed + operators_needed != target_length:
            raise ValueError(f"Cannot generate expression of length {target_length}")
            
        # Generate numbers and operators
        numbers = [str(random.randint(0, 4)) for _ in range(numbers_needed)]
        operators = [random.choice(['+', '-', '·']) for _ in range(operators_needed)]
        
        # Interleave numbers and operators
        expr = []
        for i in range(operators_needed):
            expr.append(numbers[i])
            expr.append(operators[i])
        expr.append(numbers[-1])
        
        expression = ''.join(expr)
        
        # Calculate result
        try:
            # Replace · with * for evaluation
            eval_expr = expression.replace('·', '*')
            result = eval(eval_expr) % 5
            return expression, result
        except:
            continue

def generate_samples(count: int, length: int) -> List[Tuple[str, int]]:
    """Generate multiple sample expressions with their results."""
    samples = []
    for _ in range(count):
        expr, result = generate_expression(length)
        samples.append((expr, result))
    return samples

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        required=True,
        help="Number of samples to generate."
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        required=True,
        help="Length of the samples."
    )
    args = parser.parse_args()
    
    samples = generate_samples(args.num, args.length)
    dataset = []
    for i in range(len(samples)):
        expr, result = samples[i]
        dataset.append({"id": i, "expr": expr, "result": result})
    out_file = f"modular_arithmetic/datasets/ma_{args.length}.jsonl"
    with open(out_file, "w") as file:
        for item in dataset:
            file.write(json.dumps(item) + '\n')
            
    print(f"Dataset successfully saved to {out_file}")