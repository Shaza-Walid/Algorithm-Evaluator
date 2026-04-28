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

# ── colour constants ────────────────────────────────────────
C_BLUE   = "#3B8ED0"
C_GREEN  = "#2ECC71"
C_RED    = "#E74C3C"
C_YELLOW = "#F1C40F"
C_GRAY   = "#555555"
C_BG     = "#1E1E1E"


# This function runs the whole application
def run_app():
    root = ctk.CTk()
    root.title("Algorithm Performance Evaluator")
    root.geometry("1300x750")
    # Split the screen into two columns (50/50 split)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.minsize(1100, 680)

    # Define some fonts
    # ── FONTS ────────────────────────────────────────────────
    font_title  = ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
    font_sub    = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
    font_text   = ctk.CTkFont(family="Segoe UI", size=13)
    font_code   = ctk.CTkFont(family="Consolas", size=14)
    font_big    = ctk.CTkFont(family="Segoe UI", size=32, weight="bold")
    font_result = ctk.CTkFont(family="Segoe UI", size=15, weight="bold")

    # ════════════════════════════════════════════════════════
    #  LEFT PANEL — code input + controls
    # ════════════════════════════════════════════════════════
    left = ctk.CTkFrame(root, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    left.grid_columnconfigure(0, weight=1)
    left.grid_rowconfigure(2, weight=1)   # code box expands

    ctk.CTkLabel(left, text="Algorithm Evaluator", font=font_title,
                 text_color=C_BLUE).grid(row=0, column=0, pady=(10, 5), sticky="ew")

    ctk.CTkLabel(left, text="Write your Python function below:",
                 font=font_text).grid(row=1, column=0, sticky="w", padx=5)

    code_input = ctk.CTkTextbox(left, font=font_code,
                                border_width=2, border_color=C_BLUE,
                                fg_color=C_BG)
    code_input.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5, 10))

    # ── mode + manual entry ──────────────────────────────────
    ctrl = ctk.CTkFrame(left)
    ctrl.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    ctrl.grid_columnconfigure(1, weight=1)

    mode_var = ctk.StringVar(value="auto")

    radio_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
    radio_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    ctk.CTkRadioButton(radio_frame, text="Auto Mode",
                       variable=mode_var, value="auto",
                       font=font_text).pack(pady=4, anchor="w")
    ctk.CTkRadioButton(radio_frame, text="Manual Mode",
                       variable=mode_var, value="manual",
                       font=font_text).pack(pady=4, anchor="w")

    manual_entry = ctk.CTkEntry(ctrl, font=font_text,
                                placeholder_text="Manual array: 5,3,8,1,9 …",
                                height=32)
    manual_entry.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

    # ── status label ────────────────────────────────────────
    status_lbl = ctk.CTkLabel(left, text="", font=font_text,
                              text_color=C_GRAY)
    status_lbl.grid(row=4, column=0, pady=2, sticky="ew")

    # ── RUN button ───────────────────────────────────────────
    run_btn = ctk.CTkButton(
        left, text="▶  RUN ANALYSIS",
        font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        height=48, corner_radius=10, hover_color="#1F538D"
    )
    run_btn.grid(row=5, column=0, pady=(5, 15), padx=5, sticky="ew")

    # ════════════════════════════════════════════════════════
    #  RIGHT PANEL — graph + results
    # ════════════════════════════════════════════════════════
    right = ctk.CTkScrollableFrame(root)
    right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    ctk.CTkLabel(right, text="Analysis Results", font=font_title,
                 text_color=C_BLUE).pack(pady=(10, 5))

    # ── detected complexity ──────────────────────────────────
    complexity_frame = ctk.CTkFrame(right)
    complexity_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(complexity_frame, text="DETECTED COMPLEXITY",
                 font=font_sub, text_color=C_GRAY).pack(anchor="w", padx=15, pady=(10, 0))

    complexity_lbl = ctk.CTkLabel(complexity_frame, text="—",
                                  font=font_big, text_color=C_GREEN)
    complexity_lbl.pack(anchor="w", padx=15)

    desc_lbl = ctk.CTkLabel(complexity_frame, text="",
                            font=font_text, text_color="#AAAAAA")
    desc_lbl.pack(anchor="w", padx=15, pady=(0, 5))

    # confidence bar
    ctk.CTkLabel(complexity_frame, text="Confidence",
                 font=font_sub, text_color=C_GRAY).pack(anchor="w", padx=15)

    confidence_bar = ctk.CTkProgressBar(complexity_frame, height=14,
                                        progress_color=C_GREEN)
    confidence_bar.set(0)
    confidence_bar.pack(fill="x", padx=15, pady=(3, 12))

    confidence_pct_lbl = ctk.CTkLabel(complexity_frame, text="",
                                      font=font_text, text_color=C_GRAY)
    confidence_pct_lbl.pack(anchor="e", padx=15, pady=(0, 10))

    # ── candidate classes ────────────────────────────────────
    cand_frame = ctk.CTkFrame(right)
    cand_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(cand_frame, text="CANDIDATE CLASSES",
                 font=font_sub, text_color=C_GRAY).pack(anchor="w", padx=15, pady=(10, 5))

    cand_labels  = []
    cand_bars    = []
    CAND_COLORS  = [C_GREEN, C_BLUE, C_YELLOW]

    for i in range(3):
        row_f = ctk.CTkFrame(cand_frame, fg_color="transparent")
        row_f.pack(fill="x", padx=15, pady=3)
        lbl = ctk.CTkLabel(row_f, text="", font=font_result, width=130, anchor="w")
        lbl.pack(side="left")
        bar = ctk.CTkProgressBar(row_f, height=12,
                                 progress_color=CAND_COLORS[i])
        bar.set(0)
        bar.pack(side="left", fill="x", expand=True, padx=(5, 0))
        cand_labels.append(lbl)
        cand_bars.append(bar)

    ctk.CTkLabel(cand_frame, text="", height=8).pack()   # spacer

    # ── best / avg / worst row ───────────────────────────────
    baw_frame = ctk.CTkFrame(right)
    baw_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(baw_frame, text="RUNTIME SCENARIOS",
                 font=font_sub, text_color=C_GRAY).pack(anchor="w", padx=15, pady=(10, 5))

    cols_frame = ctk.CTkFrame(baw_frame, fg_color="transparent")
    cols_frame.pack(fill="x", padx=15, pady=(0, 12))
    cols_frame.grid_columnconfigure(0, weight=1)
    cols_frame.grid_columnconfigure(1, weight=1)
    cols_frame.grid_columnconfigure(2, weight=1)

    def _make_scenario_col(parent, col_idx, title, color):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=0, column=col_idx, padx=5)
        ctk.CTkLabel(f, text=title, font=font_sub,
                     text_color=color).pack()
        val = ctk.CTkLabel(f, text="—", font=font_result,
                           text_color=color)
        val.pack()
        return val

    best_lbl  = _make_scenario_col(cols_frame, 0, "BEST",  C_GREEN)
    avg_lbl   = _make_scenario_col(cols_frame, 1, "AVG",   C_BLUE)
    worst_lbl = _make_scenario_col(cols_frame, 2, "WORST", C_RED)

    # ── graph container ──────────────────────────────────────
    graph_frame = ctk.CTkFrame(right, fg_color=C_BG)
    graph_frame.pack(fill="both", padx=10, pady=(5, 15))

    current_canvas = [None]   # list so nonlocal works in nested fn

    # ════════════════════════════════════════════════════════
    #  RUN LOGIC
    # ════════════════════════════════════════════════════════
    def run_analysis():
        user_code = code_input.get("1.0", "end").strip()
        if not user_code:
            status_lbl.configure(text="⚠  Please enter your function.", text_color=C_YELLOW)
            return

        arr = None
        if mode_var.get() == "manual":
            raw = manual_entry.get().strip()
            if not raw:
                status_lbl.configure(text="⚠  Enter an array for manual mode.", text_color=C_YELLOW)
                return
            try:
                arr = list(map(int, raw.split(",")))
            except ValueError:
                status_lbl.configure(text="✗  Invalid array — integers only, comma-separated.",
                                     text_color=C_RED)
                return

        # clear old canvas
        if current_canvas[0]:
            current_canvas[0].get_tk_widget().destroy()
            current_canvas[0] = None
        plt.close('all')

        status_lbl.configure(text="⏳  Running…", text_color=C_BLUE)
        root.update_idletasks()

        result = evaluate_algorithm(user_code, mode_var.get(), arr)

        # ── error ────────────────────────────────────────────
        if isinstance(result, str):
            status_lbl.configure(text=f"✗  {result}", text_color=C_RED)
            complexity_lbl.configure(text="Error", text_color=C_RED)
            return

        fig, info = result

        # ── update detected complexity ───────────────────────
        complexity_lbl.configure(text=info["top_label"], text_color=C_GREEN)
        desc_lbl.configure(text=info["top_desc"])

        conf = info["confidence"] / 100.0
        confidence_bar.set(min(conf, 1.0))
        confidence_pct_lbl.configure(text=f"{info['confidence']:.1f}%")

        # bar colour: green ≥80%, yellow ≥50%, red <50%
        bar_color = C_GREEN if conf >= 0.8 else (C_YELLOW if conf >= 0.5 else C_RED)
        confidence_bar.configure(progress_color=bar_color)

        # ── candidate classes ─────────────────────────────────
        for i in range(3):
            if i < len(info["candidates"]):
                lbl_text, r2_pct = info["candidates"][i]
                cand_labels[i].configure(text=lbl_text)
                cand_bars[i].set(min(r2_pct / 100.0, 1.0))
            else:
                cand_labels[i].configure(text="")
                cand_bars[i].set(0)

        # ── best / avg / worst ────────────────────────────────
        best_lbl.configure(text=info["best_label"])
        avg_lbl.configure(text=info["avg_label"])
        worst_lbl.configure(text=info["worst_label"])

        # ── manual mode extra info ────────────────────────────
        if "manual_time" in info:
            status_lbl.configure(
                text=f"✔  Manual run: {info['manual_time']*1000:.4f} ms  (n={len(arr)})",
                text_color=C_GREEN)
        else:
            status_lbl.configure(text="✔  Analysis complete.", text_color=C_GREEN)

        # ── embed graph ───────────────────────────────────────
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
        current_canvas[0] = canvas

    run_btn.configure(command=run_analysis)

    # ── clean exit ───────────────────────────────────────────
    def on_closing():
        plt.close('all')
        root.quit()
        try:
            root.destroy()
        except Exception:
            pass
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()