import random

def get_counter_move(move):
    rules = {'a': 'b', 'h': 'a', 'd': 'h', 'b': 'h'}
    return rules.get(move, 'a')

def get_valid_input():
    valid_moves = ['a', 'd', 'h', 'b']
    while True:
        move = input("Nhß║¡p n╞░ß╗¢c ─æi cß╗ºa bß║ín (A/D/H/B): ").strip().lower()
        if move in valid_moves:
            return move
        print("kh├┤ng hß╗úp lß╗ç. nhß║¡p lß║íi nha")

def play_round_1(total_turns=20):
    print("\nV├▓ng 1 : dß╗» liß╗çu")
    player_history = []
    
    for turn in range(total_turns):
        boss_move = random.choice(['a', 'd', 'h', 'b'])
        print(f"\n[L╞░ß╗út {turn + 1}] l╞░ß╗út cß╗ºa boss: {boss_move.upper()}")
        
        player_move = get_valid_input()
        player_history.append(player_move)
        
    print("kß║┐t th├║c v├▓ng 1")
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
        
        print(f">> l╞░ß╗út cß╗ºa bß║ín: {player_move.upper()} | l╞░ß╗út cß╗ºa boss: {boss_move.upper()}")
        
        if boss_move == get_counter_move(player_move):
            print("boss thß║»ng , ─æiß╗âm cß╗ºa boss +1")
            boss_score += 1
        elif player_move == get_counter_move(boss_move):
            print("bß║ín thß║»ng, ─æiß╗âm cß╗ºa bß║ín +1")
            player_score += 1
            
        print(f"tß╗òng sß╗æ lß║ºn boss thß║»ng: {boss_score}, tß╗òng sß╗æ lß║ºn bß║ín thß║»ng: {player_score}")
        
        player_history.append(player_move)

    if boss_score >= k_to_win:
        print("\nGAME OVER, BOSS WON")
    else:
        print("\nCONGRATULATIONS , YOU WON")
