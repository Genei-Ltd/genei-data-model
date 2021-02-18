from . import Resource, Section
from copy import deepcopy

def naive_ordering(r: Resource) -> Resource:
    """
    For each Section of the Resource, reorder the blocks
    using a naive leftmost, topmost algorithm.
    """
    r = deepcopy(r)  # copy r - these algos are NOT in place

    for s in r.sections:
        blocks = s.blocks
        key = lambda block: (block.coords[0], round(block.coords[1], -2), block.coords[2])
        sorted_blocks = sorted(blocks, key=key)
        s.blocks = sorted_blocks

    return r

def naive_sectioning(r:Resource) -> Resource:
    """
    Takes all the blocks in the resource and re-does the sectioning
    Using a naive algorithm that creates a new section each time it 
    encounters a title.
    """
    r = deepcopy(r) # copy r - these algos are NOT in place

    curr_section = Section()

    sections = [curr_section]
    other_blocks = []

    for section in r.sections:
        for block in section.blocks:
        
            # Figs and tables don't belong to the text sections
            if not block.label in ['title', 'text', 'list']:
                print('Added to other_blocks')
                other_blocks.append(block)
                continue
                
            if block.label == 'title':
                has_blocks = len(curr_section.blocks) > 0
                has_title = curr_section.title != None
                if has_blocks or has_title:
                    # Create a new section
                    print('Created new section')
                    curr_section = Section()
                    sections.append(curr_section)
                    
                curr_section.title = block
                curr_section.blocks = []
                continue
                
            if block.label in ['text', 'list']:
                curr_section.blocks.append(block)
                continue
                
            raise Exception(f"Did not find match for Block type: {block['type']}")

    r.sections = sections
    r.other_blocks = other_blocks
    
    return r