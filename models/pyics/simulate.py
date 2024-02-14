import paramsweep
import numpy as np

np.set_printoptions(threshold=np.inf)  # Allow for longer array outputs than the default.

from ca2 import CASim
mysim = CASim()

# Simulation with default start state.
with open(f"temp.csv", 'a') as fd:  # Change file name, so you obtain sepperate .csv per experiment.
    
    for i in range(256):
        result_for_rule = paramsweep.paramsweep(mysim, repetitions=1,
                                       param_space={'width': 100, 'height': 1000, 'rule': i, 'random': False},
                                       measure_attrs=['config'])
        tracker = {}
        cycles_per_rule = []
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