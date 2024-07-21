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

system_prompt_abc = """
You are an experts professor in a university, and you are tasked with creating a new course on a unique concept called 'Grid Transformation'.
You are going to create new tasks for grid transformation, and you need to define the key concepts and terms for the course.
The input and output grids are represented by matrices, where each cell contains a color. All colors are listed as follows: black, blue, red, green, yellow, gray, magenta, orange, aqua, maroon.

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

def get_prompt_for_hypotheses1(transformed_list, original_hypo):
        return f"""
Please generate hypotheses for the given input images.

{transformed_list}

This is the original transformation hypothesis. Please generate new hypotheses based on the given examples.
The hypotheses must be executable on the given input examples. Include necessary imports in the function.
The hypotheses should be different from the original hypothesis, and different from each other. Utilize the transformation definitions in the concept library.
Hypothesis 1 for the given input images:
{original_hypo}

Hypothesis 2 for the given input images:
[Hypothesis 2]

```python
def transform_grid(input_grid: np.ndarray[int]) -> np.ndarray[int]:
    # Your code here, apply your transformation hypothesis to the input
    return output
```

Hypothesis 3 for the given input images:
[Hypothesis 3]

```python
def transform_grid(input_grid: np.ndarray[int]) -> np.ndarray[int]:
    # Your code here, apply your transformation hypothesis to the input
    return output
```

The generated hypotheses should be no more than one sentence long.
"""     

def get_prompt_for_hypotheses2(transformed_list, hint):
        hint_str = ""
        for i, h in enumerate(hint):
                hint_str += f"{i}. {h}\n"
        return f"""
Please generate hypotheses for the given input images.

{transformed_list}

This is the original transformation hypothesis. Please generate new hypotheses based on the given examples.
The hypotheses must be executable on the given input examples. Include necessary imports in the function.
The hypothese must include the following hint:
{hint_str}

You can do various combinations and add more modification of transformations to generate new hypotheses. Differentiate the hypotheses from each other.

Hypothesis 1 for the given input images:
[Hypothesis 1]

```python
def transform_grid(input_grid: np.ndarray[int]) -> np.ndarray[int]:
    # Hypothesis
    # Your code here, apply your transformation hypothesis to the input
    
    return output
```

Hypothesis 2 for the given input images:
[Hypothesis 2]

```python
def transform_grid(input_grid: np.ndarray[int]) -> np.ndarray[int]:
    # Hypothesis
    # Your code here, apply your transformation hypothesis to the input
    return output
```

Hypothesis 3 for the given input images:
[Hypothesis 3]

```python
def transform_grid(input_grid: np.ndarray[int]) -> np.ndarray[int]:
    # Hypothesis
    # Your code here, apply your transformation hypothesis to the input
    return output
```
The generated hypotheses should be no more than one sentence long.
"""     


def get_library_example_prompt(number=1):
        example_1 = """
Task 1
Description 1
In the input, you should see: a design with lines and empty squares.
The output grid size: stays the same.
To make the output, you have to: look at the color that form the design in the input.Find any empty areas of blocks that are enclosed by the lines that form the main design, fill them yellow.You should end with the same original design from the input, but with the empty areas filled yellow.

Description 2
In the input, you should see: A random green pattern
The output grid size: Remains the same as the input size
To make the output, you have to: Fill each enclosed hole with yellow

Description 3
In the input, you should see: green pixels in a random pattern.
The output grid size: is the same as the input grid size.
To make the output, you have to: .copy the input grid and then fill in each area or pixel enclosed by green pixels with yellow.

Definition about the objects:
1. Enclosed area: a region of the grid that is surrounded by a specific color or pattern.

Grid size:
1. remain the same

Crucial concepts about the transformation:
1. Fill the enclosed area with a specific color.
"""

        example_2 = """
Task 1
Description 1
In the input, you should see: a design with lines and empty squares.
The output grid size: stays the same.
To make the output, you have to: look at the color that form the design in the input.Find any empty areas of blocks that are enclosed by the lines that form the main design, fill them yellow.You should end with the same original design from the input, but with the empty areas filled yellow.

Description 2
In the input, you should see: A random green pattern
The output grid size: Remains the same as the input size
To make the output, you have to: Fill each enclosed hole with yellow

Description 3
In the input, you should see: green pixels in a random pattern.
The output grid size: is the same as the input grid size.
To make the output, you have to: .copy the input grid and then fill in each area or pixel enclosed by green pixels with yellow.

Task 2
Description 1
In the input, you should see: a gray grid with 9 different smaller squares with various color block patterns.
The output grid size: remains the same.
To make the output, you have to: find the square that has only four color blocks in the pattern. Use that design to fill the blocks in the output design. The gray areas stay the same.

Definition about the objects:
1. Enclosed area: a region of the grid that is surrounded by a specific color or pattern.
2. Suqares that are seperated by grid.

Grid size:
1. remain the same

Crucial concepts about the transformation:
1. Fill the enclosed area with a specific color.
2. Count the number of pixels.
3. Find one specific pattern and use it to fill the rest of the grid.
"""
        example_3 = """
Task 1
```
Description 1
In the input, you should see: a design with lines and empty squares.
The output grid size: stays the same.
To make the output, you have to: look at the color that form the design in the input.Find any empty areas of blocks that are enclosed by the lines that form the main design, fill them yellow.You should end with the same original design from the input, but with the empty areas filled yellow.

Description 2
In the input, you should see: A random green pattern
The output grid size: Remains the same as the input size
To make the output, you have to: Fill each enclosed hole with yellow

Description 3
In the input, you should see: green pixels in a random pattern.
The output grid size: is the same as the input grid size.
To make the output, you have to: .copy the input grid and then fill in each area or pixel enclosed by green pixels with yellow.
```

Task 2
```
Description 1
In the input, you should see: a gray grid with 9 different smaller squares with various color block patterns.
The output grid size: remains the same.
To make the output, you have to: find the square that has only four color blocks in the pattern. Use that design to fill the blocks in the output design. The gray areas stay the same.
```

Task 3
```
Description 1
In the input, you should see: A grid with colored pixels.
The output grid size: Is twice as large as the input, so a 2x2 becomes 4x4 and a 3x3 becomes 6x6 and so on.
To make the output, you have to: Create a grid twice the size of the input. Divide the output grid into 4 quadrants. Replicate the input grid pixels in the upper right quad. In the upper left quad, place the input grid that's been rotated clockwise 90 degrees. In the lower right quad, place the input grid colored pixels that has been rotated 180 degrees. In the lower left quad place a copy of the input grid that's been rotated 90 degrees COUNTER-CLOCKWISE. Done.
```

Definition about the objects:
1. Enclosed area: a region of the grid that is surrounded by a specific color or pattern.
2. Suqares that are seperated by grid.
3. Grid with colored pixels.

Grid size:
1. remain the same
2. The length and width are both doubled.

Crucial concepts about the transformation:
1. Fill the enclosed area with a specific color.
2. Count the number of pixels.
3. Find one specific pattern and use it to fill the rest of the grid.
4. Replicate the input grid in different quadrants of the output grid.
5. Rotate the grid in different directions.
"""
        if number == 1:
                return example_1
        if number == 2:
                return example_2
        if number == 3:
                return example_3
