import time
import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

# =============================================================
# COMPLEXITY MODEL FUNCTIONS
# Each function models how time T grows with input size n
# =============================================================

def model_O1(n, a):
    return a * np.ones_like(n, dtype=float)

def model_Ologn(n, a):
    return a * np.log2(n + 1)

def model_On(n, a):
    return a * n

def model_Onlogn(n, a):
    return a * n * np.log2(n + 1)

def model_On2(n, a):
    return a * n ** 2

def model_On2logn(n, a):
    return a * (n ** 2) * np.log2(n + 1)

def model_On3(n, a):
    return a * n ** 3

def model_O2n(n, a):
    return a * 2.0 ** (n / 50.0)   # scaled to avoid overflow on large n

# Registry: label → (function, display_name)
COMPLEXITY_MODELS = [
    ("O(1)",         model_O1,       "Constant"),
    ("O(log n)",     model_Ologn,    "Logarithmic"),
    ("O(n)",         model_On,       "Linear"),
    ("O(n log n)",   model_Onlogn,   "Linearithmic"),
    ("O(n²)",        model_On2,      "Quadratic"),
    ("O(n² log n)",  model_On2logn,  "Quad-Linearithmic"),
    ("O(n³)",        model_On3,      "Cubic"),
    ("O(2ⁿ)",        model_O2n,      "Exponential"),
]


# =============================================================
# CURVE-FITTING BASED COMPLEXITY ESTIMATOR
# Returns sorted list of (label, r_squared, description)
# =============================================================

def estimate_big_o(sizes, times):
    n = np.array(sizes, dtype=float)
    t = np.array(times, dtype=float)

    # Avoid division-by-zero: floor times at 1 nanosecond
    t = np.maximum(t, 1e-9)

    results = []

    for label, model_fn, description in COMPLEXITY_MODELS:
        try:
            popt, _ = curve_fit(model_fn, n, t, p0=[1e-6], maxfev=10000)
            t_pred = model_fn(n, *popt)

            # R² score — how well does the model fit?
            ss_res = np.sum((t - t_pred) ** 2)
            ss_tot = np.sum((t - np.mean(t)) ** 2)
            r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
            r2 = max(0.0, min(1.0, r2))   # clamp to [0, 1]

            results.append((label, r2, description))
        except Exception:
            results.append((label, 0.0, description))

    # Sort descending by R²
    results.sort(key=lambda x: x[1], reverse=True)
    return results   # list of (label, r2_score, description)


# =============================================================
# INPUT GENERATORS FOR AUTO MODE
# =============================================================

def make_best_case(n):
    """Already sorted array — best case for most sorting algorithms."""
    return list(range(n))

def make_worst_case(n):
    """Reverse sorted array — worst case for many algorithms."""
    return list(range(n, 0, -1))

def make_avg_case(n):
    """Random shuffled array — average case."""
    arr = list(range(n))
    random.shuffle(arr)
    return arr


# =============================================================
# TIMING HELPER
# Runs func(arr) multiple times and returns median time
# =============================================================

SIZES = [10, 50, 100, 300, 500, 700, 1000]
REPEATS = 3   # median of this many runs per size for stability


def _time_func(func, arr):
    """Return median execution time of func(arr) over REPEATS runs."""
    recorded = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        func(arr)
        recorded.append(time.perf_counter() - start)
    return float(np.median(recorded))


# =============================================================
# PLOT BUILDER
# =============================================================

def _build_plot(sizes, best_times, avg_times, worst_times, top_label, confidence_pct):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)

    ax.plot(sizes, best_times,  marker='o', color='#2ECC71', linewidth=2, label='Best Case')
    ax.plot(sizes, avg_times,   marker='s', color='#3B8ED0', linewidth=2, label='Average Case')
    ax.plot(sizes, worst_times, marker='^', color='#E74C3C', linewidth=2, label='Worst Case')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Input Size (n)  [log scale]")
    ax.set_ylabel("Execution Time (s)  [log scale]")
    ax.set_title(f"Performance  —  {top_label}  ({confidence_pct:.0f}% fit)")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", ls="--", alpha=0.3)

    return fig


# =============================================================
# MAIN EVALUATION ENTRY POINT
# Returns (fig, result_dict) on success, or a plain string on error
#
# result_dict keys:
#   "top_label"      – best-fit complexity string  e.g. "O(n²)"
#   "top_desc"       – e.g. "Quadratic"
#   "confidence"     – R² as percentage  e.g. 97.3
#   "candidates"     – top-3 list of (label, r2_pct)
#   "best_label"     – complexity for best-case input
#   "avg_label"      – complexity for average-case input
#   "worst_label"    – complexity for worst-case input
# =============================================================

def evaluate_algorithm(user_code, mode="auto", manual_arr=None):

    local_scope = {}

    try:
        exec(user_code, {}, local_scope)
    except Exception as e:
        return "Code Error: {}".format(e)

    # Find first callable
    func = None
    for key in local_scope:
        if callable(local_scope[key]):
            func = local_scope[key]
            break

    if func is None:
        return "No function found in the submitted code."

    # ----------------------------------------------------------
    # MODE 1 — Manual
    # ----------------------------------------------------------
    if mode == "manual":
        if manual_arr is None or len(manual_arr) == 0:
            return "Manual mode requires a non-empty array."

        try:
            exec_time = _time_func(func, manual_arr)
        except Exception as e:
            return "Runtime Error: {}".format(e)

        # Single data point — can't fit curves, just report time
        plt.close('all')
        fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
        ax.bar(["Your Input  (n={})".format(len(manual_arr))], [exec_time],
               color='#3B8ED0', width=0.4)
        ax.set_ylabel("Execution Time (seconds)")
        ax.set_title("Manual Run Result")
        ax.grid(True, axis='y', ls='--', alpha=0.3)

        result = {
            "top_label":  "N/A (single run)",
            "top_desc":   "Need multiple sizes for Big-O estimation",
            "confidence": 0.0,
            "candidates": [],
            "best_label":  "—",
            "avg_label":   "—",
            "worst_label": "—",
            "manual_time": exec_time,
        }
        return fig, result

    # ----------------------------------------------------------
    # MODE 2 — Auto  (best / avg / worst)
    # ----------------------------------------------------------
    best_times  = []
    avg_times   = []
    worst_times = []

    try:
        for n in SIZES:
            best_times.append(_time_func(func, make_best_case(n)))
            avg_times.append(_time_func(func,  make_avg_case(n)))
            worst_times.append(_time_func(func, make_worst_case(n)))
    except Exception as e:
        return "Runtime Error: {}".format(e)

    # Fit curves on the average-case times (most representative)
    candidates = estimate_big_o(SIZES, avg_times)   # sorted by R²

    top_label, top_r2, top_desc = candidates[0]
    confidence_pct = top_r2 * 100.0

    # Per-scenario labels (best/worst may differ)
    best_cands  = estimate_big_o(SIZES, best_times)
    worst_cands = estimate_big_o(SIZES, worst_times)

    fig = _build_plot(SIZES, best_times, avg_times, worst_times, top_label, confidence_pct)

    result = {
        "top_label":   top_label,
        "top_desc":    top_desc,
        "confidence":  confidence_pct,
        "candidates":  [(lbl, r2 * 100.0) for lbl, r2, _ in candidates[:3]],
        "best_label":  best_cands[0][0],
        "avg_label":   top_label,
        "worst_label": worst_cands[0][0],
    }

    return fig, result