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
from random import randint


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
        self.seed = 19  # This value is not reset for randomization reasons.
        self.rule_set = []
        self.config = None
        self.quiescent_state = 0

        self.make_param('langton', 1.0)
        self.make_param('r', 1)
        self.make_param('k', 2)
        self.make_param('width', 50)
        self.make_param('height', 50)
        self.make_param('random', False)

    def linear_congruential_gen(self, a, c, m):
        """
        Return a random integer between (0) and (m - 1).
        """
        self.seed = (a * self.seed + c) % m
        return (self.seed)

    def build_rule_set_langton(self):
        """
        Builds the rule-set with the walkthrough method.
        A rule set is a list with the new state for every old configuration.
        """
        rule_set_size = self.k ** (2 * self.r + 1)

        # Step 0: Obtain a random quiescent state.
        self.linear_congruential_gen(1664525, 1013904223, pow(2, 32))
        self.quiescent_state = randint(0, self.k - 1)

        # Step 1: Initialize rule_set to quiescent state.
        self.rule_set = [self.quiescent_state] * rule_set_size

        # Step 2: Set random tables to random state until Langton is met.
        measured_langton = 0
        while (measured_langton - self.langton):
            self.linear_congruential_gen(1664525, 1013904223, pow(2, 32))

            pick_size = max(1, int((self.langton - measured_langton)
                                   * rule_set_size))

            input_state = [randint(0, rule_set_size - 1)
                           for i in range(pick_size)]

            for rule in input_state:
                random_state = self.quiescent_state

                while (random_state == self.quiescent_state):
                    random_state = randint(0, self.k - 1)

                self.rule_set[rule] = random_state

            quiescent_count = self.rule_set.count(self.quiescent_state)
            measured_langton = ((rule_set_size - quiescent_count)
                                / rule_set_size)

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

        if self.random is True:
            seed(self.linear_congruential_gen(1664525, 1013904223, pow(2, 32)))
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

        rule_set_size = self.k ** (2 * self.r + 1)

        possible_langton_values = [i / rule_set_size
                                   for i in range(rule_set_size + 1)]

        if (self.langton in possible_langton_values):
            self.build_rule_set_langton()
        else:
            print("Invalid Langton Value")

    def draw(self):
        """
        Draws the current state of the grid.
        """

        import matplotlib
        import matplotlib.pyplot as plt

        plt.cla()

        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()

        plt.imshow(self.config, interpolation='none', vmin=0,
                   vmax=self.k - 1, cmap=matplotlib.cm.binary)
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
            # while wrapping around-
            # (e.g. index -1 is the last item on the row).
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
