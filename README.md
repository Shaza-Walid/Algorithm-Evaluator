# Algorithm Performance Evaluator

A desktop GUI application that analyzes the runtime performance of user-written Python algorithms, plots execution time graphs, and estimates their Big-O complexity automatically.

---

## Features

- **Auto Mode** – Automatically tests your algorithm against multiple input sizes (`10, 100, 300, 700, 1000`) and measures execution time for each.
- **Manual Mode** – Run your algorithm once against a custom array you provide, and see the exact execution time.
- **Big-O Estimation** – Automatically classifies your algorithm's complexity as `O(1)`, `O(n)`, `O(n log n)`, `O(n²)`, or `O(2^n)` based on observed timing ratios.
- **Performance Graph** – Displays a matplotlib plot of input size vs. execution time in Auto Mode.
- **Simple GUI** – Clean Tkinter interface requiring no command-line interaction.

---

## Project Structure

```
├── main.py          # Entry point — launches the GUI
├── gui.py           # Tkinter UI definition and event handling
├── evaluator.py     # Core logic: code execution, timing, Big-O estimation, plotting
└── requirements.txt # Python dependencies
```

---

## Requirements

- Python 3.x
- `matplotlib`

Install dependencies with:

```bash
pip install -r requirements.txt
```

> `tkinter` is included with most standard Python installations. If it's missing, install it via your OS package manager (e.g., `sudo apt install python3-tk` on Ubuntu/Debian).

---

## Getting Started

```bash
git clone https://github.com/Shaza-Walid/Algorithm-Evaluator.git
cd algorithm-performance-evaluator
pip install -r requirements.txt
python main.py
```

---

## How to Use

1. **Launch the app** by running `python main.py`.
2. **Enter your algorithm** in the text area. Your code must define a function that accepts a list as its single argument. Example:

   ```python
   def my_sort(arr):
       return sorted(arr)
   ```

3. **Choose a mode:**
   - **Auto Mode** – The app runs your function against 5 increasing input sizes and plots the results.
   - **Manual Mode** – Enter a comma-separated array (e.g., `5, 3, 8, 1`) and run your function once against it.

4. **Click "Run Analysis"** to see the result.

---

## Big-O Estimation Logic

In Auto Mode, the evaluator computes timing ratios between consecutive input sizes. The average ratio is mapped to a complexity class:

| Average Ratio | Estimated Complexity |
|---------------|----------------------|
| < 1.5         | O(1)                 |
| < 3           | O(n)                 |
| < 6           | O(n log n)           |
| < 15          | O(n²)                |
| ≥ 15          | O(2^n) or higher     |

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
Estimated Complexity: O(n^2)
```

A performance graph will also appear showing the time curve.

---

## License

MIT License. See `LICENSE` for details.
