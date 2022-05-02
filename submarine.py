import sys
sys.path.append("C:/Users/MSI-NB/Desktop/2022_Spring/85-412/ACT-R/tutorial/python")
import actr
import random
import numpy as np
import matplotlib.pyplot as plt

actr.load_act_r_model("ACT-R:project;intrinsic-motivation-model;submarine-model.lisp")

size_data = []
time_data = []
#fractions = [(1,10), (1,8),  (1,6),  (1,5),  (1,4), 
#             (3,10), (1,3),  (3,8),  (2,5),  (3,7), 
#             (1,2),  (3,5),  (5,8),  (2,3),  (7,10),
#             (3,4),  (4,5),  (5,6),  (7,8),  (9,10)]
fractions = [(1,4), (1,2), (3,4)]
ship_sizes = [0.04, 0.06, 0.08, 0.10, 0.16, 0.20, 0.24, 0.30, 0.40]
time_limits = [2, 3, 4, 5, 8, 10, 15, 30]
click_loc = None
end_choice = False
current_numer = None
current_fracline = None
current_denom = None

def respond_to_key_press(model, key):
    global end_choice
    end_choice = key

def respond_to_mouse_click(model, coord, finger):
    global click_loc
    click_loc = coord[0]

def model(numer, denom, size, time):
    global current_numer, current_fracline, current_denom
    if actr.visible_virtuals_available():

        # initial display
        window = actr.open_exp_window("Submarine Game", visible=True,
                                      width=500,height=300,x=500,y=300)
        actr.install_device(window)
        num_line = actr.add_line_to_exp_window(window,[50,150],[450,150],"blue")
        current_numer = actr.add_text_to_exp_window(window, str(numer), x=250, y=200)
        current_fracline = actr.add_text_to_exp_window(window, "-", x=250, y=210)
        current_denom = actr.add_text_to_exp_window(window, str(denom), x=250, y=220)

        # collects player attack
        actr.add_command("attack", respond_to_mouse_click, 
                         "Submarine task attack mouse click")
        actr.monitor_command("click-mouse", "attack")

        global click_loc
        click_loc = -1

        actr.run(time)
        actr.remove_items_from_exp_window(window,current_numer)
        actr.remove_items_from_exp_window(window,current_fracline)
        actr.remove_items_from_exp_window(window,current_denom)
        current_numer = current_fracline = current_denom = None

        actr.remove_command_monitor("click-mouse", "attack")
        actr.remove_command("attack")

        # checks and displays answer
        width_correct = size * (450-50)
        x_correct = 50 + (numer/denom)*(450-50)
        left_end = x_correct - width_correct/2
        right_end = x_correct + width_correct/2
        click_loc_trans = 50 + (click_loc-550)/(950-550) * (450-50)
        print(click_loc_trans, x_correct)

        if (left_end <= click_loc_trans) and (click_loc_trans <= right_end):
            ship_line = actr.add_line_to_exp_window(window,
                                                    [left_end,145],
                                                    [right_end,145],
                                                    "green")
        else:
            ship_line = actr.add_line_to_exp_window(window,
                                                    [left_end,145],
                                                    [right_end,145],
                                                    "red")

        # trial-end choice
        actr.add_command("end-response", respond_to_key_press, 
                         "Submarine task trial end key response")
        actr.monitor_command("output-key", "end-response")
    
        global end_choice
        end_choice = ''

        actr.run_full_time(5)

        actr.remove_command_monitor("output-key", "end-response")
        actr.remove_command("end-response")

    return end_choice

def run_trial(size, time):
    global fractions, end_choice
    numer, denom = random.choice(fractions)
    end_choice = model(numer, denom, size, time)

def run_game(size, time):
    actr.reset()
    actr.start_hand_at_mouse()
    n_trials = 0
    while end_choice != "e":
        run_trial(size, time)
        n_trials += 1
        if n_trials > 10: break
    return np.log(n_trials*5)

def run_experiment(n):
    global ship_sizes, time_limits
    size_results, time_results = list(), list()
    for _ in range(n):
        sizes = actr.permute_list(ship_sizes)
        times = actr.permute_list(time_limits)
        exp_results = np.zeros((9,8))
        for s in range(9):
            for t in range(8):
                exp_results[s,t] = run_game(sizes[s], times[t])
        size_results.append(np.mean(exp_results, axis=1))
        time_results.append(np.mean(exp_results, axis=0))
    size_results = np.array(size_results)
    time_results = np.array(time_results)
    print_results(size_results, time_results)
    
def print_results(size_results, time_results):
    global size_data, time_data
    size_results_mn = np.mean(size_results, axis=0)
    time_results_mn = np.mean(time_results, axis=0)

    print()
    print("Size Results:")
    actr.correlation(size_data, size_results_mn)
    actr.mean_deviation(size_data, size_results_mn)
    print("Original   Current")
    for i in range(9):
        print(" ", end="")
        print("{:.3f}".format(size_data[i]), end="      ")
        print("{:.3f}".format(size_results[i]), end="\n")
    print()

    print("Time Results:")
    actr.correlation(time_data, time_results_mn)
    actr.mean_deviation(time_data, time_results_mn)
    print("Original   Current")
    for i in range(8):
        print(" ", end="")
        print("{:.3f}".format(time_data[i]), end="      ")
        print("{:.3f}".format(time_results_mn[i]), end="\n")
    print()

def plot_results(size_results, time_results):
    global ship_sizes, time_limits, size_data, time_data
    size_results_mn = np.mean(size_results, axis=0)
    time_results_mn = np.mean(time_results, axis=0)
    size_results_se = np.std(size_results, axis=0) / size_results.shape[0]
    time_results_se = np.std(time_results, axis=0) / time_results.shape[0]

    plt.figure()
    plt.plot(ship_sizes, size_results_mn, yerr = size_results_se, color = "orange")
    plt.plot(ship_sizes, size_data, color = "blue")
    plt.legend(labels = ["Model", "Human"], loc = "upper right")
    plt.xlabel("Ship Sizes")
    plt.ylabel("Engagement (log(Time x Trials))")
    plt.title("Comparison of Model and Human Performance (Size)")
    plt.draw()

    plt.figure()
    plt.plot(time_limits, time_results_mn, yerr = time_results_se, color = "orange")
    plt.plot(time_limits, time_data, color = "blue")
    plt.legend(labels = ["Model", "Human"], loc = "upper right")
    plt.xlabel("Time Limit")
    plt.ylabel("Engagement (log(Time x Trials))")
    plt.title("Comparison of Model and Human Performance (Time)")
    plt.draw()

    plt.ioff()
    plt.show()