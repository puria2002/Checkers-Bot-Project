# import the required modules
import numpy as np

# a class built to handle playing Checkers
class Checkers:
    def __init__(self):
        # the state of the game board, 0 means empty, 1 means player 1 regukar, 2 means player 1 king, 3 means player 2 regular, 4 means player 2 king
        #self.state = [[1,0,1,0,1,0,1,0], [0,1,0,1,0,1,0,1], [1,0,1,0,1,0,1,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,3,0,3,0,3,0,3], [3,0,3,0,3,0,3,0], [0,3,0,3,0,3,0,3]]
        self.state = "1010101001010101101010100000000000000000030303033030303003030303"

        # whose turn it is
        self.turn = 1
        #storing piece positions per player

        # who won, 0 for in progress,  1 and 2 for 1 or 2 victories respectively
        self.winner = 0 
        # keep of track of which number corresponds to which letter, for drawing purposes
        self.mark_dict = {'0': ' ', '1': 'r', '2': 'R', '3': 'w', '4': 'W'}
    
    # a function to print a row of the game board
    def print_helper(self, i):
        return '|'.join([self.mark_dict[self.state[j]] for j in range(8 * i, 8 * i + 8)])
    
    # a function to print the entire game board
    def print_state(self):
        print(self.print_helper(7))
        print("---------------")
        print(self.print_helper(6))
        print("---------------")
        print(self.print_helper(5))
        print("---------------")
        print(self.print_helper(4))
        print("---------------")
        print(self.print_helper(3))
        print("---------------")
        print(self.print_helper(2))
        print("---------------")
        print(self.print_helper(1))
        print("---------------")
        print(self.print_helper(0))
        print("---------------")
        print("\n")
    #see what state a given move induces without changing actual state
    def test_move(self, move):
        l = list(self.state)

        l[8*move[2] + move[3]] = l[8*move[0] + move[1]]
        l[8*move[0] +move[1]] = '0'

        #take off board if captured
        if (move[4]):
            l[8*((move[0] + move[2])//2) + (move[1] + move[3])//2] = '0'

        #take care of king logic
        if (move[2] == 0 and l[8*move[2] + move[3]] == '3'):
            l[8*move[2] + move[3]] = '4'
        if (move[2] == 7 and l[8*move[2] + move[3]] == '1'):
            l[8*move[2] + move[3]] = '2'
        return ''.join(l)
    #make an actual move on the gameboard
    def make_move(self, move):
        #update positions based on move 
        l = list(self.state)

        l[8*move[2] + move[3]] = l[8*move[0] + move[1]]
        l[8*move[0] +move[1]] = '0'

        #take off board if captured
        if (move[4]):
            l[8*((move[0] + move[2])//2) + (move[1] + move[3])//2] = '0'

        #take care of king logic
        if (move[2] == 0 and l[8*move[2] + move[3]] == '3'):
            l[8*move[2] + move[3]] = '4'
        if (move[2] == 7 and l[8*move[2] + move[3]] == '1'):
            l[8*move[2] + move[3]] = '2'
        self.state = ''.join(l)
        if (self.turn == 1):
            self.turn = 2
        else:
            self.turn = 1
    def isValid(self, x,y):
        if (x >= 8 or x < 0 or y>=8 or y < 0):
            return False 
        return True
    
    # returns a list of moves for possible moves for the current player
    def generate_possible_moves(self):
        #a move is a tuple consisting of: index of start, index of end, whether a capture was done
        moves =[]
        
        regpos =[]
        kingpos = []

        captured = False

        if (self.turn == 1):
            for i in range(8):
                for j in range(8):
                    if (self.state[8*i + j] == '1'):
                        regpos.append((i,j))
                    elif (self.state[8*i + j] == '2'):
                        kingpos.append((i,j))
        else:
            for i in range(8):
                for j in range(8):
                    if (self.state[8*i + j] == '3'):
                        regpos.append((i,j))
                    elif (self.state[8*i + j] == '4'):
                        kingpos.append((i,j))
        
        if (self.turn == 1):
            xr = [1,1]
            yr = [-1,1]

            xk = [1,1,-1,-1]
            yk = [-1,1,-1,1]

            for pos in regpos:

                for i in range(2):
                    if (self.isValid(xr[i] + pos[0], yr[i] + pos[1])):

                        if (self.state[8*(xr[i] + pos[0]) + yr[i] + pos[1]] == '0'):
                            moves.append((pos[0], pos[1], pos[0] + xr[i], pos[1] + yr[i], False))

                        elif (self.state[8*(xr[i] + pos[0]) + yr[i] + pos[1]] == '3' or self.state[8*(xr[i] + pos[0]) + yr[i] + pos[1]] == '4'):

                            if (self.isValid(2*xr[i] + pos[0], 2*yr[i] + pos[1]) and self.state[8*(2*xr[i] + pos[0])+2*yr[i] + pos[1]] == '0'):
                                moves.append((pos[0], pos[1], pos[0] + 2*xr[i], pos[1] + 2*yr[i], True))
                                captured = True
            for pos in kingpos:

                for i in range(4):
                    if (self.isValid(xk[i] + pos[0], yk[i] + pos[1])):

                        if (self.state[8*(xk[i] + pos[0]) + yk[i] + pos[1]] == '0'):
                            moves.append((pos[0], pos[1], pos[0] + xk[i], pos[1] + yk[i], False))

                        elif (self.state[8*(xk[i] + pos[0]) + yk[i] + pos[1]] == '3' or self.state[8*(xk[i] + pos[0]) + yk[i] + pos[1]] == '4'):

                            if (self.isValid(2*xk[i] + pos[0], 2*yk[i] + pos[1]) and self.state[8*(2*xk[i] + pos[0])+2*yk[i] + pos[1]] == '0'):
                                moves.append((pos[0], pos[1], pos[0] + 2*xk[i], pos[1] + 2*yk[i], True))
                                captured = True
        else:
            xr = [-1,-1]
            yr = [-1,1]

            xk = [1,1,-1,-1]
            yk = [-1,1,-1,1]

            for pos in regpos:

                for i in range(2):
                    if (self.isValid(xr[i] + pos[0], yr[i] + pos[1])):

                        if (self.state[8*(xr[i] + pos[0]) + yr[i] + pos[1]] == '0'):
                            moves.append((pos[0], pos[1], pos[0] + xr[i], pos[1] + yr[i], False))

                        elif (self.state[8*(xr[i] + pos[0]) + yr[i] + pos[1]] == '1' or self.state[8*(xr[i] + pos[0]) + yr[i] + pos[1]] == '2'):

                            if (self.isValid(2*xr[i] + pos[0], 2*yr[i] + pos[1]) and self.state[8*(2*xr[i] + pos[0])+2*yr[i] + pos[1]] == '0'):
                                moves.append((pos[0], pos[1], pos[0] + 2*xr[i], pos[1] + 2*yr[i], True))
                                captured = True
            for pos in kingpos:

                for i in range(4):
                    if (self.isValid(xk[i] + pos[0], yk[i] + pos[1])):

                        if (self.state[8*(xk[i] + pos[0]) + yk[i] + pos[1]] == '0'):
                            moves.append((pos[0], pos[1], pos[0] + xk[i], pos[1] + yk[i], False))

                        elif (self.state[8*(xk[i] + pos[0]) + yk[i] + pos[1]] == '1' or self.state[8*(xk[i] + pos[0]) + yk[i] + pos[1]] == '2'):

                            if (self.isValid(2*xk[i] + pos[0], 2*yk[i] + pos[1]) and self.state[8*(2*xk[i] + pos[0])+2*yk[i] + pos[1]] == '0'):
                                moves.append((pos[0], pos[1], pos[0] + 2*xk[i], pos[1] + 2*yk[i], True))
                                captured = True
        #logic to force capture if a capture is available
        if (captured):
            newmoves = list(filter(lambda x: x[4], moves))
            return newmoves
        return moves

# the ML agent that will learn how to play Checkers. 
class Agent:
    def __init__(self, learning_rate):
        # game states it has seen before and their corresponding values
        self.values = {}
        self.prev_state = None
        # how much the Agent should adjust values when finding good / bad states
        self.learning_rate = learning_rate
        
    def get_value(self, state):
        if state not in self.values.keys():
            self.values[state] = 0.5
        return self.values[state]
    
    def make_move(self, game, possible_moves, explore_prob=0.05):
        
        # randomness to balance explore / exploit
        if np.random.random() < explore_prob:
            # Make exploratory move
            random_move = possible_moves[np.random.randint(len(possible_moves))]
            game.make_move(random_move)
            # Don't update value of previous state since this is random
            self.prev_state = game.state
        else:
            #search possible states
            possible_states = [game.test_move(move) for move in possible_moves]
            vals = [self.get_value(state) for state in possible_states]
            # Make exploitative move;
            best_move = possible_moves[np.argmax(vals)]
            game.make_move(best_move)
            if self.prev_state is not None:
                self.get_value(self.prev_state)
                # Update value of previous state
                self.values[self.prev_state] += self.learning_rate * (self.get_value(game.state) 
                                                                      - self.get_value(self.prev_state))
            self.prev_state = game.state
    
    def new_game(self):
        self.prev_state = None
# a basic, hard-coded opponent to test our bot against
class Opponent:
    def __init__(self, level=0):
        # 0 = random, 1 = win if possible, otherwise random, 2 = win and block losses, otherwise random
        self.level = level
    
    # make a random move
    def make_random_move(self, game, possible_moves):
        random_move = possible_moves[np.random.randint(len(possible_moves))]
        game.make_move(random_move)
    
# untrained tallies
wins = 0
ties = 0
losses = 0
total_games = 1000


# play total_games number of games, WITHOUT training / learning
for _ in range(total_games):
    game = Checkers()
    agent = Agent(0.05)
    opponent = Opponent(level=0)
    agent.new_game()
    while True:
        possible_moves = game.generate_possible_moves()
        #learn from loss and end game
        if (len(possible_moves) == 0):
            agent.get_value(agent.prev_state)
            agent.values[agent.prev_state] += agent.learning_rate * (0 - agent.get_value(agent.prev_state))
            losses += 1
            break

        agent.make_move(game, possible_moves)

        possible_moves = game.generate_possible_moves()
        #learn from win and end game 
        if (len(possible_moves) == 0):
            agent.get_value(agent.prev_state)
            agent.values[agent.prev_state] = 1
            wins += 1
            break
        opponent.make_random_move(game, possible_moves)

# output the benchmark results
print(f"Record: {wins}-{losses}-{ties}")
print(f"Win Percentage: {100 * wins / total_games}")

#training our agent
training_games = 10000
trained_agent = Agent(0.05)
count = 0
tot = 0
for _ in range(training_games):
    if (count == training_games//100):
        count = 0
        tot += 1
        print("Percent trained: " + str(tot))
    game = Checkers()
    opponent = Opponent(level=0)
    trained_agent.new_game()
    while True:
        possible_moves = game.generate_possible_moves()
        #learn from loss and end game
        if (len(possible_moves) == 0):
            trained_agent.get_value(trained_agent.prev_state)
            trained_agent.values[trained_agent.prev_state] += trained_agent.learning_rate * (0 - trained_agent.get_value(trained_agent.prev_state))
            break

        trained_agent.make_move(game, possible_moves)

        possible_moves = game.generate_possible_moves()
        #learn from win and end game 
        if (len(possible_moves) == 0):
            trained_agent.get_value(trained_agent.prev_state)
            trained_agent.values[agent.prev_state] = 1
            break
        opponent.make_random_move(game, possible_moves)
    count += 1

# trained tallies
wins = 0
ties = 0
losses = 0
total_games = 1000

# play total_games number of games, to test the trained Agent
for _ in range(total_games):
    game = Checkers()
    opponent = Opponent(level=0)
    trained_agent.new_game()
    while True:
        possible_moves = game.generate_possible_moves()
        #learn from loss and end game
        if (len(possible_moves) == 0):
            trained_agent.get_value(trained_agent.prev_state)
            trained_agent.values[trained_agent.prev_state] += trained_agent.learning_rate * (0 - trained_agent.get_value(trained_agent.prev_state))
            losses += 1
            break

        trained_agent.make_move(game, possible_moves)

        possible_moves = game.generate_possible_moves()
        #learn from win and end game 
        if (len(possible_moves) == 0):
            trained_agent.get_value(trained_agent.prev_state)
            trained_agent.values[agent.prev_state] = 1
            wins += 1
            break
        opponent.make_random_move(game, possible_moves)

# output the results of the trained agent and compare to benchmark
print(f"Record: {wins}-{losses}-{ties}")
print(f"Win Percentage: {100 * wins / total_games}")