import random

def get_counter_move(move):
    rules = {'a': 'b', 'h': 'a', 'd': 'h', 'b': 'h'}
    return rules.get(move, 'a')

def get_valid_input():
    valid_moves = ['a', 'd', 'h', 'b']
    while True:
        move = input("Nhập nước đi của bạn (A/D/H/B): ").strip().lower()
        if move in valid_moves:
            return move
        print("không hợp lệ. nhập lại nha")

def play_round_1(total_turns=20):
    print("\nVòng 1 : dữ liệu")
    player_history = []
    
    for turn in range(total_turns):
        boss_move = random.choice(['a', 'd', 'h', 'b'])
        print(f"\n[Lượt {turn + 1}] lượt của boss: {boss_move.upper()}")
        
        player_move = get_valid_input()
        player_history.append(player_move)
        
    print("kết thúc vòng 1")
    return player_history

def play_round_2(predict_function, player_history):
    print("\nVòng 2 : thực chiến")
    boss_score = 0
    player_score = 0
    k_to_win = 5 
    
    while boss_score < k_to_win and player_score < k_to_win:
        predicted_move = predict_function(player_history)
        
        if predicted_move:
            boss_move = get_counter_move(predicted_move)
        else:
            boss_move = random.choice(['a', 'd', 'h', 'b'])
            
        print("\nboss chốt chiêu rồi, tới bạn")
        
        player_move = get_valid_input()
        
        print(f">> lượt của bạn: {player_move.upper()} | lượt của boss: {boss_move.upper()}")
        
        if boss_move == get_counter_move(player_move):
            print("boss thắng , điểm của boss +1")
            boss_score += 1
        elif player_move == get_counter_move(boss_move):
            print("bạn thắng, điểm của bạn +1")
            player_score += 1
            
        print(f"tổng số lần boss thắng: {boss_score}, tổng số lần bạn thắng: {player_score}")
        
        player_history.append(player_move)

    if boss_score >= k_to_win:
        print("\nGAME OVER, BOSS WON")
    else:
        print("\nCONGRATULATIONS , YOU WON")
