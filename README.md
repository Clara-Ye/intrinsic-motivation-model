# Course project for 85-412: Cognitive Modellling

The task file is `submarine.py` and the model file is `submarine-model.lisp`.

After connecting to an ACT-R session, call
~~~~
submarine.run_experiment(n)
~~~~
to run `n` simulated subjects for each experiment condition. For reasonable running time and stability, the recommeneded sample size is around 50, but see the comment at the bottom.

The function also takes 3 optional arguments:
* `progress`: if an integer `p`, then the running progress would be printed every `p` iterations. Default is `False`, i.e., no progress is printed.
* `data`: if `True`, prints the numerical summary of the simulations, including correlation, mean deviation, and side by side comparison of human and model average results. Default is `True`.
* `plot`: if `True`, plots human and model average results with standard error bars in line graphs.

It is recommended to set at least on of `data` and `plot` to `True`.

There are 2 additional functions that can be used for unit-testing purpose:
* `submarine.run_game(size, time)`: runs a single simulated subject through a full game, with specified `size` (a float between 0 and 1, exclusive) and `time` (a positive integer or float).
* `submarine.run_trial(size, time)`: runs a single simulated subject through a single trial in the game, with specified `size` and `time`.

*I do not know how to suppress warning messages. Setting `:model-warnings nil` and `:style-warnings nil` in the model does not do anything. Calling `actr.hide_output()` in `submarine.py` hides warning messages in the python terminal, but not the ACT-R terminal. This might be part of the reason why running the code takes extremely long for large values of `n`.*