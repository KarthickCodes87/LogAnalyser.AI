# LogAnalyser.AI
Analyse simple python code and generate Equivalence classes

**Assumptions**

The input is a simple Python function.
The function takes exactly one integer argument. This can be extended later
We are looking for boundaries defined in if/elif statements to create our partitions.

**How it works**

Introspection: 
  It uses inspect to grab the actual source code text of the determine_ticket_price function at runtime.

AST Parsing: 
  It parses that text into a Python logic tree.
  
Boundary Extraction: 
  It looks for "Compare" nodes (nodes where > or < are used) and extracts the numbers (0, 3, 12, 60).

Partitioning: 
  It treats those numbers as the "walls" between rooms.
If the walls are 0 and 18, the "rooms" (Equivalence Classes) are everything below 0, everything between 0 and 18, and everything above 18.

Test Generation: 
  It picks a number that sits safely inside each "room" (e.g., halfway between 0 and 18) to act as the representative test case.
