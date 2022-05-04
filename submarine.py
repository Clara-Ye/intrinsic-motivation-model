import sys
sys.path.append("C:/Users/MSI-NB/Desktop/2022_Spring/85-412/ACT-R/tutorial/python")
import actr
import random
import numpy as np
import matplotlib.pyplot as plt

actr.load_act_r_model("ACT-R:project;intrinsic-motivation-model;submarine-model.lisp")

size_success_data = [0.1250, 0.1375, 0.1750,
                     0.2000, 0.2500, 0.2750,
                     0.3000, 0.3375, 0.3750]
size_engage_data = [5.100, 5.125, 5.200,
                    5.250, 5.350, 5.400,
                    5.375, 5.500, 5.575]
ship_sizes = [0.04, 0.06, 0.08,
              0.10, 0.16, 0.20,
              0.24, 0.30, 0.40]

time_success_data = [0.1550, 0.1750, 0.2135, 0.2250,
                     0.2550, 0.2700, 0.2800, 0.3250]
time_engage_data =  [4.600, 5.125, 5.175, 5.225,
                     5.350, 5.450, 5.500, 5.650]
time_limits = [2,  3,  4,  5,
               8, 10, 15, 30]

fractions = [(1,10), (1,8),  (1,6),  (1,5),  (1,4),
             (3,10), (1,3),  (3,8),  (2,5),  (3,7),
             (1,2),  (3,5),  (5,8),  (2,3),  (7,10),
             (3,4),  (4,5),  (5,6),  (7,8),  (9,10)]
#fractions = [(1,4), (1,3), (1,2), (2,3), (3,4)]
repetitions = {(1,10):0,  (1,8):0,  (1,6):0,  (1,5):0,  (1,4): 0,
               (3,10):0,  (1,3):0,  (3,8):0,  (2,5):0,  (3,7): 0,
               (1,2): 0,  (3,5):0,  (5,8):0,  (2,3):0,  (7,10):0,
               (3,4): 0,  (4,5):0,  (5,6):0,  (7,8):0,  (9,10):0}

click_loc = None
end_choice = None
current_numer = None
current_fracline = None
current_denom = None

def respond_to_key_press(model, key):
    global end_choice
    end_choice = key

def respond_to_mouse_click(model, coord, finger):
    global click_loc
    click_loc = coord[0]

def calculate_reward(numer, denom):
    global repetitions
    fraction = (numer, denom)
    rep = repetitions[fraction]
    return 4 - 2*rep

def model(numer, denom, size, time):
    global current_numer, current_fracline, current_denom
    correct = 0
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
        actr.start_hand_at_mouse()

        global click_loc
        click_loc = -1

        actr.set_buffer_chunk("goal", "first-goal")
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
        ship_line = actr.add_line_to_exp_window(window,
                                                [left_end,145],
                                                [right_end,145],
                                                "red")

        click_loc_trans = 50 + (click_loc-550)/(950-550) * (450-50)
        print(click_loc, click_loc_trans, x_correct)
        if (left_end <= click_loc_trans) and (click_loc_trans <= right_end):
            actr.trigger_reward(calculate_reward(numer, denom))
            correct = 1
        else:
            actr.trigger_reward(-1)

        # trial-end choice
        actr.add_command("end-response", respond_to_key_press, 
                         "Submarine task trial end key response")
        actr.monitor_command("output-key", "end-response")
    
        global end_choice
        end_choice = ''

        actr.set_buffer_chunk("goal", "second-goal")
        actr.run_full_time(5)

        actr.remove_command_monitor("output-key", "end-response")
        actr.remove_command("end-response")
    return correct

def run_trial(size, time):
    global fractions, repetitions, end_choice
    fraction = random.choice(fractions)
    numer, denom = fraction
    correct = model(numer, denom, size, time)
    if correct: repetitions[fraction] += 1
    return correct

def run_game(size, time):
    global repetitions, end_choice
    repetitions = {(1,10):0,  (1,8):0,  (1,6):0,  (1,5):0,  (1,4): 0,
                   (3,10):0,  (1,3):0,  (3,8):0,  (2,5):0,  (3,7): 0,
                   (1,2): 0,  (3,5):0,  (5,8):0,  (2,3):0,  (7,10):0,
                   (3,4): 0,  (4,5):0,  (5,6):0,  (7,8):0,  (9,10):0}
    end_choice = ""
    n_trials = success_trials = 0
    actr.reset()
    while end_choice != "e":
        n_trials += 1
        success_trials += run_trial(size, time)
    return success_trials/n_trials, np.log(n_trials*6.6)

def run_experiment(n):
    global ship_sizes, time_limits
    size_success_results, size_engage_results = list(), list()
    time_success_results, time_engage_results = list(), list()
    for _ in range(n):
        success_results, engage_results = np.zeros((9,8)), np.zeros((9,8))
        for s in range(9):
            for t in range(8):
                success, engage = run_game(ship_sizes[s], time_limits[t])
                success_results[s,t] = success
                engage_results[s,t] = engage
        size_success_results.append(np.mean(success_results, axis=1))
        time_success_results.append(np.mean(success_results, axis=0))
        size_engage_results.append(np.mean(engage_results, axis=1))
        time_engage_results.append(np.mean(engage_results, axis=0))
    size_success_results = np.array(size_success_results)
    time_success_results = np.array(time_success_results)
    size_engage_results = np.array(size_engage_results)
    time_engage_results = np.array(time_engage_results)
    #print_results(size_success_results, time_success_results,
    #              size_engage_results, time_engage_results)
    plot_results(size_success_results, time_success_results,
                  size_engage_results, time_engage_results)
    
