original_transformation_library = """
1. Color identification and changing based on object characteristics (shape, area size, adjacency).
2. Size modification of objects including expansion and contraction within the grid.
3. Repositioning of objects based on specific alignment instructions (vertical, horizontal, or diagonal).
4. Application of standard grid transformations such as reflection, rotation, or color inversion.
5. Creating borders around objects to either redefine or accentuate them.
6. Pattern continuation or completion based on initial patterns or directions provided.
7. Conversion of 2D patterns into different dimensions (expanding a pixel into a larger grid).
8. Color replacement specific to the object's location and its relation to other objects.
9. Maintaining object attributes such as color and size post-transformation within the new grid.
10. Comprehensive grid resizing maintaining the visual layout but altering dimensions.
11. Uniformity application where one rule is applied to all objects regardless of original condition.
12. Gravity simulation effecting vertical repositioning of objects.

1. Coloring according to adjacent or nearby object colors.
2. Overlaying grid dimensions or expanding them proportionally.
3. Filling in specified color patterns based on the position or other characteristics.
4. Keeping or changing the original spatial configurations within transformations.
5. Applying patterns or transformations inclusive or exclusive to specific predefined criteria (e.g., non-diagonals, within a row).
6. Transformative focus from one section or component of the grid to affect only designated sections.
7. Replacement of one set of object characteristics (e.g., color, shape) with another while maintaining original positioning.
8. Movement of objects based on spatial relations like adjacency or surrounding emptiness.
9. Inverting positioning or coloring patterns from input to output processes.
10. Isolating and magnifying specific sections of the grid for detailed transformations.

1. Grid expansion: Increasing the grid's dimensions tailored to transformation requirements.
2. Grid rotation: Rotating the entire grid or specific sections by specific degrees.
3. Grid reflection: Creating a mirror image of the grid or sections of it along vertical or horizontal axes.
4. Grid placement: Specifying placement of initial or transformed grid sections into designated areas of an output grid.
5. Grid filling: Filling the grid or sections by duplicating, rotating, or mirroring parts of the original grid.
6. Grid duplication: Copying the grid multiple times into a new or expanded grid format.
7. Color transformation: Modifying the color of specific sections or objects based on defined rules.
8. Grid partitioning: Dividing the grid into smaller sections for individual transformations.
9. Symmetric filling: Mirroring sections of the grid to preserve or create symmetry.
10. Object movement: Relocating specific objects within the grid to adjacent or specific positions.

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

1. Counting and locating specific elements or colors.
2. Mirroring or reflecting designs within sections or across grids.
3. Filling or coloring specific sections based on particular rules or patterns observed.
4. Resizing grids to match counts or dimensions of certain elements.
5. Transferring and replicating specific grid contents to other sections.
6. Sequential alteration of elements across a pattern or grid.
7. Maintaining the background or certain elements while transforming others.
8. Utilizing attributes like the position or count of elements to execute transformations.
9. Implementing transformations based on matching or coordinated colors.
10. Delimiting transformations strictly within defined boundaries of figures or layouts.
11. Overlapping or assigning priority to specific elements during transformations.
12. Ensuring transformations cater to both aesthetic and logical harmony.

1. Identify and merge adjacent cells of the same color to form larger blocks.
2. Overlap segments to create new patterns while maintaining visibility of underlying layers.
3. Transform object colors based on properties like adjacency or matching characteristics.
4. Adjust grid dimensions to match the properties or size of specific objects or patterns.
5. Use horizontal or vertical extensions to impact grid transformation.
6. Copy and superimpose grid segments to merge and modify features.
7. Shift object positions within grids while preserving or changing object properties.
8. Utilize pattern recurrence to adjust grid alignment or size expansion.
9. Calculate and compare object properties for transformation feedback.
10. Formulate connections or interactions between like-colored or positioned objects.

1. Pattern Analysis: Identifying recurring or distinctive patterns in the input.
2. Grid Resizing: Modifying grid size based on the complexity or simplicity of elements.
3. Superimposing: Layering one section of the grid onto another for comparison or transformation.
4. Color Coding: Applying specific colors to grid blocks based on defined rules (e.g., empty, pattern presence).
5. Element Isolation: Focusing on specific elements like intersections or individual squares for transformation.
6. Recursive Reproduction: Repeating a pattern within its components.
7. Alternate Coloring: Implementing color changes following a specific sequence across the grid columns.
8. Dominant Features: Determining the most prevalent color or pattern and adapting the grid accordingly.
9. Layer Swapping: Exchanging colors or patterns between different layers or sections of the grid.
10. Mirror Imaging: Reflecting existing patterns into newly structured areas or components.
11. Relocation: Moving specific elements from one position to another while maintaining relative positions.
12. Component Identification: Recognizing and focusing transformation on selected grid components (e.g., yellow blocks, vertical columns).
13. Incremental Alteration: Sequential modifications following a set progression or pattern.
14. Color Replacement: Substituting one color with another while keeping specific areas unchanged.
15. Direct Copy: Replicating the input directly into the output with selective modifications.
16. Horizontal Synchronization: Matching elements across horizontal rows for uniform transformation.
"""

def get_transformation_library():
    global original_transformation_library
    transform_library = original_transformation_library.replace('\n\n', '\n')
    transform_library = transform_library.split('\n')
    transform_library = [x for x in transform_library if x]
    transform_library = [x[x.find('.')+1:].strip() for x in transform_library]
    # print(transform_library)
    return transform_library