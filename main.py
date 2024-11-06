import os

def parse_file(filepath):
    try:
        filepath = os.path.normpath(filepath)

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Input file not found: {filepath}")
        
        with open(filepath, 'r') as file:
            for line in file:
                if not line.strip():
                    continue

                try:
                    parts = line.strip().split('depends on')
                    if len(parts) != 2:
                        raise ValueError(f"Invalid format: {line.strip()}")
                    
                    library = parts[0].strip()
                    dependencies = set(parts[1].strip().split())
                    

                    print(f"Library: {library}, Dependencies: {dependencies}")

                except Exception as e:
                    print(f"Error processing line: {line.strip()}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")


test_files = ["INPUT1.txt", "INPUT2.txt", "INPUT3.txt",]
for file in test_files:
    print(f"Processing: {file}")
    parse_file(file)
    print("\n---------------------------\n")