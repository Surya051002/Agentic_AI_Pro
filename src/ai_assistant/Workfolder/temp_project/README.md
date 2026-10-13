# Simple Calculator

## Description
A lightweight, command‑line calculator written in Python that supports basic arithmetic operations (addition, subtraction, multiplication, division) as well as exponentiation. The tool parses user input, validates it, performs the requested operation, and prints the result. It is designed to be easy to extend with additional functions.

## Features
- **Addition** (`+`)
- **Subtraction** (`-`)
- **Multiplication** (`*`)
- **Division** (`/`) – handles division‑by‑zero with a friendly error message
- **Exponentiation** (`**`)
- Simple command‑line interface with input validation
- Easily extensible for more operations

## Installation
1. Clone the repository or download the source files.
2. Ensure you have Python 3.8+ installed.
3. Install the required dependencies (currently none, but a `requirements.txt` is provided for future extensions):

```bash
pip install -r requirements.txt
```

## Usage
Run the calculator script from the command line:

```bash
python calculator.py
```

You will be prompted to enter an expression in the following format:

```
<number> <operator> <number>
```

Examples:

```bash
> 5 + 3
Result: 8

> 10 / 2
Result: 5.0

> 2 ** 8
Result: 256
```

Supported operators:
- `+`  addition
- `-`  subtraction
- `*`  multiplication
- `/`  division
- `**` exponentiation

The program will continue to prompt for new expressions until you type `exit` or press `Ctrl+C`.

## Extending the Calculator
To add new operations:
1. Define a new function in **calculator.py** that performs the operation.
2. Add the operator symbol and the function reference to the `operations` dictionary inside `main()`.
3. Update the README with usage examples for the new operation.

## Testing Guide
Unit tests are located in the `tests/` directory (optional). To run the tests, install `pytest` (listed in `requirements.txt`) and execute:

```bash
pytest
```

The test suite covers:
- Correct results for each operation
- Handling of invalid input formats
- Division‑by‑zero protection

## License
This project is released under the MIT License.

---
*Happy calculating!*