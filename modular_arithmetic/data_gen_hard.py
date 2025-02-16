import argparse
import json
import random

digits = ['0', '1', '2', '3', '4']
ops = ['+', '-', '·']  # We'll convert '·' to '*' before eval in Python

def random_expr(depth=0, max_depth=3, top_level=False):
    """
    Generate a random expression string.
    
    :param depth: Current recursion depth.
    :param max_depth: Maximum depth to avoid infinite growth.
    :param top_level: Whether this call is generating the top-level expression.
    :return: A string representing the expression.
    """
    # If we've reached the max depth, just return a random digit
    # to avoid expressions that grow too big.
    if depth >= max_depth:
        return random.choice(digits)
    
    # We can either produce a single digit or a binary operation
    # but for the top-level, we do NOT wrap the entire thing in parentheses.
    # For a sub-expression, we do wrap in parentheses.
    
    # Randomly decide to produce a digit or a sub-expression
    # (You can tweak these probabilities.)
    if depth > 0 and random.random() < 0.3:
        # Return just a digit
        return random.choice(digits)
    else:
        # Produce a binary operation
        op = random.choice(ops)
        left = random_expr(depth+1, max_depth, top_level=False)
        right = random_expr(depth+1, max_depth, top_level=False)
        
        if top_level:
            # Top-level expression: no parentheses around the whole thing
            return left + op + right
        else:
            # Sub-expression: wrap in parentheses
            return "(" + left + op + right + ")"

def evaluate_mod_5(expr_string):
    """
    Evaluate the expression modulo 5.
    We need to replace '·' with '*' so Python's eval can handle multiplication.
    Also be mindful of Python's interpretation of '-' (it’s fine normally).
    """
    # Replace the '·' symbol with Python's '*'
    safe_expr = expr_string.replace('·', '*')
    
    # Evaluate in Python, then mod 5
    val = eval(safe_expr)  # Be careful with eval in production code!
    return val % 5

def generate_expressions_with_length(target_length=39, n_samples=5, max_depth=5):
    """
    The length of the expression is the number of digits + the number of operators, and it must have the form of 4n+3.
    Keep randomly generating expressions until we find n_samples of the exact length.
    Returns a list of (expr, result_mod_5) pairs.
    """
    results = []
    
    while len(results) < n_samples:
        expr = random_expr(depth=0, max_depth=max_depth, top_level=True)
        if len(expr) == target_length:  # Check length
            # Evaluate modulo 5
            result = evaluate_mod_5(expr)
            results.append((expr, result))
    
    return results

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

    samples = generate_expressions_with_length(
        target_length=args.length,
        n_samples=args.num,
        max_depth=5
    )
    
    dataset = []
    for i in range(len(samples)):
        expr, result = samples[i]
        dataset.append({"id": i, "expr": expr, "result": result})
    out_file = f"modular_arithmetic/datasets/ma_hard_{args.length}.jsonl"
    with open(out_file, "w") as file:
        for item in dataset:
            file.write(json.dumps(item) + '\n')
            
    print(f"Dataset successfully saved to {out_file}")
