import sys
sys.path.append("C:/Users/MSI-NB/Desktop/2022_Spring/85-412/ACT-R/tutorial/python")
import actr
import random
import numpy as np

actr.load_act_r_model("ACT-R:project;code;submarine-model.lisp")

# submarine_data = []
fractions = [(1,10), (1,8),  (1,6),  (1,5),  (1,4), 
             (3,10), (1,3),  (3,8),  (2,5),  (3,7), 
             (1,2),  (3,5),  (5,8),  (2,3),  (7,10),
             (3,4),  (4,5),  (5,6),  (7,8),  (9,10)]
end_choice = False
current_numer = None
current_fracline = None
current_denom = None

def respond_to_key_press(model, key):
    global end_choice
    end_choice = key

def model(numer, denom, size, time):
    global current_numer, current_fracline, current_denom
    if actr.visible_virtuals_available():

        # initial display
        window = actr.open_exp_window("Submarine Game", visible=True,
                                      width=500,height=300,x=500,y=300)
        actr.install_device(window)
        actr.add_line_to_exp_window(window,[50,150],[450,150],"blue")
        current_numer = actr.add_text_to_exp_window(window, str(numer), x=250, y=200)
        current_fracline = actr.add_text_to_exp_window(window, "-", x=250, y=210)
        current_denom = actr.add_text_to_exp_window(window, str(denom), x=250, y=220)

        # collects reponse and displays answer
        actr.start_hand_at_mouse()
        actr.run(time)
        actr.remove_items_from_exp_window(window,current_numer)
        actr.remove_items_from_exp_window(window,current_fracline)
        actr.remove_items_from_exp_window(window,current_denom)
        current_numer = current_fracline = current_denom = None

        width_correct = size * (450-50)
        x_correct = 50 + (numer/denom)*(450-50) - width_correct/2
        width_left = x_correct - 50
        x_left = 50
        width_right = 450 - x_correct - width_correct
        x_right = 450 - width_right
        #print(x_correct, width_correct, x_left, width_left, x_right, width_right)
        #actr.add_image_to_exp_window(window, text="target", file="submarine.png",
        #                             x=x, y=120, width=width, height=30)
        actr.add_line_to_exp_window(window,[x_correct-width_correct/2,145],
                                    [x_correct+width_correct/2,145],"red")
        #actr.add_button_to_exp_window(window, text="", color = "green",
        #                              x=x_correct, y=120, 
        #                              height=60, width=width_correct, 
        #                              action=["mouse-pressed","correct"])
        #if (width_left > 0):
        #    actr.add_button_to_exp_window(window, text="", color = "red",
        #                                x=x_left, y=120, 
        #                                height=60, width=width_left, 
        #                                action=["mouse-pressed","left"])
        #if (width_right > 0):
        #    actr.add_button_to_exp_window(window, text="", color = "red",
        #                                x=x_right, y=120, 
        #                                height=60, width=width_right, 
        #                                action=["mouse-pressed","right"])        

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
    n_trials = 0
    while end_choice != "e":
        run_trial(size)
        n_trials += 1
    return n_trials