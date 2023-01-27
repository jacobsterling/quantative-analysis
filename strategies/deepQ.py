import backtrader as bt
import numpy as np
from pathlib import Path

import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from collections import deque


AGENT_path = Path(r"F://AiQuant/models/deepQ.h5")


class DeepQAgent:
    memory = deque(maxlen=2000)
    gamma = 0.95  # discount rate
    epsilon = 1.0  # exploration rate
    action_space = 3  # hold = 0, buy = 1, sell = 2

    model = Sequential()

    def __init__(self, state_space=5):  # time open high low close

        # Neural Net for Deep-Q learning Model
        self.model.add(Dense(24, input_dim=state_space, activation='relu'))
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(self.action_space, activation='linear'))
        self.model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):

        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_space)

        act_values = self.model.predict(state)

        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size=32):

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                    np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > 0.01:  # min epsilon
            self.epsilon *= 0.995  # epsilon decay

    def load(self):
        self.model.load_weights(AGENT_path)

    def save(self):
        self.model.save_weights(AGENT_path)


class DeepQ(bt.Strategy):

    params = {'percents': 1}  # risk per trade in %

    model = DeepQAgent()

    entry_state = None

    def __init__(self):
        try:
            self.model.load()
        except FileNotFoundError:
            pass

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if not self.position:  # if exited the market
                next_state = [order.executed.dt, self.data.open[0], self.data.high[0],
                              self.data.low[0], self.data.close[0]]

                self.model.remember(self.entry_state, -1 if order.isbuy()
                                    else 1, order.executed.pnl, next_state, False)

                self.entry_state = None

            # else:
                # print(f'{  "Long" if order.isbuy() else "Short" } Position Opened @price: {order.executed.price}')

    def next(self):

        # Initialize the state
        state = [self.data.datetime.dt(), self.data.open[0],
                            self.data.high[0], self.data.low[0], self.data.close[0]]

        # Choose an action
        action = self.model.act(state)

        if action > 0:  # if action is to not hold

            if action == 1:  # if action is to buy
            
                if self.position.size < 0:
                    # close if already short
                    self.close() 
                else:
                    self.entry_state = state
                    self.buy()

            elif action == 2:  # if action is to sell
                # close if already long
                
                if self.position.size > 0:
                    self.close() 
                else:
                    self.entry_state = state
                    self.sell()

    def stop(self):
        self.model.save()
