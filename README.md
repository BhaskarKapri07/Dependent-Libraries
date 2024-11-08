# Library Dependency Resolver

This is the Round 2 programming assignment for the Software Engineering role. It implements a tool that figures out which software libraries depend on which other software libraries, handling both direct and transitive dependencies.


## Project Structure
```
Dependent-Libraries/
├── src/
│   ├── __init__.py
│   └── dependency_resolver.py
├── tests/
│   ├── __init__.py
│   ├── unit_tests.py
│   └── test_data/
│       ├── INPUT1.txt  
│       ├── INPUT2.txt
│       └── INPUT3.txt
├── main.py
├── test_runner.py
└── README.MD
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/BhaskarKapri07/Dependent-Libraries.git
cd Dependent-Libraries
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On Unix/MacOS
python -m venv .venv
source .venv/bin/activate
```

## Usage

The program takes the input file path as a command line argument through `main.py`.

### Running the Program
1. Open your terminal/command prompt
2. Navigate to the project directory
3. Run the following command:
```bash
python main.py <input_file>
```
where <input_file> is the path to your input file containing library dependencies.

### Examples

1. If your input file is in the current directory:
```bash
python main.py input.txt
```

2. If your input file is in a different directory, provide the path to it:
```bash
python main.py path/to/your/input.txt
```

If no input file is provided or the file is not found, you'll see:
```
Usage: python main.py <input_file>
Example: python main.py input.txt
```

**Note: The file path must be provided as a command line argument when running the program.**


### Input Format
- Each line must follow the format: `<library> depends on [dependencies...]`
- Library names must be alphanumeric
- Dependencies are optional (a library can have no dependencies)
- Multiple dependencies are space-separated

Example input:
```
A depends on B C
B depends on C E
C depends on G
D depends on A F
E depends on F
F depends on H
```

### Output Format
For each library, outputs its complete set of dependencies (both direct and transitive).

Example output:
```
A depends on B C E F G H
B depends on C E F G H
C depends on G
D depends on A B C E F G H
E depends on F H
F depends on H

```

## Running Tests

Run all unit tests:
```bash
python -m unittest -v tests/unit_tests.py
```

For individual test classes:
```bash
python -m unittest -v tests.unit_tests.TestDependencyParser
python -m unittest -v tests.unit_tests.TestDependencyResolver
```

You can also use `test_runner.py` which processes all .txt files in the `tests/test_data` directory:

```bash
python test_runner.py
```

This will process all test files and display the results for each file sequentially.

## Design Decisions and Assumptions

### 1. Error Handling Strategy
- **Strict Validation**: The program fails fast on first error encountered
- **Rationale**: In a production environment, partial or incorrect dependencies could lead to serious issues. Better to fail early and explicitly than to process potentially incomplete data.

### 2. Input Processing
- **Case Sensitivity**: Library names are case-sensitive (e.g., 'A' and 'a' are different libraries)
- **Whitespace Handling**: Multiple spaces are normalized to single spaces
- **Empty Lines**: Skipped during processing
- **Line Format**: Strict enforcement of "<library> depends on [dependencies...]" format

### 3. Dependency Resolution
- **Missing Dependencies**: Treated as valid (might be external dependencies)
- **Self Dependencies**: Not allowed (raises error)
- **Duplicate Declarations**: Uses last declaration, maintains original order

## Edge Cases Handled

1. **File-Related Cases**
   - Empty files
   - Non-existent files

2. **Syntax Cases**
   - Missing "depends on" separator
   - Invalid library names (non-alphanumeric)
   - Extra whitespace variations
   - Empty dependency lists
   - Duplicate dependencies in same line

3. **Dependency Cases**
   - Circular dependencies
   - Self dependencies
   - Missing/undefined dependencies
   - Duplicate library declarations
   - Transitive dependencies

## Test Cases

1. **Basic Functionality Tests**
   - Single dependency parsing
   - Multiple dependencies parsing
   - Multiple lines parsing
   - Empty file handling
   - Whitespace variation handling

2. **Error Case Tests**
   - Invalid syntax detection
   - Invalid character detection
   - Self dependency detection
   - File not found handling

3. **Dependency Resolution Tests**
   - Direct dependency resolution
   - Transitive dependency resolution
   - Circular dependency handling
   - Missing dependency handling
   - Complex dependency chain resolution
   - Duplicate dependency handling

## Production Considerations

1. **Reliability**
   - Comprehensive error handling
   - No partial processing of invalid files
   - Clear error messages with line numbers
   - Robust handling of edge cases

2. **Maintainability**
   - Clear code structure
   - Comprehensive documentation
   - Thorough test coverage
   - Consistent coding style

3. **Performance**
   - Efficient dependency resolution using iterative approach
   - Minimal memory usage
   - Handles large dependency chains



