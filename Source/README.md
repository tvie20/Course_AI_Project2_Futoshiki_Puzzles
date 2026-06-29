# Futoshiki Puzzle Project

This project contains the Futoshiki puzzle solver, KB/CNF generation modules, a simple GUI, and an automated test suite.

## Requirements

- Python 3.9+
- Tkinter (usually included with Python on Windows)

## Run the GUI

From the project root, go to the Source folder and run:

```bash
cd Source
py -3.9 gui.py
```

If your machine uses `python` instead of `py`, use:

```bash
cd Source
python gui.py
```

## Run the test suite

From the project root, run:

```bash
cd Source/test
python run_tests.py
```

You can also pass custom limits:

```bash
cd Source/test
python run_tests.py --time-limit 300 --max-expansions 5000000 --max-inferences 5000000
```

To see all available options:

```bash
cd Source/test
python run_tests.py --help
```

## Run the KB / CNF module tests

If you want to test the knowledge-base generation and CNF export flow:

```bash
cd Source
py -3.9 test_kb.py
```

## Export CNF files

To export CNF inputs for all puzzle files:

```bash
cd Source
py -3.9 export_cnf.py
```

The exported files will be placed in the CNF folder.
