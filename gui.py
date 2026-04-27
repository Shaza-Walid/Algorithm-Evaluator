# This library (customtkinter)is more modern than tkinter for design
import customtkinter as ctk
from evaluator import evaluate_algorithm
# Added these to embed the plot inside the GUI instead of a separate window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys

# The general theme "dark mode with blue text"
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

# This function runs the whole application
def run_app():
    root = ctk.CTk()
    root.title("Algorithm Performance Evaluator")
    root.geometry("1200x700") # Made wider for the split screen

    # Split the screen into two columns (50/50 split)
    root.grid_columnconfigure(0, weight=1) # Left half
    root.grid_columnconfigure(1, weight=1) # Right half
    root.grid_rowconfigure(0, weight=1)

    # --- LEFT HALF: INPUT & CONTROLS ---
    left_side = ctk.CTkFrame(root, fg_color="transparent")
    left_side.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Define some fonts 
    # title font: bold and large
    title_font = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
    # text font: medium size
    text_font = ctk.CTkFont(family="Segoe UI", size=14)
    # code font: better for readability
    code_font = ctk.CTkFont(family="Consolas", size=15)

    # main title 
    title_label = ctk.CTkLabel(left_side, text="Algorithm Evaluator", font=title_font, text_color="#3B8ED0")
    # space around the title 
    title_label.pack(pady=25)

    # main input area
    input_frame = ctk.CTkFrame(left_side, fg_color="transparent")
    # space around input area
    input_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # instructions for user 
    ctk.CTkLabel(input_frame, text="Write your Python function here:", font=text_font).pack(anchor="w", padx=10)
    
    # code input box
    code_input = ctk.CTkTextbox(
        input_frame, 
        height=250, 
        font=code_font, 
        border_width=2,
        border_color="#3B8ED0",
        fg_color="#1E1E1E" 
    )
    code_input.pack(pady=10, fill="both", expand=True)

    # control panel for mode selection 
    control_panel = ctk.CTkFrame(left_side)
    control_panel.pack(pady=15, padx=10, fill="x")
    # store selected mode
    mode_var = ctk.StringVar(value="auto")
    
    # mode selection 
    radio_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
    radio_frame.pack(side="left", padx=20, pady=10)
    # radio buttons 
    ctk.CTkRadioButton(radio_frame, text="Auto Mode", variable=mode_var, value="auto", font=text_font).pack(pady=5, anchor="w")
    ctk.CTkRadioButton(radio_frame, text="Manual Mode:", variable=mode_var, value="manual", font=text_font).pack(pady=5, anchor="w")

    # manual input area
    manual_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
    manual_frame.pack(side="right", padx=10, fill="x", expand=True)
    # entry for manual
    manual_entry = ctk.CTkEntry(manual_frame, font=text_font, placeholder_text="Manual array: Numbers only...", height=30)
    manual_entry.pack(pady=(35,5), fill="x")

    # result display area
    result_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
    result_label = ctk.CTkLabel(left_side, text="Result will appear here", font=result_font, text_color="#555555")
    result_label.pack(pady=20)

    # --- RIGHT HALF: PLOTTING AREA ---
    right_side = ctk.CTkFrame(root)
    right_side.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    
    ctk.CTkLabel(right_side, text="Performance Graph", font=title_font, text_color= "#3B8ED0").pack(pady=20)
    
    # Container that will hold the graph inside the right half
    plot_container = ctk.CTkFrame(right_side, fg_color="#1E1E1E")
    plot_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Global canvas variable to keep track of the drawing
    current_canvas = None

    # run
    def run_analysis():
        nonlocal current_canvas
        user_code = code_input.get("1.0", "end")
        
        arr = None
        if mode_var.get() == "manual":
            try:
                arr = list(map(int, manual_entry.get().split(",")))
            except:
                result_label.configure(text="Error: Invalid input", text_color="#E74C3C")
                return

        # 1. Properly clear the old canvas if it exists
        if current_canvas:
            current_canvas.get_tk_widget().destroy()
            current_canvas = None
        
        # 2. Clear matplotlib memory
        plt.close('all') 

        # evaluate the code and get result
        # evaluate_algorithm now returns (figure, text)
        result = evaluate_algorithm(user_code, mode_var.get(), arr)
        
        if isinstance(result, tuple):
            fig, complexity_text = result
            result_label.configure(text=f"{complexity_text}", text_color="#2ECC71")
            
            # 3. Create and embed new canvas
            current_canvas = FigureCanvasTkAgg(fig, master=plot_container)
            canvas_widget = current_canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)
            current_canvas.draw()
        else:
            # Show error message if evaluation failed
            result_label.configure(text=f"{result}", text_color="#E74C3C")

    # run button
    run_button = ctk.CTkButton(
        left_side, 
        text="RUN ANALYSIS", 
        command=run_analysis, 
        font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        height=45,
        corner_radius=10,
        hover_color="#1F538D"
    )
    run_button.pack(pady=10)

    # Clean cleanup on exit to prevent "invalid command" errors
    def on_closing():
        plt.close('all')
        root.quit()
        # Using try-except to swallow the 'after' script errors on exit
        try:
            root.destroy()
        except:
            pass
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()