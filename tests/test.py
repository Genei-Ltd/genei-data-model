from geneidatamodel import merge_resources
from geneidatamodel import naive_sectioning
from geneidatamodel import naive_ordering
from geneidatamodel import Resource

from pprint import PrettyPrinter
pp = PrettyPrinter()

def test_basic(blank_resource):
    assert blank_resource

def test_io(blank_resource):
    r = blank_resource
    s = r.dumps()
    r = Resource.loads(s)
    assert r.to_dict() == blank_resource.to_dict()

def test_merge(blank_resource):
    rs = [blank_resource]*3
    ls = len(rs[0].sections)
    r = merge_resources(rs)
    pp.pprint(r.to_dict())
    assert r.title == 'The Art of Decomposition'
    assert len(r.sections) == 3 * ls

def test_ordering(blank_resource):
    r = naive_ordering(blank_resource)
    d = r.to_dict()
    pp.pprint(d['sections'][0]['blocks'][:2])
    assert r.sections[0].blocks[0].text.startswith('_n the bitter realization')
    assert r.sections[0].blocks[1].text.startswith('The critic\'s annoyance')

def test_sectioning(blank_resource):
    print('Sections before: ', len(blank_resource.sections))
    r = naive_sectioning(blank_resource)
    print('Sections after: ', len(r.sections))
    print('And not inplace: ', len(blank_resource.sections))
    assert len(r.sections) == 11
    assert len(blank_resource.sections) == 1