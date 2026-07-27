import random

def get_counter_move(move):
    rules = {'a': 'b', 'h': 'a', 'b': 'h'}
    return rules.get(move, 'a')

def get_valid_input():
    valid_moves = ['a', 'h', 'b']
    while True:
        move = input("Nhap nuoc di cua ban (A/H/B): ").strip().lower()
        if move in valid_moves:
            return move
        print("Khong hop le. Nhap lai nha.")

def play_round_1(total_turns=20):
    print("\nVong 1 : Thu thap du lieu")
    player_history = []
    
    for turn in range(total_turns):
        boss_move = random.choice(['a', 'h', 'b'])
        print(f"\n[Luot {turn + 1}] Luot cua boss: {boss_move.upper()}")
        
        player_move = get_valid_input()
        player_history.append(player_move)
        
    print("Ket thuc Vong 1")
    return player_history

def play_round_2(predict_function, player_history, total_turns=20):
    print("\nVòng 2 : thực chiến")
    boss_score = 0
    player_score = 0
    k_to_win = 10 
    
    for turn in range(total_turns):
        predicted_move = predict_function(player_history)
        
        if predicted_move:
            boss_move = get_counter_move(predicted_move)
        else:
            boss_move = random.choice(['a', 'b', 'h'])
            
        print(f"\n[Lượt {turn + 1}] boss chốt chiêu rồi, tới bạn")
        
        player_move = get_valid_input()
        
        print(f">> Luot cua ban: {player_move.upper()} | Luot cua boss: {boss_move.upper()}")
        
        if boss_move == get_counter_move(player_move):
            print("Boss thang, diem cua boss +1")
            boss_score += 1
        elif player_move == get_counter_move(boss_move):
            print("Ban thang, diem cua ban +1")
            player_score += 1
            
        print(f"Tong so lan boss thang: {boss_score}, tong so lan ban thang: {player_score}")
        
        player_history.append(player_move)

    if boss_score >= k_to_win:
        print("\nGAME OVER, BOSS WON")
    else:
        print("\nCONGRATULATIONS , YOU WON")

if __name__ == '__main__':
    def mock_predict(history):
        return random.choice(['a', 'b', 'h'])
    print("--- CHAY THU DEMO GAMEPLAY ---")
    h = play_round_1(total_turns=3)
    play_round_2(mock_predict, h, total_turns=3)

