import matplotlib.pyplot as plt
import numpy as np


class GBM:
    def __init__(self) -> None:
        #  \mu is responsible for ev / overall direction -> drift
        #  \s is responsible for the noise -> volatility
        self.time_horizon = 252 #252 trading days in a year
        self.delta_t = 1
        self.mu = 0.05/252 #5% annual returned scaled by number of trading days in a year
        self.sigma = 0.01
        self.init_value = 150
        
    def randomWalk(self):
        x = np.linspace(0,self.time_horizon,self.time_horizon)
        y = np.zeros(self.time_horizon)
        y[0] = self.init_value

        for i in range(1,self.time_horizon):
            y[i] = y[i-1] * np.exp(
                (self.mu - 0.5 * self.sigma**2) * self.delta_t + self.sigma*np.sqrt(self.delta_t)*np.random.normal(0,1)
            )

        return y

    def runGBMsim(self,n_paths):
        self.price_paths = []
        for i in range(n_paths):
            random_walk = self.randomWalk()
            self.price_paths.append(random_walk)

    def display(self):
        if len(self.price_paths) == 0:
            print('ERROR > No Price Paths to be Displayed')
            return 
        
        fig,ax = plt.subplots()
        ax.axhline(y=self.init_value,color='red',linestyle='--')

        for path in self.price_paths:
            plt.plot(path,color='gray')

        plt.show()

if __name__ == '__main__':
    gbm_runner = GBM()
    gbm_runner.runGBMsim(1)
    gbm_runner.display()