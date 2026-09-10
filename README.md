# Enhanced LEM1 Rule Induction

A Python implementation of an enhanced LEM1-style rule-induction algorithm using rough-set approximations.

The program processes decision tables, identifies consistent and inconsistent cases, and generates human-readable **certain** and **possible** decision rules. It also extends the basic approach by converting numerical attributes into intervals using calculated cut points.

> **Project status:** This academic project was originally developed in 2017. Its documentation was refreshed later to explain the implementation and limitations more clearly.

## Features

* Reads structured decision-table datasets
* Supports categorical and numerical condition attributes
* Discretizes numerical values using candidate cut points
* Constructs equivalence classes for attribute-value combinations
* Calculates lower approximations for certain classifications
* Calculates upper approximations for possible classifications
* Removes unnecessary attributes and rule conditions
* Generates separate files for certain and possible rules
* Includes sample datasets and example outputs

## How It Works

1. The input decision table is parsed into condition attributes and a decision attribute.
2. Numerical attributes are converted into value intervals.
3. Cases with equivalent condition values are grouped into equivalence classes.
4. Decision concepts are identified from the final column.
5. Lower approximations are calculated to identify cases that certainly belong to a concept.
6. Upper approximations are calculated for inconsistent data to identify cases that possibly belong to a concept.
7. Redundant attributes and conditions are removed.
8. The resulting rules are written to separate output files.

## Technology Stack

* Python
* NumPy
* Pandas

## Running the Project

### Prerequisites

Install Python and the required packages:

```bash
pip install numpy pandas
```

### Execution

1. Clone the repository:

   ```bash
   git clone https://github.com/TejaJag/Enhanced_Lem1.git
   cd Enhanced_Lem1
   ```

2. Run the program:

   ```bash
   python Lem1.py
   ```

3. Enter the name of an input dataset located in the current directory.

4. Enter a base name for the output files.

The program produces:

```text
<output-name>.certain.r
<output-name>.possible.r
```

The `certain` file contains rules derived from lower approximations. The `possible` file contains rules derived from upper approximations when the decision table is inconsistent.

## Example Datasets

The repository includes sample inputs such as:

* `bowl.txt`
* `iris.txt`
* `test.txt`
* `test2.txt`

Corresponding generated-rule files are included for reference.

## Current Limitations

* The implementation is contained in a single script.
* The input format requires a specific decision-table structure.
* The code was written against older NumPy versions and may require replacing deprecated `np.float` references with `float` for modern NumPy.
* Automated tests and dependency-version configuration are not yet included.
* The implementation is intended for educational and experimental use rather than production workloads.

## Possible Improvements

* Separate parsing, discretization, approximation, and rule-generation logic into modules
* Add command-line arguments instead of interactive prompts
* Add unit tests for consistent and inconsistent decision tables
* Replace deprecated NumPy types
* Add formal evaluation of rule coverage and accuracy
* Package the project with explicit dependency versions
