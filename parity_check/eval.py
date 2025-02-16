import argparse
from utils import read_jsonl, extract_result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Path of batch_output file."
    )
    parser.add_argument(
        "-d", "--dataset",
        type=str,
        required=True,
        help="Path of the dataset."
    )
    parser.add_argument(
        "-l", "--letter",
        type=str,
        choices=["a", "b"],
        required=True,
        help="The letter (substring) for parity checking."
    )
    
    args = parser.parse_args()
    
    dataset = read_jsonl(args.dataset)
    results = read_jsonl(args.path)

    preds = {}
    for r in results:
        id = int(r["custom_id"].split("-")[1])
        completion = r["response"]["body"]["choices"][0]["message"]["content"]
        
        result_str = extract_result(completion)
        if result_str is not None:
            preds[id] = result_str
        else:
            print(f"Result not found in response for ID {id}. Please check and fix the response or revise prompt template.")
            print(f"Completion: {repr(completion)}")
            preds[id] = ""
            continue


    correct_count = 0
    for idx, pred in preds.items():
        if pred == str(dataset[idx][args.letter]):
            correct_count += 1
    
    accuracy = correct_count / len(preds) if len(preds) > 0 else 0
    print(f"The final accuracy is: {accuracy:.2%}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")