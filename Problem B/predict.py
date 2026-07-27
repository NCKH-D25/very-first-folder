from enum import Enum
import random


class Skill(Enum):
    ATTACK = 0
    BLOCK = 1
    HEAL = 2


def skill_to_string(s: Skill) -> str:
    return s.name.capitalize()


def predict_next(trie, history: list[Skill], n_gram: int = 4) -> Skill:
    k = n_gram - 1

    global_freq: dict[Skill, int] = {}
    for s in history:
        global_freq[s] = global_freq.get(s, 0) + 1

    if k > 0 and len(history) >= k:
        context = history[-k:]
    elif k == 0:
        context = []
    else:
        context = history[:]

    counts = trie.search(context) if trie else {}
    if counts is None:
        counts = {}

    max_freq = -1
    candidates: list[Skill] = []
    for s in Skill:
        freq = counts.get(s, 0)
        if freq > max_freq:
            max_freq = freq
            candidates = [s]
        elif freq == max_freq:
            candidates.append(s)

    if len(candidates) == 1:
        return candidates[0]

    # Tie-Breaking
    best_global = -1
    final_candidates: list[Skill] = []
    for s in candidates:
        freq = global_freq.get(s, 0)
        if freq > best_global:
            best_global = freq
            final_candidates = [s]
        elif freq == best_global:
            final_candidates.append(s)

    if len(final_candidates) == 1:
        return final_candidates[0]

    return random.choice(final_candidates)


def get_counter(predicted_move: Skill) -> Skill:
    mapping = {
        Skill.ATTACK: Skill.BLOCK,
        Skill.BLOCK: Skill.HEAL,
        Skill.HEAL: Skill.ATTACK,
    }
    return mapping[predicted_move]
