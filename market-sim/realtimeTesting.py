import random
from re import X
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import init, Fore, Back, Style
import os
import inquirer
import importlib
import time
import multiprocessing


# Look at principle component analysis
#some MIT linear algebra course


init(autoreset=True)

stock_params_dict = {
    "Blue-Chip / Stable":    [ [0.09, 0.20], [-0.02, 0.35] ],
    "Tech Growth":           [ [0.18, 0.30], [-0.15, 0.50] ],
    "Defensive / Utility":   [ [0.07, 0.18], [0.01, 0.28] ],
    "Cyclical / Industrial": [ [0.14, 0.28], [-0.20, 0.45] ],
    "Speculative / Biotech": [ [0.30, 0.55], [-0.40, 0.80] ],
    "Financial / Bank":      [ [0.11, 0.25], [-0.25, 0.55] ],
    "Aggressive Growth":     [ [0.22, 0.40], [-0.30, 0.65] ],
    "Commodity / Energy":    [ [0.16, 0.38], [-0.12, 0.48] ],
    "Stable Dividend":       [ [0.08, 0.19], [0.00, 0.30] ],
    "Broad Market ETF":      [ [0.10, 0.17], [-0.10, 0.32] ],
    "Emerging Market":       [ [0.25, 0.45], [-0.35, 0.70] ],
    "Real Estate (REIT)":    [ [0.09, 0.22], [-0.05, 0.38] ],
    "Small-Cap Value":       [ [0.15, 0.28], [-0.22, 0.45] ],
    "International Developed ETF": [ [0.08, 0.19], [-0.12, 0.33] ],
    "Hyper-Growth / Meme Stock": [ [0.50, 0.80], [-0.60, 1.20] ],
    "Pharmaceutical (Stable)": [ [0.12, 0.23], [-0.05, 0.36] ],
    "Consumer Staples":      [ [0.06, 0.15], [0.01, 0.25] ],
    "Semiconductor (Cyclical)": [ [0.28, 0.48], [-0.30, 0.60] ],
    "Precious Metal (Gold)": [ [0.05, 0.20], [-0.01, 0.30] ],
    "SaaS (Software)":       [ [0.26, 0.42], [-0.35, 0.65] ]
}

single_stable = {
    'stable' : [[0.2,0.01],[0.2,0.01]]
}

class stockSimulation:
    def __init__(self,init_value=150,state_parameters=[[0.2,0.05],[-0.1,0.025]]) -> None:
        self.init_value = init_value
        self.y = [self.init_value]
        self.state_parameters = state_parameters #parameters are annualised
        
        self.initaliseTransitionMatrix()

        self.n_states = len(self.state_parameters)
        self.current_state = random.randint(0,self.n_states-1)
        self.state_history = [self.current_state]

    def walk(self,n_days):
        mu,sigma = self.state_parameters[self.current_state]

        delta_t = 1/252 # scale to be annualised

        #perform a single step
        for i in range(n_days):
            new_y = self.y[-1] * np.exp(
                (mu - 0.5 * sigma**2) * delta_t
                + sigma * np.sqrt(delta_t) * np.random.normal(0,1)
            )

            self.y.append(new_y)
            self.state_history.append(self.current_state)

            self.transitionStates()

    def transitionStates(self):
        cur_state_switch_probs = self.transitionMatrix[self.current_state]
        cum_probs = np.cumsum(cur_state_switch_probs)
        rand_val = np.random.rand()
        for i,x in enumerate(cum_probs):
            if rand_val<=x:
                self.current_state = i
                break

    def initaliseTransitionMatrix(self):
        self.transitionMatrix = np.array([
            [0.9,0.1],
            [0.1,0.9]
        ])
        

class Market():
    def __init__(self,stock_params,market_size,name) -> None:
        self.name = name
        self.universe = {}
        for i in range(market_size):
            self.universe[f'stock_{i}'] = stockSimulation(150,stock_params)

    def walk(self,n_days):
        for key in self.universe:
            self.universe[key].walk(n_days)

    def getPriceAnalytics(self,target_stock):
        stock_history = self.universe[target_stock].y
        if len(stock_history)<2:
            return None
        start_val = stock_history[0]
        current_val = stock_history[-1]
        hold_val_change = current_val-start_val
        hold_pct_change = (hold_val_change/start_val)*100
        
        dod_val_change = current_val-stock_history[-2]
        dod_pct_change = (dod_val_change/stock_history[-2])*100

        return (float(hold_val_change),float(hold_pct_change),float(dod_val_change),float(dod_pct_change))

