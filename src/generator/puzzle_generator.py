import random
import json
import os

# -------------------------
# Standard puzzle functions
# -------------------------
def generate_arithmetic():
    n = random.randint(1, 10)
    q = f'{n} * ({n+1}) = ?'
    a = n*(n+1)
    e = f'Multiply {n} by {n+1} to get {a}.'
    return q, a, e

def generate_geometric():
    start = random.randint(1, 5)
    ratio = random.randint(2, 4)
    seq = [start, start*ratio, start*ratio**2]
    q = f'{", ".join(map(str, seq))}, ... ?'
    a = start*ratio**3
    e = f'Each term is multiplied by {ratio}. The next term is {a}.'
    return q, a, e

def generate_logical():
    n = random.randint(1, 20)
    seq = [i for i in range(n, n+4)]
    missing = random.choice(seq)
    display_seq = [str(x) if x != missing else "_" for x in seq]
    q = f'Find the missing number: {", ".join(display_seq)}'
    a = missing
    e = f'The sequence is consecutive numbers starting from {n}.'
    return q, a, e

def generate_fibonacci():
    seq = [0, 1]
    for _ in range(2, 5):
        seq.append(seq[-1]+seq[-2])
    missing = random.choice(seq)
    display_seq = [str(x) if x != missing else "_" for x in seq]
    q = f'Fibonacci sequence: {", ".join(display_seq)}'
    a = missing
    e = f'The next Fibonacci number is {a}.'
    return q, a, e

def generate_squares():
    n = random.randint(1, 10)
    seq = [i*i for i in range(n, n+4)]
    missing = random.choice(seq)
    display_seq = [str(x) if x != missing else "_" for x in seq]
    q = f'Square numbers sequence: {", ".join(display_seq)}'
    a = missing
    e = f'The sequence is consecutive squares. Missing is {a}.'
    return q, a, e

# -------------------------
# Load themes JSON
# -------------------------
THEMES_FILE = os.path.join(os.getcwd(), 'themes.json')
with open(THEMES_FILE, 'r') as f:
    THEMES = json.load(f)

# Map string names to functions
THEME_FUNCTIONS = {
    "generate_arithmetic": generate_arithmetic,
    "generate_geometric": generate_geometric,
    "generate_logical": generate_logical,
    "generate_fibonacci": generate_fibonacci,
    "generate_squares": generate_squares
}

# -------------------------
# Generate puzzles by theme
# -------------------------
def generate_puzzle_by_theme(theme_name):
    if theme_name == "Random":
        func = random.choice(list(THEME_FUNCTIONS.values()))
    else:
        func_name = THEMES.get(theme_name)
        func = THEME_FUNCTIONS.get(func_name, random.choice(list(THEME_FUNCTIONS.values())))
    return func()

def generate_puzzle_batch(count=5, theme_name="Random"):
    batch = []
    for _ in range(count):
        q, a, e = generate_puzzle_by_theme(theme_name)
        batch.append({'question': q, 'answer': a, 'explanation': e})
    return batch
