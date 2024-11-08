import os
from src.dependency_resolver import parse_file, find_all_dependencies

def process_test_files():
    """
    Process all .txt files in the tests/test_data directory.
    
    This function:
    1. Checks if test_data directory exists
    2. Finds all .txt files in the directory
    3. Processes each file to determine library dependencies
    4. Prints the complete dependency tree for each library

    Returns:
        None
    """
    test_data_dir = os.path.join('tests', 'test_data')
    
    # Check if test directory exists
    if not os.path.exists(test_data_dir):   
        print(f"Error: Test data directory not found: {test_data_dir}")
        return
    
    # Get all .txt files
    test_files = [f for f in os.listdir(test_data_dir) if f.endswith('.txt')]
    
    # Check if any test files exist
    if not test_files:
        print(f"Error: No .txt files found in : {test_data_dir}")
        return
    
    # Process each test file
    for filename in sorted(test_files):
        filepath = os.path.join(test_data_dir, filename)
        try:
            print(f"\nProcessing: {filename}")
            print("-" * 50)
            
            deps, order = parse_file(filepath)

            # Print complete dependency tree for each library
            for lib in order:
                all_deps = find_all_dependencies(lib, deps)
                deps_str = " ".join(sorted(all_deps)) if all_deps else "no dependencies"
                print(f"{lib} depends on {deps_str}")

        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {str(e)}")
        print("-" * 50)

def main():
    process_test_files()

if __name__ == "__main__":
    main()