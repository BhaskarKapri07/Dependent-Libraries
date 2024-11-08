import os

def parse_file(filepath):
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

                library = parts[0].strip()
                if not library:
                    raise ValueError(f"Line {line_num}: Library name cannot be empty")
                if not library.isalnum():
                    raise ValueError(f"Line {line_num}: {library} name must be alphanumeric")



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

                    if dep and dep not in deps:  
                        deps.append(dep)

                if library not in dependencies:
                    library_order.append(library)
                
                dependencies[library] = deps

            except ValueError as e:
                raise ValueError(f"Error in {filepath}, Line {line_num}: {str(e)}")

    return dependencies, library_order



def find_all_dependencies(library, dependencies):
    # print("----INSIDE FIND ALL DEPENDENCIES")
    # print(f"\nLibrary: {library}")
    # print(f"\nDependencies: {dependencies}")

    if library not in dependencies:
        return set()

    all_deps = set()
    stack = [library]
    visited = set()


    while stack:
        current_lib = stack.pop()
        # print(f"\nCurrent Library: {current_lib}")

        if current_lib not in dependencies:
            continue

        for dep in dependencies[current_lib]:
            # print(f"\nDependency: {dep}")
            if dep not in visited:
                visited.add(dep)
                stack.append(dep)


            if dep != library:
                all_deps.add(dep)
    
    return all_deps


