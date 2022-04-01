
from mesa import Agent
from bank_reserves.random_walk import RandomWalker
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
from mesa.batchrunner import batch_run
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


all_wealth = []
  
"""
If you want to perform a parameter sweep, call batch_run.py instead of run.py.
For details see batch_run.py in the same directory as run.py.
"""

# Start of datacollector functions
class Bank(Agent):
    def __init__(self, unique_id, model, reserve_percent=50):
        # initialize the parent class with required parameters
        super().__init__(unique_id, model)
        # for tracking total value of loans outstanding
        self.bank_loans = 0
        """percent of deposits the bank must keep in reserves - this is a
           UserSettableParameter in server.py"""
        self.reserve_percent = reserve_percent
        # for tracking total value of deposits
        self.deposits = 0
        # total amount of deposits in reserve
        self.reserves = (self.reserve_percent / 100) * self.deposits
        # amount the bank is currently able to loan
        self.bank_to_loan = 1000
        self.saved_taxes = 0

    """update the bank's reserves and amount it can loan;
       this is called every time a person balances their books
       see below for Person.balance_books()"""

    def bank_balance(self):
       self.reserves = (self.reserve_percent / 100) * self.deposits
       if self.bank_to_loan > 300:
           self.bank_to_loan = self.deposits - (self.reserves + self.bank_loans)
       else:
           self.bank_to_loan = self.deposits - (self.reserves + self.bank_loans)
           self.bank_to_loan += int(0.75*self.saved_taxes)
           self.saved_taxes = 0



