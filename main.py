import sys
from src.dependency_resolver import parse_file, find_all_dependencies

def process_file(filepath):
    """
    Process a single dependency file and print the complete dependency tree.
    
    Args:
        filepath (str): Path to the input file

    Returns:
        None
    """
    try:
        # Parse file and get dependencies
        deps, order = parse_file(filepath)

        # Process and print dependencies for each library
        for lib in order:
            all_deps = find_all_dependencies(lib, deps)
            deps_str = " ".join(all_deps) if all_deps else "no dependencies"
            print(f"{lib} depends on {deps_str}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)  

def main():
    # Check if input file is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        print("Example: python main.py input.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    print(f"\nProcessing: {input_file}")
    print("-" * 50)
    process_file(input_file)

if __name__ == "__main__":
    main()