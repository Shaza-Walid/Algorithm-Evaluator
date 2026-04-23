import time
import matplotlib.pyplot as plt
import numpy as np

# This function tries to estimate the Big-O complexity based on how execution time grows as input size increases.
def estimate_big_o(sizes, times):

    # We store ratios of how much time increases between runs
    ratios = []

    # Start from index 1 because we compare with previous value
    for i in range(1, len(times)):
        # Ratio = current time / previous time
        ratios.append(times[i] / times[i-1])

    # Average growth rate of execution time
    avg_ratio = sum(ratios) / len(ratios)

    # ---------------------------------------------------------
    # We use simple heuristic thresholds to guess complexity
    # NOTE: This is NOT mathematically exact, just estimation
    # I think we have to make it mathematical but I couldn't do it
    # ---------------------------------------------------------
    if avg_ratio < 1.5:
        return "O(1)  (Constant Time - very fast, no growth)"
    elif avg_ratio < 3:
        return "O(n)  (Linear Time - grows proportionally)"
    elif avg_ratio < 6:
        return "O(n log n)  (Efficient sorting-like behavior)"
    elif avg_ratio < 15:
        return "O(n^2)  (Quadratic - nested loops likely)"
    else:
        return "O(2^n) or higher (Very slow exponential growth)"
    # write more O(n^3) O(logn)....
    # we mest have at least one test case for every function


# ---------------------------------------------------------
# Main function that evaluates user-provided algorithm
# ---------------------------------------------------------
def evaluate_algorithm(user_code, mode="auto", manual_arr=None):

    # This dictionary will store everything created by exec()
    local_scope = {}

    try:
        # WARNING: exec runs raw Python code from a string
        # It is powerful but unsafe if input is not trusted
        exec(user_code, {}, local_scope)

    except Exception as e:
        # If user's code has syntax or runtime error
        return "Code Error: {}".format(e)

    # We try to find the function written by the user
    # We assume the first callable object is the algorithm
    func = None
    for key in local_scope:
        if callable(local_scope[key]):
            func = local_scope[key]
            break

    # If no function was found
    if func is None:
        return "No function found in code"

    # Different input sizes for performance testing
    sizes = [10, 100, 300, 700, 1000]

    # Store execution times for each input size
    times = []

    try:
        # -----------------------------------------------------
        # MODE 1: Manual testing                                          # not working yet
        # User provides their own input array
        # -----------------------------------------------------
        if mode == "manual":

            start = time.perf_counter()  # start timer
            func(manual_arr)             # run user function
            end = time.perf_counter()    # end timer

            return "Manual run time: {:.6f} sec".format(end - start)

        # -----------------------------------------------------
        # MODE 2: Automatic testing
        # We generate arrays of increasing size
        # -----------------------------------------------------
        for n in sizes:

            # Create input array [0, 1, 2, ..., n-1]
            arr = list(range(n))

            # Start measuring time BEFORE execution
            start = time.perf_counter()

            # Run the user-defined algorithm
            func(arr)

            # Stop measuring time AFTER execution
            end = time.perf_counter()

            # Store how long it took
            times.append(end - start)

    except Exception as e:
        # If function crashes during execution
        return "Runtime Error: {}".format(e)


    # Visualization: plot time vs input size
    plt.plot(sizes, times, marker='o')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Algorithm Performance Analysis")
    plt.grid(True)
    plt.show()

    # Estimate complexity based on collected data
    complexity = estimate_big_o(sizes, times)

    # Return final result to user
    return "Estimated Complexity: " + complexity



'''
Limitations
The function in your code must accept a single list argument.
Only the first callable found in the submitted code is evaluated.
Manual Mode returns only execution time — no graph or Big-O estimate is provided.
Very fast algorithms (sub-microsecond) may produce unreliable Big-O estimates due to timer resolution limits.

check readme.md and edit it in how to use section to fit your fixed code
'''