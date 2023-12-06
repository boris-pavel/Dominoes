import random

PLAYER_PIECES = 7


def generate_domino_set():
    lst = []
    for i in range(0, 7):
        for j in range(i, 7):
            lst.append([i, j])
    return lst


def split_to_player(domino_set):
    lst = []
    for i in range(PLAYER_PIECES):
        lst.append(domino_set.pop(random.randint(0, len(domino_set) - 1)))
    return lst


def get_highest_double(player):
    current_highest_double = None
    for piece in player:
        a, b = piece
        if a == b:
            if current_highest_double is None:
                current_highest_double = [a, a]
                continue
            highest_a = current_highest_double[0]
            if highest_a < a:
                current_highest_double = [a, a]
    return current_highest_double


def get_first_player(computer, player):
    computer_double = get_highest_double(computer)
    player_double = get_highest_double(player)
    if computer_double is None and player_double is None:
        return 'reshuffle'
    elif computer_double is None and player_double is not None:
        return 'player'
    elif computer_double is not None and player_double is None:
        return 'computer'

    if computer_double[0] > player_double[0]:
        return 'computer'
    else:
        return 'player'


def check_end_game(domino_snake, player, computer):
    if len(player) == 0:
        return 'player'
    if len(computer) == 0:
        return 'computer'
    count = 0
    if len(domino_snake) > 2:
        if domino_snake[0][0] == domino_snake[len(domino_snake) - 1][1]:
            for piece in domino_snake:
                if domino_snake[0][0] == piece[0]:
                    count += 1
                if domino_snake[0][0] == piece[1]:
                    count += 1
    if count == 8:
        return 'draw'
    return None


def verify_legal(domino_snake, piece, side):
    if side:
        if piece[0] == domino_snake[-1][1] or piece[1] == domino_snake[-1][1]:
            return True
        else:
            return False
    else:
        if piece[0] == domino_snake[0][0] or piece[1] == domino_snake[0][0]:
            return True
        else:
            return False


def count_appearances(domino_snake, hand):
    d = {i: 0 for i in range(7)}
    for piece in domino_snake:
        d[piece[0]] += 1
        d[piece[1]] += 1
    for piece in hand:
        d[piece[0]] += 1
        d[piece[1]] += 1
    return d


def calculate_score(d, piece):
    return d[piece[0]] + d[piece[1]]


def is_equal_domino(tupl, lst):
    return tupl[0] == lst[0] and tupl[1] == lst[1]


def main():
    domino_set = generate_domino_set()
    computer_pieces = split_to_player(domino_set)
    player_pieces = split_to_player(domino_set)
    first_player = get_first_player(computer_pieces, player_pieces)
    domino_snake = []
    if first_player == 'reshuffle':
        pass
    elif first_player == 'player':
        first_player = 'computer'
        domino_snake.append(get_highest_double(player_pieces))
        player_pieces.remove(get_highest_double(player_pieces))
    elif first_player == 'computer':
        first_player = 'player'
        domino_snake.append(get_highest_double(computer_pieces))
        computer_pieces.remove((get_highest_double(computer_pieces)))
    while True:
        print('======================================================================')
        print(f'Stock size: {len(domino_set)}')
        print(f'Computer pieces: {len(computer_pieces)}\n')

        if len(domino_snake) > 6:
            for i in range(3):
                print(domino_snake[i], end='')
            print('...', end='')
            for i in range(-3, 0):
                print(domino_snake[i], end='')
        else:
            for piece in domino_snake:
                print(piece, end='')
        print('\n')

        piece_count = 1

        print('Your pieces:')
        for piece in player_pieces:
            print(f'{piece_count}:{piece}')
            piece_count += 1
        print()

        end = check_end_game(domino_snake, player_pieces, computer_pieces)
        match end:
            case 'player':
                print('Status: The game is over. You won!')
                break
            case 'computer':
                print('Status: The game is over. The computer won!')
                break
            case 'draw':
                print('Status: The game is over. It\'s a draw!')
                break

        if first_player == 'player':
            print('Status: It\'s your turn to make a move. Enter your command.')
        elif first_player == 'computer':
            print('Status: Computer is about to make a move. Press Enter to continue...')

        while True:
            command = input()
            if first_player == 'player':
                try:
                    command = int(command)
                    if -len(player_pieces) > command or command > len(player_pieces):
                        raise ValueError
                    if command > 0:
                        if not verify_legal(domino_snake, player_pieces[command - 1], True):
                            print('Illegal move. Please try again.')
                            continue
                        if domino_snake[-1][1] != player_pieces[command - 1][0]:
                            player_pieces[command - 1].reverse()
                        domino_snake.append(player_pieces[command - 1])
                        player_pieces.pop(command - 1)
                        first_player = 'computer'
                    elif command < 0:
                        if not verify_legal(domino_snake, player_pieces[-command - 1], False):
                            print('Illegal move. Please try again.')
                            continue
                        if domino_snake[0][0] != player_pieces[-command - 1][1]:
                            player_pieces[-command - 1].reverse()
                        domino_snake.insert(0, player_pieces[-command - 1])
                        player_pieces.pop(-command - 1)
                        first_player = 'computer'
                    else:
                        if len(domino_set):
                            player_pieces.append(domino_set.pop(random.randint(0, len(domino_set) - 1)))
                        first_player = 'computer'
                    break
                except ValueError:
                    print('Invalid input. Please try again.')
                    continue

            else:
                running = True
                d = count_appearances(domino_snake, computer_pieces)
                score_dict = dict()
                for piece in computer_pieces:
                    score = calculate_score(d, piece)
                    score_dict.update({tuple(piece): score})
                score_dict = sorted(score_dict, key=score_dict.get, reverse=True)
                computer_pieces = [list(piece) for piece in score_dict]

                for piece in computer_pieces:
                    if verify_legal(domino_snake, piece, True):
                        if piece[0] != domino_snake[-1][1]:
                            piece.reverse()
                        domino_snake.append(piece)
                        computer_pieces.remove(piece)
                        running = False
                        break
                    if verify_legal(domino_snake, piece, False):
                        if piece[1] != domino_snake[0][0]:
                            piece.reverse()
                        domino_snake.insert(0, piece)
                        computer_pieces.remove(piece)
                        running = False
                        break
                if running:
                    if len(domino_set):
                        computer_pieces.append(domino_set.pop(random.randint(0, len(domino_set) - 1)))
                first_player = 'player'
                break


main()
