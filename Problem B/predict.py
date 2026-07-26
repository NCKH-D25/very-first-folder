from enum import Enum
import random


class Skill(Enum):
    ATTACK = 0
    DODGE = 1
    HEAL = 2


def skill_to_string(s: Skill) -> str:
    return s.name.capitalize()


def predict_next(history: list[Skill], n_gram: int = 3) -> Skill:
    k = n_gram - 1

    #tan suat toan cuc
    global_freq: dict[Skill, int] = {}
    for s in history:
        global_freq[s] = global_freq.get(s, 0) + 1

    #lay k chieu gan nhat lam ngu canh
    if k > 0 and len(history) >= k:
        context = history[-k:]
    elif k == 0:
        context = []
    else:
        context = history[:]  # chua du k chieu (dau van) -> dung tam ca history

    #hoi cay Trie
    counts = get_next_counts(context)

    #tim cac chieu co tan suat cao nhat
    max_freq = -1
    candidates: list[Skill] = []
    for s in Skill:  # duyet du ca 3 skill, ke ca skill chua tung xay ra
        freq = counts.get(s, 0)
        if freq > max_freq:
            max_freq = freq
            candidates = [s]
        elif freq == max_freq:
            candidates.append(s)

    # Khong hoa -> tra ve luon
    if len(candidates) == 1:
        return candidates[0]

    #phan dinh bang tan suat toan cuc
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

    #Neu van hoa thi random
    return random.choice(final_candidates)



def get_counter(predicted_move: Skill) -> Skill:
    mapping = {
        Skill.ATTACK: Skill.DODGE,   
        Skill.DODGE: Skill.HEAL,     
        Skill.HEAL: Skill.ATTACK,    
    }
    return mapping[predicted_move]
