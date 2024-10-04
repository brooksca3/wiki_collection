import torch
import sys
from binoculars import Binoculars
import sys
torch.cuda.empty_cache()

bino = Binoculars()

def ai_score(lines, truncate_to=5000):
    print(f"number of lines: {len(lines)}")
    scores = []
    for ind, line in enumerate(lines):
        score = bino.compute_score(' '.join(line.strip().split()[:truncate_to]))
        print(score, ind)
        scores.append((score, ind))  # Store score, index, and line

    return scores