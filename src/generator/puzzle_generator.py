import random

def generate_number_pattern():
    n = random.randint(2, 8)

    seq = []
    for i in range(n, n+4):
        seq.append((i, i*(i+1)))

    question = "\n".join([f"{a} -> {b}" for a,b in seq[:-1]])
    question += f"\n{seq[-1][0]} -> ?"

    answer = str(seq[-1][1])
    explanation = "Pattern: n x (n + 1)"

    return {
        "type": "number_pattern",
        "question": question,
        "answer": answer,
        "explanation": explanation
    }

def generate_puzzle():
    # 🔥 ONLY ONE PUZZLE
    return [generate_number_pattern()]