def print_results(size_success_results, time_success_results,
                  size_engage_results, time_engage_results):
    global size_success_data, time_success_data
    global size_engage_data, time_engage_data

    size_success_results_mn = np.mean(size_success_results, axis=0)
    time_success_results_mn = np.mean(time_success_results, axis=0)
    size_engage_results_mn = np.mean(size_engage_results, axis=0)
    time_engage_results_mn = np.mean(time_engage_results, axis=0)

    print()
    print("Size Success Results:")
    actr.correlation(size_success_data, list(size_success_results_mn))
    actr.mean_deviation(size_success_data, list(size_success_results_mn))
    print("Original   Current")
    for i in range(9):
        print(" ", end="")
        print("{:.3f}".format(size_success_data[i]), end="      ")
        print("{:.3f}".format(size_success_results_mn[i]), end="\n")
    print()

    print("Time Success Results:")
    actr.correlation(time_success_data, list(time_success_results_mn))
    actr.mean_deviation(time_success_data, list(time_success_results_mn))
    print("Original   Current")
    for i in range(8):
        print(" ", end="")
        print("{:.3f}".format(time_success_data[i]), end="      ")
        print("{:.3f}".format(time_success_results_mn[i]), end="\n")
    print()

    print("Size Engage Results:")
    actr.correlation(size_engage_data, list(size_engage_results_mn))
    actr.mean_deviation(size_engage_data, list(size_engage_results_mn))
    print("Original   Current")
    for i in range(9):
        print(" ", end="")
        print("{:.3f}".format(size_engage_data[i]), end="      ")
        print("{:.3f}".format(size_engage_results_mn[i]), end="\n")
    print()

    print("Time Engage Results:")
    actr.correlation(time_engage_data, list(time_engage_results_mn))
    actr.mean_deviation(time_engage_data, list(time_engage_results_mn))
    print("Original   Current")
    for i in range(8):
        print(" ", end="")
        print("{:.3f}".format(time_engage_data[i]), end="      ")
        print("{:.3f}".format(time_engage_results_mn[i]), end="\n")
    print()

def plot_results(size_success_results, time_success_results,
                 size_engage_results, time_engage_results):
    global ship_sizes, time_limits
    global size_success_data, time_success_data
    global size_engage_data, time_engage_data

    size_success_results_mn = np.mean(size_success_results, axis=0)
    time_success_results_mn = np.mean(time_success_results, axis=0)
    size_success_results_se = np.std(size_success_results, axis=0) / size_success_results.shape[0]
    time_success_results_se = np.std(time_success_results, axis=0) / time_success_results.shape[0]
    size_engage_results_mn = np.mean(size_engage_results, axis=0)
    time_engage_results_mn = np.mean(time_engage_results, axis=0)
    size_engage_results_se = np.std(size_engage_results, axis=0) / size_engage_results.shape[0]
    time_engage_results_se = np.std(time_engage_results, axis=0) / time_engage_results.shape[0]

    plt.figure()
    plt.plot(ship_sizes, size_success_results_mn, yerr = size_success_results_se, color = "orange")
    plt.plot(ship_sizes, size_success_data, color = "blue")
    plt.legend(labels = ["Model", "Human"], loc = "upper right")
    plt.xlabel("Ship Sizes")
    plt.ylabel("Success Rate")
    plt.title("Comparison of Model and Human Performance (Size)")
    plt.draw()

    plt.figure()
    plt.plot(time_limits, time_success_results_mn, yerr = time_success_results_se, color = "orange")
    plt.plot(time_limits, time_success_data, color = "blue")
    plt.legend(labels = ["Model", "Human"], loc = "upper right")
    plt.xlabel("Time Limit")
    plt.ylabel("Success Rate")
    plt.title("Comparison of Model and Human Performance (Time)")
    plt.draw()

    plt.figure()
    plt.plot(ship_sizes, size_engage_results_mn, yerr = size_engage_results_se, color = "orange")
    plt.plot(ship_sizes, size_engage_data, color = "blue")
    plt.legend(labels = ["Model", "Human"], loc = "upper right")
    plt.xlabel("Ship Sizes")
    plt.ylabel("Engagement (log(Time x Trials))")
    plt.title("Comparison of Model and Human Engagement (Size)")
    plt.draw()

    plt.figure()
    plt.plot(time_limits, time_engage_results_mn, yerr = time_engage_results_se, color = "orange")
    plt.plot(time_limits, time_engage_data, color = "blue")
    plt.legend(labels = ["Model", "Human"], loc = "upper right")
    plt.xlabel("Ship Sizes")
    plt.ylabel("Engagement (log(Time x Trials))")
    plt.title("Comparison of Model and Human Engagement (Time)")
    plt.draw()

    plt.ioff()
    plt.show()