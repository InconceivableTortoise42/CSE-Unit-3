import random 
strategy_name = "If you win, play opponents move next, if you lose play the move that beats oponent"
opponent_pattern = ""
beat_pattern = ""
current_pattern_index = None

def beat_move(move) -> str:
    if (move=="r"):
        return "p"
    if (move == "p"):
        return "s"
    if (move=="s"):
        return "r"
    else:
        return ""

def detect_pattern(history):
    history = history[::-1]
    for i in range(1, 50):
        sample = history[:i]
        search_string = history
        matches = 0
        while True: 
            match = search_string.startswith(sample)
            if match:
                # print(match,"-", sample,"-", search_string)
                search_string = search_string[len(sample):]
                matches += 1
            else:
                break
        if matches > 10:
            return sample 
    else:
        return None

def anti_pattern(pattern: str):
    anti_pattern = ""
    for char in pattern:
        anti_pattern += beat_move(char)
    return anti_pattern

def find_current_pattern_index(history: str, pattern: str) -> int:
    index = history.rfind(pattern)
    print(history, history[index:], pattern, index)
    return 0

def move(my_history, their_history):
    if len(their_history) == 50:
        pattern = detect_pattern(their_history)
        if pattern:
            opponent_pattern = pattern
            beat_pattern = anti_pattern(pattern)
            current_pattern_index = find_current_pattern_index(their_history, pattern)
            # print(their_history, current_pattern_index, opponent_pattern, beat_pattern[current_pattern_index + 1])
    if len(their_history) and len(my_history):
        if beat_move(their_history[-1]) == my_history[-1]: # Win
            return their_history[-1]
        elif their_history[-1] == my_history[-1]: # Draw
            return random.choice(["r", "p", "s"])
        else: # Loss
            return beat_move(their_history[-1])
    return random.choice(["r", "p", "s"])