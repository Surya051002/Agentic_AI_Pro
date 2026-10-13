# calculator.py
"""Command-line calculator supporting basic arithmetic operations.

Usage:
    python calculator.py <num1> <operator> <num2>

Supported operators:
    +   addition
    -   subtraction
    *   multiplication
    /   division (division by zero is handled)
    **  exponentiation

Example:
    $ python calculator.py 5 * 3
    Result: 15

The script validates input, handles errors gracefully, and prints a helpful
message when usage is incorrect.
"""

import sys
from typing import Callable, Tuple

# ---------------------------------------------------------------------------
# Arithmetic operation implementations
# ---------------------------------------------------------------------------

def add(a: float, b: float) -> float:
    """Return the sum of *a* and *b*."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of *a* and *b* (a - b)."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of *a* and *b*."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of *a* divided by *b*.

    Raises:
        ZeroDivisionError: If *b* is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero is undefined.")
    return a / b


def power(a: float, b: float) -> float:
    """Return *a* raised to the power of *b* (a ** b)."""
    return a ** b

# Mapping of operator symbols to their corresponding functions
OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_arguments(args: list[str]) -> Tuple[float, str, float]:
    """Parse command‑line arguments.

    Expected format: ``<num1> <operator> <num2>``.
    Returns a tuple ``(num1, operator, num2)`` where the numbers are converted
    to ``float``.

    Raises:
        ValueError: If the number of arguments is incorrect or conversion fails.
        KeyError:   If the operator is not supported.
    """
    if len(args) != 3:
        raise ValueError(
            "Incorrect number of arguments. Expected format: <num1> <operator> <num2>."
        )

    raw_a, operator, raw_b = args

    # Validate operator early to give a clear message
    if operator not in OPERATIONS:
        raise KeyError(f"Unsupported operator '{operator}'. Supported: {', '.join(OPERATIONS)}")

    try:
        a = float(raw_a)
        b = float(raw_b)
    except ValueError as exc:
        raise ValueError("Both operands must be numeric.") from exc

    return a, operator, b


def calculate(a: float, operator: str, b: float) -> float:
    """Execute the arithmetic operation.

    This function simply looks up the appropriate callable from ``OPERATIONS``
    and invokes it. Any exception raised by the operation (e.g., ``ZeroDivisionError``)
    propagates to the caller so that it can be handled uniformly.
    """
    operation = OPERATIONS[operator]
    return operation(a, b)

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the command‑line interface.

    The function extracts arguments from ``sys.argv``, performs validation,
    runs the calculation, and prints the result. All expected errors are caught
    and displayed to the user without a full traceback, keeping the UX clean.
    """
    try:
        # ``sys.argv[0]`` is the script name; the rest are user‑provided arguments.
        a, operator, b = parse_arguments(sys.argv[1:])
        result = calculate(a, operator, b)
        # Remove trailing ``.0`` for integer‑like results for nicer output.
        if result.is_integer():
            result_str = str(int(result))
        else:
            result_str = str(result)
        print(f"Result: {result_str}")
    except ValueError as ve:
        print(f"Input error: {ve}")
        print("Usage: python calculator.py <num1> <operator> <num2>")
    except KeyError as ke:
        print(f"Operator error: {ke}")
        print("Supported operators: ", ", ".join(OPERATIONS))
    except ZeroDivisionError as zde:
        print(f"Math error: {zde}")
    except Exception as e:  # Catch‑all for unexpected issues
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
