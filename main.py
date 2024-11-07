import os
from pathlib import Path
from src.dependency_resolver import parse_file, find_all_dependencies


def process_test_files():
    test_data_dir = os.path.join('tests', 'test_data')

    if not os.path.exists(test_data_dir):   
        print(f"Error: Test data directory not found: {test_data_dir}")
        return
    
    test_files = [f for f in os.listdir(test_data_dir) if f.endswith('.txt')]

    if not test_files:
        print(f"Error: No .txt files found in : {test_data_dir}")
        return
    

    for filename in sorted(test_files):
        filepath = os.path.join(test_data_dir, filename)
        try:
            print(f"Processing: {filename}")
            print("----------------------------------")

            deps, order = parse_file(filepath)
            for lib in order:
                all_deps = find_all_dependencies(lib, deps)
                deps_str = " ".join(sorted(all_deps)) if all_deps else "no dependencies"
                print(f"{lib} depends on {deps_str}")

        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {str(e)}")
        
        print("---------------\n\n")


def main():
    process_test_files()


if __name__ == "__main__":
    main()