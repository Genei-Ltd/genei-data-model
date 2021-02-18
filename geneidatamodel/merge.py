"""
Takes a list of Resource, Section or Blocks and combines them.
"""
from typing import List
from copy import deepcopy
from . import Resource, Section, Block

def merge_resources(resources:List[Resource], allow_overwrite:bool =True) -> Resource:
    """
    Merges a list of Resources into 1 Resource.
    Sections are joined in input order.
    If allow_overwrite: For overlapping keys (not including sections, which are 
    joined) the earlier items in the input list take precendence. Otherwise
    a RuntimeError will be raised.
    Returns new objects, not pointers to inputs, atleast on the surface.
    """
    if len(resources) == 0:
        raise RuntimeError('Resources cannot be of length 0')
    
    r1 = resources.pop(0)
    return_resource = deepcopy(r1)

    for resource in resources:
        assert isinstance(resource, Resource)
        for section in resource.sections:
            return_resource.sections.append(section)
        for k,v in resource.__dict__.items():
            if not return_resource.__dict__.get(k, False):
                setattr(return_resource, k, v)

    return return_resource