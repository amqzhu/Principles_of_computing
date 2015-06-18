"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(30)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        #a time, an item that was bought at that time (or None), 
        #the cost of the item, and the total number of cookies produced by that time
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._time) + " Current Cookies: "+ str(self._current_cookies)+ " CPS: "+str(self._cps)+" Total Cookies: "+ str(self._total_cookies)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history_clone = self._history
        return history_clone

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cookies:
            time_left = 0.0
        else:
            time_left = (cookies - self._current_cookies)/self._cps
        
        return math.ceil(time_left)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._time += time
            self._current_cookies += time * self._cps
            self._total_cookies += time * self._cps
        
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time,item_name,float(cost),self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_info_clone = build_info.clone()
    
    clicker_state = ClickerState()
    
    while clicker_state.get_time() <= duration:
        clicker_cookies = clicker_state.get_cookies()
        clicker_cps = clicker_state.get_cps()
        clicker_history = clicker_state.get_history()
        time_left = duration - float(clicker_state.get_time())
        
        chosen_item = strategy(clicker_cookies, clicker_cps, clicker_history, time_left, build_info_clone)
        
        if chosen_item == None:
            break
        else:
            item_cost = float(build_info_clone.get_cost(chosen_item))
            item_cps = float(build_info_clone.get_cps(chosen_item))
            time_needed = math.ceil((item_cost - clicker_cookies) / clicker_cps)
            if (clicker_state.get_time() + time_needed) <= duration:
                clicker_state.wait(time_needed)
                clicker_state.buy_item(chosen_item, item_cost, item_cps)
                build_info_clone.update_item(chosen_item)
            else:
                break
    
    clicker_state.wait(duration - clicker_state.get_time())
    
    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    build_info_clone = build_info.clone()
    items_list = build_info_clone.build_items()
    cost_list = []
    
    for item in items_list:
        cost_list.append(build_info_clone.get_cost(item))
        
    cheap_cost = min(cost_list)
    
    items_dict = {}
    
    for item in items_list:
        items_dict[build_info_clone.get_cost(item)] = item
    
    cheap_item = items_dict[cheap_cost]
    
    return cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    build_info_clone = build_info.clone()
    items_list = build_info_clone.build_items()
    cost_list = []
    
    for item in items_list:
        cost_list.append(build_info_clone.get_cost(item))
        
    expensive_cost = max(cost_list)
    
    items_dict = {}
    
    for item in items_list:
        items_dict[build_info_clone.get_cost(item)] = item
    
    expensive_item = items_dict[expensive_cost]
    
    return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    build_info_clone = build_info.clone()
    items_list = build_info_clone.build_items()
    
    return random.choice(items_list)
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, strategy) 
    #state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

