import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

class Engine:
    def __init__(self) -> None:
        self.transition_matrix = []
        self.state_variables = []
        self.n_states = 3
        self.createTransitionMatrix()
        # Start in a defined state (e.g., state 0) or random
        self.current_state = random.randint(0,self.n_states-1) 
        self.initialiseStateVariables()
        self.y = []
        self.state_history = []

    def createTransitionMatrix(self):
        state_stickiness = (0.8, 0.8, 0.8)

        for i, s in enumerate(state_stickiness):
            state_change_prob = (1 - s) / (self.n_states - 1) # More general
            state_transition = np.full((self.n_states), state_change_prob)
            state_transition[i] = s
            self.transition_matrix.append(state_transition)

        self.transition_matrix = np.array(self.transition_matrix)

    def moveToNextState(self):
        # Removed print statements for cleaner simulation
        cum_probs = np.cumsum(self.transition_matrix, axis=1)
        target_cum_probs = cum_probs[self.current_state]
        rand_val = np.random.rand()
        for i, x in enumerate(target_cum_probs):
            if rand_val <= x:
                self.current_state = int(i)
                break

    def initialiseStateVariables(self):
        # each state needs to have a sigma - vol - and mu - drift - values
        self.state_variables = np.array([
            # [annual_mu, annual_sigma]
            [0.15, 0.04],  # State 0: Calm bull
            [-0.1, 0.1],  # State 1: Crisis bear
            [0.075, 0.06],  # State 2: Weak calm bull
        ])

    def randomWalk(self, time_horizon, init_value):
        delta_t = 1 / 252  

        self.y = np.zeros(time_horizon)
        self.state_history = np.zeros(time_horizon, dtype=int)
        self.y[0] = init_value
        self.state_history[0] = self.current_state

        for i in range(1, time_horizon):
            mu, sigma = self.state_variables[self.current_state]
            self.y[i] = self.y[i-1] * np.exp(
                (mu - 0.5 * sigma**2) * delta_t
                + sigma * np.sqrt(delta_t) * np.random.normal(0, 1)
            )

            self.state_history[i] = self.current_state

            self.moveToNextState()

    def display(self):
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot price
        color = 'tab:blue'
        ax1.set_xlabel('Time (Days)')
        ax1.set_ylabel('Price', color=color)
        ax1.plot(self.y, color=color, label='Price')
        ax1.tick_params(axis='y', labelcolor=color)

        # ax2 = ax1.twinx()
        # color = 'tab:red'
        # ax2.set_ylabel('Market State', color=color, rotation=-90, labelpad=15)
        # ax2.plot(self.state_history, color=color, label='State', 
        #          linestyle='--', drawstyle='steps-post')
        # ax2.tick_params(axis='y', labelcolor=color)

        
        fig.tight_layout()
        plt.title('GBM with State Switching')
        plt.show()

    def saveData(self):
        save_location = 'data.csv'
        data = {'Price':self.y,
                'State':self.state_history}
        df = pd.DataFrame(data)
        df.to_csv(save_location)


if __name__ == '__main__':
    print('Starting Sim Engine')
    sim_engine = Engine()
    sim_engine.randomWalk(2520, 150)
    sim_engine.saveData()
    sim_engine.display()