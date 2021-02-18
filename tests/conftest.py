import pytest
import sys


from geneidatamodel import Resource

tests_dir = '/'.join(__file__.split('/')[:-1])

@pytest.fixture
def blank_resource():
    with open(f'{tests_dir}/resources/example_resource_blank.json', 'r') as f:
        raw_str = f.read()
    r = Resource.loads(raw_str)
    return r