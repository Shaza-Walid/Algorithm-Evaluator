# This library (customtkinter) is more modern than tkinter for design
import customtkinter as ctk
from evaluator import evaluate_algorithm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import sys

# Dark mode theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── colours ────────────────────────────────────────
C_BLUE   = "#3B8ED0"
C_GREEN  = "#2ECC71"
C_RED    = "#E74C3C"
C_YELLOW = "#F1C40F"
C_GRAY   = "#555555"
C_BG     = "#1E1E1E"
C_BAR_BG = "#333333" # Dark background for the progress bars


def run_app():
    root = ctk.CTk()
    root.title("Algorithm Performance Evaluator")
    root.geometry("1400x800")  # Increased size for full visibility
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # ── FONTS ────────────────────────────────────────────────
    font_title  = ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
    font_text   = ctk.CTkFont(family="Segoe UI", size=13)
    font_code   = ctk.CTkFont(family="Consolas", size=14)
    font_big    = ctk.CTkFont(family="Segoe UI", size=32, weight="bold")
    font_result = ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
    font_small  = ctk.CTkFont(family="Segoe UI", size=11)

    # ════════════════════════════════════════════════════════
    # LEFT PANEL
    # ════════════════════════════════════════════════════════
    left = ctk.CTkFrame(root, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    left.grid_columnconfigure(0, weight=1)
    left.grid_rowconfigure(2, weight=1)

    ctk.CTkLabel(left, text="Algorithm Evaluator",
                 font=font_title, text_color=C_BLUE).grid(row=0, column=0)

    code_input = ctk.CTkTextbox(left, font=font_code,
                                 fg_color=C_BG, border_width=2,
                                 border_color=C_BLUE)
    code_input.grid(row=2, column=0, sticky="nsew", pady=10)

    mode_var = ctk.StringVar(value="auto")

    ctrl = ctk.CTkFrame(left)
    ctrl.grid(row=3, column=0, sticky="ew")

    ctk.CTkRadioButton(ctrl, text="Auto Mode",
                       variable=mode_var, value="auto").pack(side="left", padx=10)

    ctk.CTkRadioButton(ctrl, text="Manual Mode",
                       variable=mode_var, value="manual").pack(side="left", padx=10)

    manual_entry = ctk.CTkEntry(ctrl,
                                placeholder_text="5,3,8,1,9...")
    manual_entry.pack(side="left", fill="x", expand=True, padx=10)

    status_lbl = ctk.CTkLabel(left, text="")
    status_lbl.grid(row=4, column=0)

    run_btn = ctk.CTkButton(left, text="RUN ANALYSIS")
    run_btn.grid(row=5, column=0, pady=10)

    # ════════════════════════════════════════════════════════
    # RIGHT PANEL
    # ════════════════════════════════════════════════════════
    right = ctk.CTkFrame(root, fg_color="transparent")
    right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    ctk.CTkLabel(right, text="Analysis Results",
                 font=font_title, text_color=C_BLUE).pack()

    complexity_lbl = ctk.CTkLabel(right, text="—", font=font_big, text_color=C_GREEN)
    complexity_lbl.pack()

    desc_lbl = ctk.CTkLabel(right, text="")
    desc_lbl.pack()

    # Confidence section
    conf_container = ctk.CTkFrame(right, fg_color="transparent")
    conf_container.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(conf_container, text="Confidence", font=font_small, text_color=C_GRAY).pack(anchor="w")

    # Initial color is set to Red
    confidence_bar = ctk.CTkProgressBar(conf_container, fg_color=C_BAR_BG, progress_color=C_RED, height=8, corner_radius=10)
    confidence_bar.set(0)
    confidence_bar.pack(fill="x", pady=(5, 0))

    percent_lbl = ctk.CTkLabel(conf_container, text="0.0%", font=font_small, text_color=C_GRAY)
    percent_lbl.pack(anchor="e")

    cand_frame = ctk.CTkFrame(right, fg_color="transparent")
    cand_frame.pack(fill="x", padx=10)
    
    ctk.CTkLabel(cand_frame, text="CANDIDATE CLASSES", font=ctk.CTkFont(size=12, weight="bold"), text_color=C_GRAY).pack(anchor="w", pady=(10, 5))

    cand_labels = []
    cand_bars = []
    bar_colors = [C_GREEN, C_BLUE, C_YELLOW] 

    for i in range(3):
        row = ctk.CTkFrame(cand_frame, fg_color="transparent")
        row.pack(fill="x", pady=5)

        lbl = ctk.CTkLabel(row, text="", width=120, anchor="w", font=font_result)
        lbl.pack(side="left")

        bar = ctk.CTkProgressBar(
            row, 
            progress_color=bar_colors[i], 
            fg_color=C_BAR_BG, 
            height=8, 
            corner_radius=10
        )
        bar.set(0)
        bar.pack(side="left", fill="x", expand=True)

        cand_labels.append(lbl)
        cand_bars.append(bar)

    # ── Classification label  (NEW — shown only in Manual Mode) ──
    classification_lbl = ctk.CTkLabel(right, text="", font=font_result)
    classification_lbl.pack(pady=(8, 0))

    graph_frame = ctk.CTkFrame(right, fg_color=C_BG)
    graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    current_canvas = [None]

    # ════════════════════════════════════════════════════════
    # UI UPDATE HELPER  (NEW — called from the worker thread via root.after)
    # ════════════════════════════════════════════════════════
    def update_ui(result):
        """Apply analysis results to all widgets. Always runs on the main thread."""
        run_btn.configure(state="normal", text="RUN ANALYSIS")
        status_lbl.configure(text="")

        if isinstance(result, str):
            status_lbl.configure(text=result)
            classification_lbl.configure(text="")
            return

        fig, info = result

        complexity_lbl.configure(text=info["top_label"])
        desc_lbl.configure(text=info["top_desc"])

        # Dynamic color logic for confidence bar
        raw_conf = info["confidence"]
        if raw_conf >= 80:
            confidence_bar.configure(progress_color=C_GREEN)
        elif raw_conf >= 50:
            confidence_bar.configure(progress_color=C_YELLOW)
        else:
            confidence_bar.configure(progress_color=C_RED)

        confidence_bar.set(raw_conf / 100)
        percent_lbl.configure(text=f"{raw_conf:.1f}%")

        for i in range(3):
            if i < len(info["candidates"]):
                lbl_text, r2 = info["candidates"][i]
                cand_labels[i].configure(text=lbl_text)
                cand_bars[i].set(r2 / 100)

        # ── Show classification result for Manual Mode  (NEW) ──
        if "classification" in info:
            c = info["classification"]
            closest = c["closest"]

            color_map = {
                "Best Case":    C_GREEN,
                "Average Case": C_BLUE,
                "Worst Case":   C_RED,
            }
            classification_lbl.configure(
                text=f"📍 Your input is closest to: {closest}",
                text_color=color_map[closest]
            )
        else:
            classification_lbl.configure(text="")

        # Replace the chart
        if current_canvas[0]:
            current_canvas[0].get_tk_widget().destroy()

        plt.close("all")
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
        current_canvas[0] = canvas

    # ════════════════════════════════════════════════════════
    # RUN LOGIC  (updated — runs analysis in a background thread)
    # ════════════════════════════════════════════════════════
    def run_analysis():
        user_code = code_input.get("1.0", "end").strip()

        if not user_code:
            status_lbl.configure(text="Enter code first")
            return

        # Validate manual array before starting the thread
        arr = None
        if mode_var.get() == "manual":
            raw = manual_entry.get().strip()
            if not raw:
                status_lbl.configure(text="Enter a manual array first")
                return
            try:
                arr = list(map(int, raw.split(",")))
            except ValueError:
                status_lbl.configure(text="Invalid array — use comma-separated integers")
                return

        # Disable button and show progress while the worker runs
        run_btn.configure(state="disabled", text="Analyzing...")
        status_lbl.configure(text="⏳ Running analysis in background…")
        classification_lbl.configure(text="")

        def worker():
            result = evaluate_algorithm(user_code, mode_var.get(), arr)
            # Always update the UI from the main thread
            root.after(0, lambda: update_ui(result))

        threading.Thread(target=worker, daemon=True).start()

    run_btn.configure(command=run_analysis)

    def on_close():
        plt.close("all")
        root.destroy()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    run_app()