# subclass of RandomWalker, which is subclass to Mesa Agent
class Person(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, bank, rich_threshold, taxation):
        # init parent class with required parameters
        super().__init__(unique_id, pos, model, moore=moore)
        # the amount each person has in savings
        self.savings = 0
        # total loan amount person has outstanding
        self.loans = 0
        """start everyone off with a random amount in their wallet from 1 to a
           user settable rich threshold amount"""
        self.wallet = self.random.randint(1, rich_threshold + 1)
        # savings minus loans, see balance_books() below
        self.wealth = 0
        # person to trade with, see do_business() below
        self.customer = 0
        # person's bank, set at __init__, all people have the same bank in this model
        self.bank = bank
        #tributo governo
        self.taxation = taxation

    def do_business(self):
        """check if person has any savings, any money in wallet, or if the
        bank can loan them any money"""
        if self.savings > 0 or self.wallet > 0 or self.bank.bank_to_loan > 0:
            # create list of people at my location (includes self)
            my_cell = self.model.grid.get_cell_list_contents([self.pos])
            # check if other people are at my location
            if len(my_cell) > 1:
                # set customer to self for while loop condition
                customer = self
                while customer == self:
                    """select a random person from the people at my location
                    to trade with"""
                    customer = self.random.choice(my_cell)
                # 50% chance of trading with customer
                if self.random.randint(0, 1) == 0:
                    # 50% chance of trading $5
                    #fosse um inteiro interativo na tela
                    random_number = self.random.randint(0, 4)
                    if random_number== 0:
                        # give customer $5 from my wallet (may result in negative wallet)
                        customer.wallet += 10
                        self.wallet -= 10
                    # 50% chance of trading $2
                    elif random_number == 2:
                        customer.wallet += 20
                        self.wallet -= 20
                    elif random_number == 3:
                        customer.wallet += 50
                        self.wallet -= 50
                    else:
                        # give customer $10 from my wallet (may result in negative wallet)
                        customer.wallet += 100
                        self.wallet -= 100

    def balance_books(self):
        # check if wallet is negative from trading with customer
        if self.wallet < 0:
            # if negative money in wallet, check if my savings can cover the balance
            if self.savings >= (self.wallet * -1):
                """if my savings can cover the balance, withdraw enough
                money from my savings so that my wallet has a 0 balance"""
                self.withdraw_from_savings(self.wallet * -1)
            # if my savings cannot cover the negative balance of my wallet
            else:
                # check if i have any savings
                if self.savings > 0:
                    """if i have savings, withdraw all of it to reduce my
                    negative balance in my wallet"""
                    self.withdraw_from_savings(self.savings)
                # record how much money the bank can loan out right now
                temp_loan = self.bank.bank_to_loan
                """check if the bank can loan enough money to cover the
                   remaining negative balance in my wallet"""
                if temp_loan >= (self.wallet * -1):
                    """if the bank can loan me enough money to cover
                    the remaining negative balance in my wallet, take out a
                    loan for the remaining negative balance"""
                    self.take_out_loan(self.wallet * -1)
                else:
                    """if the bank cannot loan enough money to cover the negative
                    balance of my wallet, then take out a loan for the
                    total amount the bank can loan right now"""
                    self.take_out_loan(temp_loan)
        else:
            """if i have money in my wallet from trading with customer, deposit
            it to my savings in the bank"""
            self.deposit_to_savings(self.wallet)
        # check if i have any outstanding loans, and if i have savings
        if self.loans > 0 and self.savings > 0:
            # check if my savings can cover my outstanding loans
            if self.savings >= self.loans:
                # payoff my loans with my savings
                self.withdraw_from_savings(self.loans)
                self.repay_a_loan(self.loans)
            # if my savings won't cover my loans
            else:
                # pay off part of my loans with my savings
                self.withdraw_from_savings(self.savings)
                self.repay_a_loan(self.wallet)
        # calculate my wealth
        self.wealth = self.savings - self.loans

    # part of balance_books()
    def deposit_to_savings(self, amount):
        # take money from my wallet and put it in savings
        self.wallet -= amount
        self.savings += amount
        # increase bank deposits
        self.bank.deposits += amount

    # part of balance_books()
    def withdraw_from_savings(self, amount):
        # put money in my wallet from savings
        self.wallet += amount
        self.savings -= amount
        # decrease bank deposits
        self.bank.deposits -= amount
        
        
    # part of balance_books()
    def repay_a_loan(self, amount):
        """# take money from my wallet to pay off all or part of a loan
        if (int(amount * self.taxation / 100))< 1:
            self.loans -= amount + 1
            self.wallet -= amount 
            # increase the amount the bank can loan right now
            self.bank.bank_to_loan += amount - 1 
            # decrease the bank's outstanding loans
            self.bank.bank_loans -= amount - 1
            
            self.bank.saved_taxes += 1
        else:"""
        self.loans -= amount + int(amount * self.taxation / 100)
        self.wallet -= amount 
        # increase the amount the bank can loan right now
        self.bank.bank_to_loan += amount - int(amount * self.taxation / 100)
        # decrease the bank's outstanding loans
        self.bank.bank_loans -= amount - int(amount * self.taxation / 100)
        
        self.bank.saved_taxes += int(amount * self.taxation / 100)

    # part of balance_books()
    def take_out_loan(self, amount):
        """borrow from the bank to put money in my wallet, and increase my
        outstanding loans
        if (int(amount * self.taxation / 100))< 1:
            self.loans += amount + 1
            self.wallet += amount 
            # decresae the amount the bank can loan right now
            self.bank.bank_to_loan -= amount
            # increase the bank's outstanding loans
            self.bank.bank_loans += amount + 1
            self.bank.saved_taxes += 1
        else:"""
        self.loans += amount + int(amount * self.taxation / 100)
        self.wallet += amount 
        # decresae the amount the bank can loan right now
        self.bank.bank_to_loan -= amount
        # increase the bank's outstanding loans
        self.bank.bank_loans += amount + int(amount * self.taxation / 100)
        self.bank.saved_taxes += int(amount * self.taxation / 100)
            


    # step is called for each agent in model.BankReservesModel.schedule.step()
    def step(self):
        # move to a cell in my Moore neighborhood
        self.random_move()
        # trade
        self.do_business()
        # deposit money or take out a loan
        self.balance_books()
        # update the bank's reserves and the amount it can loan right now
        self.bank.bank_balance()

def get_num_rich_agents(model):
    """return number of rich agents"""

    rich_agents = [a for a in model.schedule.agents if a.savings > model.rich_threshold]
    return len(rich_agents)


def get_num_poor_agents(model):
    """return number of poor agents"""

    poor_agents = [a for a in model.schedule.agents if a.loans > 25]
    return len(poor_agents)


def get_num_mid_agents(model):
    """return number of middle class agents"""

    mid_agents = [
        a
        for a in model.schedule.agents
        if a.loans < 25 and a.savings < model.rich_threshold
    ]
    return len(mid_agents)
  

