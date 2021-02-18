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

    curr_section = None
    sections = []

    for section in r.sections:
        for block in section.blocks:
        
            # Figs and tables get their own section
            if not block.label in ['title', 'text', 'list']:
                fig_section = Section(blocks=[block])
                sections.append(fig_section)
                
            elif block.label == 'title':
                if curr_section is not None:
                    sections.append(curr_section)
                curr_section = Section()
                curr_section.title = block
                
            elif block.label in ['text', 'list']:
                if curr_section is None:
                    curr_section = Section()
                curr_section.blocks.append(block)
            
            else: 
                raise Exception(f"Did not find match for Block type: {block['type']}")

    if curr_section is not None:
        sections.append(curr_section)
    r.sections = sections
    
    return r