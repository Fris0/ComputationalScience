import paramsweep
import numpy as np

np.set_printoptions(threshold=np.inf)  # Allow for longer array outputs than the default.

from ca2 import CASim
mysim = CASim()

REPETITION = 3

# Simulation with random start state.
with open(f"random_result.csv", 'a') as fd:
    
    for i in range(256):
        cycles_per_rule = []

        for j in range(REPETITION):
            result_for_rule = paramsweep.paramsweep(mysim, repetitions=1,
                                           param_space={'width': 50, 'height': 10000, 'rule': i, 'random': True},
                                           measure_attrs=['config'])
            tracker = {}
    
            for idx, row in enumerate(result_for_rule):
                try:
                    if np.array_equal(row, result_for_rule[idx + 1]):
                       break
                    else:
                        if str(row) not in tracker.keys():
                            tracker[str(row)] = idx
                        else:
                            cycles_per_rule.append(idx - tracker[str(row)])
                            tracker[str(row)] = idx
                except:
                    continue
        
        if cycles_per_rule:
            fd.write(f"{np.mean(cycles_per_rule)},")
        else:
            fd.write(f"0,")