"""
Author: Mark Jansen (13385569)

Summary: 
This program functions as a specific cellular automaton, and uses the pycx
module to show the states in between steps. Through the GUI you can change the
step size, interval, rule for the configurations and
1D-celullar automata characteristics.

Usage:
- Make sure Python version 3.10 or higher is installed.
- Run the file

or

- Use the paramsweep script to capture the data;
- Process the return values instantly;
- Or use the csv option in paramsweep.

Look at simulate_random.py and simulate.py how paramsweep was implemented.
"""


import numpy as np
from model import Model
from random import seed


def decimal_to_base_k(n, k):
    """
    Converts a given decimal (i.e. base-10 integer) to a list containing the
    base-k equivalant.

    For example, for n=34 and k=3 this function should return [1, 0, 2, 1].
    """

    number = []
    while n != 0:
        number.append(n % k)
        n = n // k

    return number[::-1]


def base_k_to_decimal(values, k):
    """
    Converts a given base_k value of type list to base_10

    val = list of state in base_k
    k   = base of list in int.

    Output: base_10 integer.
    """

    count = 0

    for idx, val in enumerate(values[::-1]):
        count += val * (k ** idx)
    
    return (int(count))


class CASim(Model):
    def __init__(self):
        Model.__init__(self)

        self.t = 0
        self.rule_set = []
        self.config = None

        self.make_param('r', 1)
        self.make_param('k', 2)
        self.make_param('width', 50)
        self.make_param('height', 50)
        self.make_param('rule', 30, setter=self.setter_rule)
        self.make_param('random', False)

    def setter_rule(self, val):
        """
        Setter for the rule parameter, clipping its value between 0 and the
        maximum possible rule number.
        """
        rule_set_size = self.k ** (2 * self.r + 1)
        max_rule_number = self.k ** rule_set_size
        return max(0, min(val, max_rule_number - 1))

    def build_rule_set(self):
        """
        Sets the rule set for the current rule.
        A rule set is a list with the new state for every old configuration.

        For example, for rule=34, k=3, r=1 this function should set rule_set to
        [0, ..., 0, 1, 0, 2, 1] (length 27). This means that for example
        [2, 2, 2] -> 0 and [0, 0, 1] -> 2.
        """
        rule_set_size = self.k ** (2 * self.r + 1)

        rule = decimal_to_base_k(self.rule, self.k)

        difference = rule_set_size - len(rule)
        padding = [0] * difference

        self.rule_set = padding + rule # Rule-set with padded 0's.

    def check_rule(self, inp):
        """
        Returns the new state based on the input states.

        The input state will be an array of 2r+1 items between 0 and k, the
        neighbourhood which the state of the new cell depends on.
        """
        rule_set_size = self.k ** (2 * self.r + 1) - 1
        base_dec = base_k_to_decimal(inp, self.k)
        return (self.rule_set[np.abs(base_dec - rule_set_size)])

    def setup_initial_row(self):
        """
        Returns an array of length `width' with the initial state for each of
        the cells in the first row. Values should be between 0 and k.
        """
        initial_array = None
        if self.random == True:
            seed()
            initial_array = np.random.randint(0, high=self.k, size=self.width)
        else:
            initial_array = np.zeros(self.width)
            initial_array[self.width // 2] = self.k - 1
        return initial_array

    def reset(self):
        """
        Initializes the configuration of the cells and converts the entered
        rule number to a rule set.
        """

        self.t = 0
        self.config = np.zeros([self.height, self.width])
        self.config[0, :] = self.setup_initial_row()
        self.build_rule_set()

    def draw(self):
        """
        Draws the current state of the grid.
        """

        import matplotlib
        import matplotlib.pyplot as plt

        plt.cla()
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.imshow(self.config, interpolation='none', vmin=0, vmax=self.k - 1,
                cmap=matplotlib.cm.binary)
        plt.axis('image')
        plt.title('t = %d' % self.t)

    def step(self):
        """
        Performs a single step of the simulation by advancing time (and thus
        row) and applying the rule to determine the state of the cells.
        """
        self.t += 1
        if self.t >= self.height:
            return True

        for patch in range(self.width):
            # We want the items r to the left and to the right of this patch,
            # while wrapping around (e.g. index -1 is the last item on the row).
            # Since slices do not support this, we create an array with the
            # indices we want and use that to index our grid.
            indices = [i % self.width
                    for i in range(patch - self.r, patch + self.r + 1)]
            values = self.config[self.t - 1, indices]
            self.config[self.t, patch] = self.check_rule(values)


if __name__ == '__main__':
    sim = CASim()
    from pycx_gui import GUI
    cx = GUI(sim)
    cx.start()
