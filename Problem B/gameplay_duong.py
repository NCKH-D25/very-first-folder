import random
from predict import Skill, get_counter, predict_next
from trie import NGramTrie


def get_valid_input():
    valid_moves = {"a": Skill.ATTACK, "h": Skill.HEAL, "b": Skill.BLOCK}
    while True:
        move = input("Nhập nước đi của bạn (A/H/B): ").strip().lower()
        if move in valid_moves:
            return valid_moves[move]
        print("không hợp lệ. nhập lại nha")


def play_round_1(total_turns=20):
    print("\nVòng 1 :")
    player_history = []
    boss_score = 0
    player_score = 0
    for turn in range(total_turns):
        print(f"\n[Lượt {turn + 1}]")
        boss_move = random.choice([Skill.ATTACK, Skill.BLOCK, Skill.HEAL])
        player_move = get_valid_input()
        player_history.append(player_move)
        print(f"boss: {boss_move.name}")

        if boss_move == get_counter(player_move):
            print("boss thắng, điểm của boss +1")
            boss_score += 1
        elif player_move == get_counter(boss_move):
            print("bạn thắng, điểm của bạn +1")
            player_score += 1
        else:
            print("hòa nhau")

    print(
        f"tổng số lần boss thắng: {boss_score}, tổng số lần bạn thắng: {player_score}"
    )
    print("kết thúc vòng 1")
    return player_history


def play_round_2(trie_tree, player_history, total_turns=20):
    print("\nVòng 2 :")
    boss_score = 0
    player_score = 0
    k_to_win = 10

    context_history = (
        player_history[-2:] if len(player_history) >= 2 else player_history[:]
    )

    for turn in range(total_turns):
        predicted_move = predict_next(trie_tree, context_history)

        if predicted_move:
            boss_move = get_counter(predicted_move)
        else:
            boss_move = random.choice([Skill.ATTACK, Skill.BLOCK, Skill.HEAL])

        print(f"\n[Lượt {turn + 1}] boss đã hành động, tới lượt bạn")

        player_move = get_valid_input()

        print(f">> lượt của bạn: {player_move.name} | lượt của boss: {boss_move.name}")

        if boss_move == get_counter(player_move):
            print("boss thắng, điểm của boss +1")
            boss_score += 1
        elif player_move == get_counter(boss_move):
            print("bạn thắng, điểm của bạn +1")
            player_score += 1
        else:
            print("hòa nhau")

        print(
            f"tổng số lần boss thắng: {boss_score}, tổng số lần bạn thắng: {player_score}"
        )

        context_history.append(player_move)
        if len(context_history) > 2:
            context_history.pop(0)

    if boss_score >= k_to_win:
        print("\nGAME OVER, BOSS WON")
    else:
        print("\nCONGRATULATIONS, YOU WON")
    print(f"\nLOG: Tỉ lệ đoán trúng của boss: {(boss_score / total_turns) * 100} %")


if __name__ == "__main__":
    history = play_round_1(20)

    trie_tree = NGramTrie()
    n_gram = 3

    for i in range(len(history) - n_gram + 1):
        combo = history[i : i + n_gram]
        trie_tree.insert(combo)

    play_round_2(trie_tree, history, 20)
