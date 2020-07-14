import numpy as np
import pickle
import random

class Game:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.board = np.zeros((3, 3))
        self.end = False
        self.place_symbol = 1
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0

    def get_Hash(self):
        return str(self.board.flatten())  # gamestate ID

    def available_spots(self):
        return np.array(np.where(self.board == 0)).T  # list of coordinates that don't have a symbol

    def updateState(self, position):
        self.board[tuple(position)] = self.place_symbol
        # switch to another player
        self.place_symbol = -1 if self.place_symbol == 1 else 1

    def winner(self):
        # check rows
        p1rowsum = max(np.sum(self.board, axis=1))
        p2rowsum = min(np.sum(self.board, axis=1))
        # check columns
        p1colsum = max(np.sum(self.board, axis=0))
        p2colsum = min(np.sum(self.board, axis=0))
        # check both diagonals
        diag1sum = self.board.trace()
        diag2sum = np.rot90(self.board).trace()
        if (p1rowsum == 3) or (p1colsum == 3) or (diag1sum == 3) or (diag2sum == 3):
            return 1
        elif (p2rowsum == -3) or (p2colsum == -3) or (diag1sum == -3) or (diag2sum == -3):
            return -1

        if len(self.available_spots()) == 0:
            self.end = True
            return 0
        else:
            return None  # still playing

    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(2)
            self.p2.feedReward(-2)
            self.win_count += 1
        elif result == -1:
            self.p1.feedReward(-2)
            self.p2.feedReward(2)
            self.loss_count += 1
        else:
            self.p1.feedReward(0.2)
            self.p2.feedReward(0.2)
            self.draw_count += 1

    def reward(self):
        self.board = np.zeros((3, 3))
        self.end = False
        self.place_symbol = 1

    def reset(self):
        self.board = np.zeros((3, 3))
        self.end = False
        self.place_symbol = 1

    def play(self, rounds):
        for i in range(rounds):
            if (i > 0) and (i % (rounds / 10) == 0):
                print(f'{(i / rounds) * 100}% done')
                print(f'winrate: {self.win_count / i}')
                print(f'lossrate: {self.loss_count / i}')
                print(f'drawrate: {self.draw_count / i}')
            self.place_symbol = random.choice([1,-1])
            while not self.end:
                if self.place_symbol == 1:
                    placeable = self.available_spots()
                    p1_action = self.p1.chooseAction(placeable, self.board, self.place_symbol)
                    self.updateState(p1_action)
                    hash = self.get_Hash()
                    self.p1.addState(hash)
                    win = self.winner()
                else:
                    placeable = self.available_spots()
                    p2_action = self.p2.chooseAction(placeable, self.board, self.place_symbol)
                    self.updateState(p2_action)
                    hash = self.get_Hash()
                    self.p2.addState(hash)
                    win = self.winner()
                if win is not None:  # did player 1 win after their move?
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

class Agent:
    def __init__(self, name, exp_rate=0.3, lr=0.2, decay_gamma=0.9):
        self.name = name
        self.exp_rate = exp_rate
        self.lr = lr
        self.decay_gamma = decay_gamma
        self.states = []
        self.state_values = {}


    def get_Hash(self, board):
        return str(board.flatten())  # gamestate ID

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            index = np.random.choice(len(positions))
            action = tuple(positions[index])
        else:
            # take greedy action
            value_max = -1 * float("inf")
            for p in positions:
                next_board = current_board.copy()
                next_board[tuple(p)] = symbol
                next_boardHash = self.get_Hash(next_board)
                value = 0 if self.state_values.get(next_boardHash) is None else self.state_values.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = tuple(p)
        return action

        # append a hash state

    def addState(self, state):
        self.states.append(state)

    def feedReward(self, reward):
        for state in reversed(self.states):
            if self.state_values.get(state) is None:
                self.state_values[state] = 0
            self.state_values[state] += self.lr * (self.decay_gamma * reward - self.state_values[state])
            reward = self.state_values[state]

    def reset(self):
        self.states = []

    def save_states(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.state_values, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.state_values = pickle.load(fr)
        fr.close()


if __name__ == "__main__":
    p1 = Agent("Player1", exp_rate=0.1)
    p2 = Agent("Player2", exp_rate=0.1)

    p1.loadPolicy("policy_Player1")
    p2.loadPolicy("policy_Player2")
    game = Game(p1, p2)
    print("start training...")
    game.play(20000)
    print("done!")
    p1.save_states()
    p2.save_states()

