# We import tkinter library
# tkinter is used to create GUI (Graphical User Interface) apps in Python
import tkinter as tk

# We import our own function from evaluator.py
# This function is responsible for analyzing the algorithm (the cote logic)
from evaluator import evaluate_algorithm


# This is the main function that runs the whole application
def run_app():

    # Create the main window (the app screen)
    root = tk.Tk()

    # Set the title of the window (what appears at the top)
    root.title("Algorithm Performance Evaluator")

    # Set the size of the window (width x height)
    root.geometry("800x600")


    # ---------------- TITLE LABEL ----------------
    # This creates a text label (just text on screen)
    # font=("Arial", 16) means font type Arial and size 16
    tk.Label(root, text="Algorithm Evaluator", font=("Arial", 16)).pack(pady=10)


    # ---------------- CODE INPUT AREA ----------------
    # This label tells the user what to do
    tk.Label(root, text="Enter your algorithm:").pack()

    # This is a big text box where user writes their algorithm code
    # height = number of lines visible
    # width = size of box
    code_input = tk.Text(root, height=10, width=80)
    code_input.pack()


    # ---------------- MODE SELECTION ----------------
    # StringVar is a special variable that stores text in tkinter
    # default value is "auto"
    mode = tk.StringVar(value="auto")

    # Radio buttons = user can select ONLY ONE option

    # Auto mode button (automatic input)
    tk.Radiobutton(root, text="Auto Mode", variable=mode, value="auto").pack()

    # Manual mode button (user enters array manually)
    tk.Radiobutton(root, text="Manual Mode", variable=mode, value="manual").pack()


    # ---------------- MANUAL INPUT ----------------
    # Label for manual array input
    tk.Label(root, text="Manual Array (comma separated):").pack()

    # Entry = small input box (single line)
    manual_entry = tk.Entry(root, width=50)
    manual_entry.pack()


    # ---------------- RESULT DISPLAY ----------------
    # This label will show results after analysis
    result_label = tk.Label(root, text="Result will appear here", fg="blue")
    result_label.pack(pady=10)


    # ---------------- FUNCTION THAT RUNS ANALYSIS ----------------
    def run_analysis():

        # Get code written by user from text box
        # "1.0" means start line 1, character 0
        # tk.END means until the end of text
        user_code = code_input.get("1.0", tk.END)


        # Check which mode is selected
        if mode.get() == "manual":

            # If manual mode → read array from input box
            try:
                # split(",") means split text by commas
                # map(int, ...) converts each item into integer
                arr = list(map(int, manual_entry.get().split(",")))

            except:
                # If user input is wrong, show error message
                result_label.config(text="Invalid manual input")
                return

        else:
            # If auto mode → we don't use manual array
            arr = None


        # Call evaluator function (core logic of project)
        # It returns result (like Big-O estimation)
        result = evaluate_algorithm(user_code, mode.get(), arr)

        # Show result on screen
        result_label.config(text=result)


    # ---------------- BUTTON ----------------
    # Button to start analysis
    # command=run_analysis means when button clicked → run function
    tk.Button(root, text="Run Analysis", command=run_analysis).pack(pady=10)


    # Keep the window running (VERY IMPORTANT)
    # Without this → window will open and close immediately
    root.mainloop()