class AlgoTrading:
    def __init__(self,market,trading_func) -> None:
        self.market = market
        self.universe = self.market.universe
        self.trading_func = trading_func
        self.capital = 100000
        self.starting_capital = 100000
        self.capital_history = [self.capital]

        self.initialisePositions()
        
    def initialisePositions(self):
        self.positions = {}
        for stock in self.universe:
            self.positions[stock] = None

    def singleDayStep(self):
        self.market.walk(1)
        if self.capital>0:    
            signals = {} 
            for stock in self.universe:
                if len(self.universe[stock].y) > 50:
                    signal = self.trading_func(self.universe[stock].y)   
                    signals[stock] = signal 

            self.handleSignals(signals)

        self.capital_history.append(self.capital)

    def handleSignals(self, signals: dict): # Expects a dictionary
        unrealised_orders = []
        
        for stock in self.universe:
            signal = signals.get(stock) 

            if signal == 0:
                if self.positions[stock] is not None:
                    self.sell(stock)
            elif signal == -1:
                buy_price = self.universe[stock].y[-1]
                unrealised_orders.append((stock, -1, buy_price))
            elif signal == 1:
                buy_price = self.universe[stock].y[-1]
                unrealised_orders.append((stock, 1, buy_price))

        self.realiseBuyOrders(unrealised_orders)

    def realiseBuyOrders(self, unrealised_orders):
        max_capital_allocation = 0.02
        
        for order in unrealised_orders:
            stock, indicator, buy_price = order
            

            if self.positions[stock] is not None and self.positions[stock][0] != indicator:
                self.sell(stock)
                
            position_size = self.capital * max_capital_allocation
            
            if self.capital < position_size or self.capital <= 0:
                continue
                        
            self.positions[stock] = (indicator, buy_price, position_size)
            self.capital -= position_size    



    #create the buy order, then add it to a list of newly developed orders
    #then once all stocks have been analysed size the positions based on the newly developed orders

    def sell(self,stock):
        order = self.positions[stock]
        buy_price = order[1]
        position_size = order[2]
        current_price = self.universe[stock].y[-1]

        if order[0] == 1: #long position
            stock_val_change = current_price-buy_price                   

        elif order[0] == -1: #short position
            stock_val_change = buy_price-current_price

        else:
            return

        position_mult = 1 + (stock_val_change/buy_price)
        sale_val = position_size*position_mult
        self.capital+=sale_val

        self.positions[stock] = None

def handleLiveTesting(multi_market_params, algo_func):
    test_start_time = time.time()
    time_horizon = 1008

    market_size = 30    

    live_testers = {}
    for market_name in multi_market_params:
        cur_market = Market(multi_market_params[market_name], market_size, market_name)
        live_testers[market_name] = AlgoTrading(cur_market, algo_func)

    COL_WIDTH = 20
    NAME_WIDTH = 30

    n_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=n_cores)

    try:
        for i in range(time_horizon):
            row_buffer = []
            
            parallel_args = []
            for market_name, tester_obj in live_testers.items():
                parallel_args.append((tester_obj, market_name, COL_WIDTH, NAME_WIDTH))
            
            header = (
                f"{'Market':<{NAME_WIDTH}}"
                f"{'Balance ($)':>{COL_WIDTH}}"
                f"{'Total PnL ($)':>{COL_WIDTH}}"
                f"{'Total PnL (%)':>{COL_WIDTH}}"
                f"{'Daily PnL ($)':>{COL_WIDTH}}"
            )
            row_buffer.append(header)
            row_buffer.append("-" * len(header)) 


            results = pool.starmap(get_pnl_row, parallel_args) #error being generated on this line?


            for row_string, updated_tester in results:
                row_buffer.append(row_string)
                live_testers[updated_tester.market.name] = updated_tester

            os.system('clear')
            print(f"Day: {i+1}/{time_horizon} | Testing > {algo_func.__module__.split('.')[1]}")
            print("\n".join(row_buffer))
            
    finally:
        pool.close()
        pool.join()

    print(f'Took > {(time.time()-test_start_time):.5f}s to Backtest')

def get_pnl_row(market_algorithm, sector, COL_WIDTH, NAME_WIDTH):
    market_algorithm.singleDayStep()

    starting_cap = market_algorithm.starting_capital
    current_cap = market_algorithm.capital
    
    if len(market_algorithm.capital_history) >= 2:
        previous_cap = market_algorithm.capital_history[-2]
    else:
        previous_cap = starting_cap

    total_pnl = current_cap - starting_cap
    total_pnl_pct = (total_pnl / starting_cap) * 100

    daily_pnl = current_cap - previous_cap

    #get the position exposure
    
    exposure = 0

    for stock in market_algorithm.universe:
        if market_algorithm.positions[stock] == None:
            exposure += 0

        else:
            exposure += market_algorithm.positions[stock][2]*market_algorithm.positions[stock][0]

    row_string = (
        f"{sector:<{NAME_WIDTH}}"
        f"{Fore.WHITE}{current_cap:>{COL_WIDTH},.2f}" 
        f"{Fore.RED if total_pnl < 0 else Fore.GREEN}{total_pnl:>{COL_WIDTH},.2f}"
        f"{Fore.RED if total_pnl_pct < 0 else Fore.GREEN}{total_pnl_pct:>{COL_WIDTH}.2f}%"
        f"{Fore.RED if daily_pnl < 0 else Fore.GREEN}{daily_pnl:>{COL_WIDTH},.2f}"
        #print positon exposure

        f"{Style.RESET_ALL}"
    )
    
    return row_string,market_algorithm

if __name__ == '__main__':

    algo_dir = 'algos'
    algo_choices = [
        f.replace('.py', '') 
        for f in os.listdir(algo_dir) 
        if f.endswith('.py') and f != '__init__.py'
    ]

    algo_q = [
        inquirer.List(
            'Algorithm',
            message='Select a Trading Algorithm',
            choices = algo_choices 
        )
    ]
    algo_dict = inquirer.prompt(algo_q)

    try:
        chosen_algo_name = algo_dict['Algorithm']
        module_path = f"{algo_dir}.{chosen_algo_name}"
        print(f"Loading module: {module_path}")
        chosen_module = importlib.import_module(module_path)
        algo_func = getattr(chosen_module, 'runAnalysis')

    except ImportError:
        print(f"Error: Could not import {module_path}.")
        print("Check that the file exists and has no syntax errors.")
        exit()
    except AttributeError:
        print(f"Error: The file {chosen_algo_name}.py does not have a 'runAnalysis' function.")
        exit()

    handleLiveTesting(single_stable,algo_func)