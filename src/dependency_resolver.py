import os

def parse_file(filepath):
    """
    Parse a dependency file and return dependencies and their order.
    
    Args:
        filepath (str): Path to the input file.
        
    Returns:
        tuple: (dependencies, library_order)
            - dependencies (dict): Dictionary mapping libraries to their dependencies
            - library_order (list): List of libraries in order of appearance
    """
    dependencies = {}
    library_order = []
    
    filepath = os.path.normpath(filepath)

    # if fild does not exist
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    # if file is empty
    if os.path.getsize(filepath) == 0:
        return {}, []

        
    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file,1):
            # Skip empty lines or lines with only whitespace
            if not line.strip():
                continue

            try:
                # normalize multiple spaces
                normalized_line = ' '.join(line.split())
            
                # checking basic formatting
                if 'depends on' not in normalized_line:
                    raise ValueError(f"Line {line_num}: Missing 'depends on' separator")

                parts = normalized_line.strip().split('depends on')
                if len(parts) != 2:
                    raise ValueError(f"Line {line_num}: Line must have exactly one 'depends on' separator") 

                # Validate library name
                library = parts[0].strip()
                if not library:
                    raise ValueError(f"Line {line_num}: Library name cannot be empty")
                if not library.isalnum():
                    raise ValueError(f"Line {line_num}: {library} name must be alphanumeric")


                # Parse and validate dependencies
                deps = []
                for dep in parts[1].strip().split():
                    # skip empty dependencies
                    if not dep:
                        continue

                    # check dependency name
                    if not dep.isalnum():
                        raise ValueError(f"Line {line_num}: Dependency {dep} name must be alphanumeric")
                    
                    # check self dependency
                    if dep == library:
                        raise ValueError(f"Line {line_num}: Self dependency not allowed. '{library}' cannot depend on itself")

                    # Add dependency if not already present
                    if dep and dep not in deps:  
                        deps.append(dep)

                # Add library to order if first appearance
                if library not in dependencies:
                    library_order.append(library)
                
                # Store dependencies
                dependencies[library] = deps

            except ValueError as e:
                raise ValueError(f"Error in {filepath}, Line {line_num}: {str(e)}")

    return dependencies, library_order



def find_all_dependencies(library, dependencies):
    """
    Find all dependencies (direct + transitive) for a given library.
    
    Args:
        library (str): The library to find dependencies for
        dependencies (dict): Dictionary of direct dependencies
        
    Returns:
        set: Complete set of all dependencies for the given library
    """

    if library not in dependencies:
        return set()

    all_deps = set()    # To store all dependencies
    stack = [library]   # Stack of libraries to process
    visited = set()     # To track visited libraries

    while stack:
        current_lib = stack.pop()

        if current_lib not in dependencies:
            continue

        # Process each direct dependency of current library
        for dep in dependencies[current_lib]:
            if dep not in visited:
                visited.add(dep)
                stack.append(dep)

            # Add to final dependencies if not the original library
            if dep != library:
                all_deps.add(dep)
    
    return all_deps