def get_total_savings(model):
    """sum of all agents' savings"""

    agent_savings = [a.savings for a in model.schedule.agents]
    # return the sum of agents' savings
    return np.sum(agent_savings)


def get_total_wallets(model):
    """sum of amounts of all agents' wallets"""

    agent_wallets = [a.wallet for a in model.schedule.agents]
    # return the sum of all agents' wallets
    return np.sum(agent_wallets)


def get_total_money(model):
    # sum of all agents' wallets
    wallet_money = get_total_wallets(model)
    # sum of all agents' savings
    savings_money = get_total_savings(model)
    # return sum of agents' wallets and savings for total money
    return wallet_money + savings_money


def get_total_loans(model):
    # list of amounts of all agents' loans
    agent_loans = [a.loans for a in model.schedule.agents]
    # return sum of all agents' loans
    return np.sum(agent_loans)

def plt_value(model):
    agent_wealth = [a.wealth for a in model.schedule.agents]
    all_wealth.append(agent_wealth)
        

class BankReserves(Model):
    """
    This model is a Mesa implementation of the Bank Reserves model from NetLogo.
    It is a highly abstracted, simplified model of an economy, with only one
    type of agent and a single bank representing all banks in an economy. People
    (represented by circles) move randomly within the grid. If two or more people
    are on the same grid location, there is a 50% chance that they will trade with
    each other. If they trade, there is an equal chance of giving the other agent
    $5 or $2. A positive trade balance will be deposited in the bank as savings.
    If trading results in a negative balance, the agent will try to withdraw from
    its savings to cover the balance. If it does not have enough savings to cover
    the negative balance, it will take out a loan from the bank to cover the
    difference. The bank is required to keep a certain percentage of deposits as
    reserves and the bank's ability to loan at any given time is a function of
    the amount of deposits, its reserves, and its current total outstanding loan
    amount.
    """

    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    """init parameters "init_people", "rich_threshold", and "reserve_percent"
       are all UserSettableParameters"""

    def __init__(
        self,
        height=grid_h,
        width=grid_w,
        init_people=10,
        rich_threshold=100,
        reserve_percent=10,
        taxation = 10
    ):
        self.height = height
        self.width = width
        self.init_people = init_people
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        # rich_threshold is the amount of savings a person needs to be considered "rich"
        self.rich_threshold = rich_threshold
        self.reserve_percent = reserve_percent
        self.taxation = taxation
        # see datacollector functions above
        self.datacollector = DataCollector(
            model_reporters={
                "Rich": get_num_rich_agents,
                "Poor": get_num_poor_agents,
                "Middle Class": get_num_mid_agents,
                "Savings": get_total_savings,
                "Wallets": get_total_wallets,
                "Money": get_total_money,
                "Loans": get_total_loans,
                "Value": plt_value,
            },
            agent_reporters={"Wealth": "wealth"}
        )

        # create a single bank for the model
        self.bank = Bank(1, self, self.reserve_percent)

        # create people for the model according to number of people set by user
        for i in range(self.init_people):
            # set x, y coords randomly within the grid
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            p = Person(i, (x, y), self, True, self.bank, self.rich_threshold, self.taxation)
            # place the Person object on the grid at coordinates (x, y)
            self.grid.place_agent(p, (x, y))
            # add the Person object to the model schedule
            self.schedule.add(p)

        self.running = True
        self.datacollector.collect(self)
    

    
    def step(self):
        # tell all the agents in the model to run their step function
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        #self.render()
        #self deposits
          
            

    def run_model(self):
        for i in range(self.run_time): 
            self.step()
           # plt.show()
            
            
            
if __name__ == "__main__":
    variable_params={
        "width": [20],
        "height": [20],
        "init_people":  [50, 100,150],
        "rich_threshold" :  [100 ,200],
        "reserve_percent" :  [10, 20, 30],
        "taxation" : [10, 20, 30]
    }
    
    
    batch_runner = batch_run(
        BankReserves,
        parameters= variable_params,
        iterations= 1,
        max_steps= 100,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,

            
    )
    
    results_df = pd.DataFrame(batch_runner)
    
    now = datetime.now().strftime("%Y-%m-%d")
    file_name_suffix =  ("_bank_reserve_"+now )
    
    plt.hist(all_wealth)
    plt.show()
    #results_df.to_csv("analise-dt3-1it-100steps"+file_name_suffix+".csv")

    
  
        
