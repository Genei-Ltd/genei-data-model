from . import Resource, Section
from copy import deepcopy

def naive_ordering(r: Resource) -> Resource:
    """
    For each Section of the Resource, reorder the blocks
    using a naive leftmost, topmost algorithm.
    Use the same algorithm to reorder the sections.
    """
    r = deepcopy(r)  # copy r - these algos are NOT in place

    # sort the blocks inside the section
    for s in r.sections:
        blocks = s.blocks
        key = lambda block: (block.coords[0], round(block.coords[1], -2), block.coords[2])
        sorted_blocks = sorted(blocks, key=key)
        s.blocks = sorted_blocks

    # sort the sections themselves
    sections = r.sections
    def key(s):
        if s.title is not None:
            pn, x1, y1, x2, y2 = s.title.coords
            return (pn, round(x1, -2), y1)
        elif len(s.blocks) > 0:
            pn, x1, y1, x2, y2 = s.blocks[0].coords
            return (pn, round(x1, -2), y1)
        else:
            return (-1,-1,-1)
    sorted_sections = sorted(sections, key=key)
    r.sections = sorted_sections

    return r

def naive_sectioning(r:Resource) -> Resource:
    """
    Takes all the blocks in the resource and re-does the sectioning
    Using a naive algorithm that creates a new section each time it 
    encounters a title.
    """
    r = deepcopy(r) # copy r - these algos are NOT in place

    # First, totally flatten the data structure
    all_blocks = []
    for section in r.sections:
        for block in section.blocks:
            all_blocks.append(block)
        if section.title is not None:
            all_blocks.append(section.title)

    # Then sort them
    key = lambda block: (block.coords[0], round(block.coords[1], -2), block.coords[2])
    all_blocks = sorted(all_blocks, key=key)

    curr_section = None
    sections = []

    for block in all_blocks:
        
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