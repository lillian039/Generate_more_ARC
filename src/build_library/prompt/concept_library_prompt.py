system_prompt = """
You are an experts professor in a university, and you are tasked with creating a new course on a unique concept called 'Grid Transformation'.
You are going to create new tasks for grid transformation, and you need to define the key concepts and terms for the course.
The input and output grids are represented by matrices, where each cell contains a color represented by a number.    

The corresponding relationship between colors and numbers is delimited by triple backticks as follows.

```
0: black, 1: blue, 2: red, 3: green, 4: yellow, 5: gray, 6: magenta, 7: orange, 8: aqua, 9: maroon
```

Here is a list of object definitions for the transformation.
```
1. Grid: A structured arrangement of cells in rows and columns used as the workspace for transformations.
2. Object: Any distinguishable element within the grid, characterized by properties like color, shape, or size.
3. Color Block/Shape: A specifically colored area on the grid, which could hold significance in the transformation process.
4. Pattern: A reoccurring design or sequence within the grid which could guide transformations.
5. Border: A visual boundary around an object or color block often used to distinguish or highlight.
6. Pixel: The smallest unit within the grid that can be independently modified or identified.
7. Cluster: A group of connected objects which share similar characteristics and are handled as a single unit during transformations.
8. Diagonal Line: A line or sequence that propagates diagonally across the grid providing directional layout for object transformations.
9. Corner: A point where two or more grid boundaries meet, often used as reference points for transformation.
10. Alignment: The arrangement or positioning of objects based on predefined conditions (horizontal, vertical).
11. Block (as an object cluster): A collection of adjacent cells of the same color surrounded by different colors or grid edges.
12. Sequence: An order or chain in which objects follow, often considered for transforming or reproducing similar patterns throughout the grid.
```

Here is a list of transformation definitions for the course.
```
1. Replication of patterns/colors from the input grid to specific locations within the output grid.
2. Rotation and mirroring of elements across axes for symmetry or new orientation.
3. Resizing grid dimensions with structural changes such as expansion, reduction, or extraction of specific sections.
4. Movement of elements vertically or horizontally, including cycling of out-of-bound elements to the opposite side.
5. Overlaying multiple patterns with transparency rules, creating composite designs from multiple different areas or layers.
6. Filling and coloring specific cells or patterns based on positional rules, distinctive shapes, or adjacency considerations.
7. Shifting of color properties or shapes to new positions, often with conditional rules for non-movement.
8. Direct duplication or mirroring of entire grids or segments to multiple sections of a larger grid.
9. Systematic color additions or replacements adhering to spatial configurations or pattern-dominance criteria.
10. Application of fixed, strategic positions for colored objects based on counted quantities or predefined positions.
```

You can refer to these definitions while creating tasks for the course.
"""

def get_content_prompt(task_list, generate_number):
        content_prompt = ""
        for i, task in enumerate(task_list):
                content_prompt += f"Task {i+1}:\n"
                content_prompt += task + '\n\n'

        content_prompt = content_prompt.strip()

        generate_prompt = ""
        for i in range(generate_number):
                generate_prompt += f"Task {i+1}:\n[Your Task Here]\n\n"
        generate_prompt = generate_prompt.strip()
        content = f"""
You are an expert in the field of Grid Transformation and have been invited to design new tasks. You can generate your tasks based on the following examples but should be different.

{content_prompt}

Please generate the new tasks in the following format. Feel free to be creative and innovative in your task designs, you can refer to the concept library and the given examples:

{generate_prompt}

The rule should be clear, concise, and easy to understand for the students. The steps should be no more than three.
"""
        return content
content_prompt = """
You are an expert in the field of Grid Transformation and have been invited to design new tasks. You can generate your tasks based on the following examples but should be different.

Task 1:
Step 1: Identify all black areas within the gray objects on the input grid.
Step 2: Check the shape of each identified black area.
Step 3: If the black area is a square, fill it with red color.
Step 4: If the black area is not a square, do not change the color; leave it black.
Step 5: Retain the original size of the grid and proceed to reflect these changes on the output grid.

Task 2:
Rule:
Step 1: Examine the 3x3 input grid and count the number of squares for each color present.
Step 2: Identify the color that appears most frequently in the input grid.
Step 3: Fill every square of the 3x3 output grid with the color identified in step 2, making the output grid consist of a single, uniform color.

Task 3:
step 1: Identify the colors present in each column of the 3x3 grid.
step 2: For each cell in a column, check the colors:
        - If a cell is grey, change the color to dark blue.
        - If a cell is dark blue, change the color to grey.
        - If a cell is light blue, change the color to dark red.
        - If a cell is dark red, change the color to light blue.
        - If a cell is magenta, change the color to light red.
        - If a cell is light red, change the color to magenta.
        - If a cell is green, change the color to yellow.
        - If a cell is yellow, change the color to green.
step 3: Apply the color changes for each cell based on the identifications from step 2 to produce the output grid.

Task 4:
Step 1: Count the number of squares filled with each different color in the grid.
Step 2: Identify the color that fills the most squares.
Step 3: Change the color of all squares that are not of the most frequently occurring color to gray.
Step 4: Keep the squares with the most frequently occurring color unchanged.

Task 5:
Step 1: Identify all the blue squares in the grid.
Step 2: Locate the incomplete rectangle or square structure which is partially formed by light blue blocks.
Step 3: Replace the blue squares with green squares to complete the rectangle or square when necessary, ensuring that the final shape is geometrically correct.
Step 4: Ensure the integrity of the grid shape matches the input grid size, specifically maintaining the same number of rows and columns.

Task 6:
[Your Task Here]

Task 7:
[Your Task Here]

Task 8:
[Your Task Here]

Task 9:
[Your Task Here]

Task 10:
[Your Task Here]

The rule should be clear, concise, and easy to understand for the students. The steps should be no more than three.
"""