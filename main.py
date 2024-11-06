import os

def parse_file(filepath):
    dependencies = {}
    library_order = []
    
    filepath = os.path.normpath(filepath)

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")
        
    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file,1):
            if not line.strip():
                continue

            try:
                parts = line.strip().split('depends on')
                if len(parts) != 2:
                    raise ValueError(f"Line {line_num}: Missing 'depends on' separator") 

                library = parts[0].strip()
                if not library:
                    raise ValueError(f"Line {line_num}: Empty library name")

                if library not in dependencies:
                    library_order.append(library)


                deps = []
                for dep in parts[1].strip().split():
                    if dep and dep not in deps:  
                        deps.append(dep)

                dependencies[library] = deps

            except ValueError as e:
                raise ValueError(f"Error in {filepath}, {str(e)}")

    return dependencies, library_order



test_files = ["INPUT1.txt", "INPUT2.txt", "INPUT3.txt"]
for file in test_files:
    try:
        print(f"Processing: {file}")
        deps, order = parse_file(file)
        print(f"Dependencies: {deps}")
        print(f"Order: {order}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {str(e)}")
    print("\n---------------------------\n")
