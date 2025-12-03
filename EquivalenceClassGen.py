import ast
import inspect
import sys

# ==========================================
# Test module
# ==========================================
def determine_price(age):
    """
    Assumptions:
    - Input is an integer.
    - Logic handles various age ranges.
    """
    if age < 0:
        return "Invalid Age"
    elif age < 3:
        return "Free (Infant)"
    elif age <= 12:
        return "Child Price"
    elif age < 60:
        return "Adult Price"
    else:
        return "Senior Price"

# ==========================================
# 2. The Equivalence Class Generator
# ==========================================
class BoundaryExtractor(ast.NodeVisitor):
    """
    Parses Python code to find integer comparison boundaries.
    """
    def __init__(self):
        self.boundaries = set()

    def visit_Compare(self, node):
        # Look for comparisons like: if age < 18
        # We assume the variable is on the left and a number is on the right for simplicity
        # e.g., "age < 18" or "age >= 65"
        
        # Check if the right side is a number
        for comparator in node.comparators:
            if isinstance(comparator, ast.Constant) and isinstance(comparator.value, (int, float)):
                self.boundaries.add(comparator.value)
        
        # Continue visiting child nodes
        self.generic_visit(node)

def generate_equivalence_classes(func_to_analyze):
    print(f"--- Analyzing Function: '{func_to_analyze.__name__}' ---")
    
    try:
        source_code = inspect.getsource(func_to_analyze)
    except OSError:
        print("Error: Could not retrieve source code.")
        return

    tree = ast.parse(source_code)

    extractor = BoundaryExtractor()
    extractor.visit(tree)
    
    sorted_boundaries = sorted(list(extractor.boundaries))
    
    if not sorted_boundaries:
        print("No boundaries found. The function might not use integer comparisons.")
        return

    print(f"Found Boundaries in code: {sorted_boundaries}\n")

    # 4. Generate Equivalence Partitions (Ranges)
    # We create ranges based on the sorted boundaries.
    # If boundaries are [0, 18], partitions are: (<0), [0, 18), (>=18)
    
    partitions = []
    # Partition 1: Below the lowest boundary
    first_b = sorted_boundaries[0]
    partitions.append({
        "class_name": f"Value < {first_b}",
        "representative_value": first_b - 5, # Arbitrary offset
        "type": "Invalid/Low"
    })

    # Partition 2: Between boundaries
    for i in range(len(sorted_boundaries) - 1):
        low = sorted_boundaries[i]
        high = sorted_boundaries[i+1]
        
        # Calculate a middle point for the representative value
        mid_point = (low + high) // 2
        
        partitions.append({
            "class_name": f"{low} <= Value < {high}",
            "representative_value": mid_point,
            "type": "Valid/Mid-range"
        })

    # Partition 3: Above the highest boundary
    last_b = sorted_boundaries[-1]
    partitions.append({
        "class_name": f"Value >= {last_b}",
        "representative_value": last_b + 5, # Arbitrary offset
        "type": "Valid/High"
    })

    # 5. Output the Test Cases
    print(f"{'EQUIVALENCE CLASS':<30} | {'TEST INPUT':<12} | {'EXPECTED BEHAVIOR (Prediction)'}")
    
    for p in partitions:
        # We actually run the function with the generated input to see what happens
        try:
            actual_output = func_to_analyze(p['representative_value'])
        except Exception as e:
            actual_output = f"Error: {e}"

        print(f"{p['class_name']:<30} | {str(p['representative_value']):<12} | {actual_output}")

if __name__ == "__main__":
    generate_equivalence_classes(determine_price)
