# Algorithm Performance Evaluator

A desktop GUI application that analyzes the runtime performance of user-written Python algorithms, plots execution time graphs, and estimates their Big-O complexity automatically using curve fitting.

---

## Features

- **Auto Mode** – Benchmarks your algorithm across 7 input sizes (`10, 50, 100, 300, 500, 700, 1000`) and measures execution time for best-case, average-case, and worst-case inputs separately.
- **Manual Mode** – Run your algorithm once against a custom array you provide and see the exact execution time on a bar chart.
- **Big-O Estimation** – Fits your timing data against 8 complexity models (`O(1)`, `O(log n)`, `O(n)`, `O(n log n)`, `O(n²)`, `O(n² log n)`, `O(n³)`, `O(2ⁿ)`) using `scipy` curve fitting and selects the best match via R² score.
- **Confidence Score** – Reports how well the best-fit model matches your data (e.g., `97% fit`), with a colour-coded progress bar (green ≥ 80%, yellow ≥ 50%, red < 50%).
- **Performance Graph** – Displays a log-log matplotlib plot of input size vs. execution time for best, average, and worst cases in Auto Mode — embedded directly inside the app window.
- **Modern Dark GUI** – Built with `customtkinter` (dark mode, blue accent theme), no command-line interaction needed.

---

## Project Structure

```
├── main.py          # Entry point — launches the GUI
├── gui.py           # CustomTkinter UI definition and event handling
├── evaluator.py     # Core logic: code execution, timing, Big-O estimation, plotting
└── requirements.txt # Python dependencies
```

---

## Requirements

- Python 3.x
- `matplotlib`
- `numpy`
- `scipy`
- `customtkinter`

Install dependencies with:

```bash
pip install -r requirements.txt
```

> `tkinter` is included with most standard Python installations. If it's missing, install it via your OS package manager (e.g., `sudo apt install python3-tk` on Ubuntu/Debian).

---

## Getting Started

```bash
git clone https://github.com/Shaza-Walid/Algorithm-Evaluator.git
cd Algorithm-Evaluator
pip install -r requirements.txt
python main.py
```

---

## How to Use

1. **Launch the app** by running `python main.py`.

2. **Enter your algorithm** in the code box on the left. Your code must define a function that accepts a list as its single argument. Example:

   ```python
   def my_sort(arr):
       return sorted(arr)
   ```

3. **Choose a mode:**
   - **Auto Mode** – Runs your function against 7 increasing input sizes using sorted (best), shuffled (average), and reverse-sorted (worst) arrays, then plots all three curves.
   - **Manual Mode** – Enter a comma-separated array (e.g., `5, 3, 8, 1`) and run your function once against it to see the raw execution time.

4. **Click "▶ RUN ANALYSIS"** to see the results on the right panel.

---

## Big-O Estimation Logic

In Auto Mode, the evaluator uses **curve fitting** (via `scipy.optimize.curve_fit`) to match the observed average-case timing data against 8 complexity models. Each model is scored using **R² (coefficient of determination)** — the model with the highest R² is selected as the best fit. Best-case and worst-case inputs are fitted independently, so their estimated complexity may differ from the average-case result.

| Complexity      | Description        |
|-----------------|--------------------|
| `O(1)`          | Constant           |
| `O(log n)`      | Logarithmic        |
| `O(n)`          | Linear             |
| `O(n log n)`    | Linearithmic       |
| `O(n²)`         | Quadratic          |
| `O(n² log n)`   | Quad-Linearithmic  |
| `O(n³)`         | Cubic              |
| `O(2ⁿ)`         | Exponential        |

---

## Example

**Input code:**

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

**Output:**

```
Detected Complexity: O(n²) — Quadratic  (~98% fit)

Best Case:    O(n)
Average Case: O(n²)
Worst Case:   O(n²)
```

A log-log performance graph will appear inside the app showing all three timing curves.

---

## License

MIT License. See `LICENSE` for details.
