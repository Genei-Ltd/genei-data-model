"""
Classes that define the Resource, Section and Block datatypes.

Whilst using these classses doesn't provide much function use,
the requirement to use them acts as a validator inside the codebase,
forcing i/o between functions to adhere to a globally defined standard.

For example, creating a resource from JSON validates that that JSON was in the correct standard.
There are of course other ways to validate JSON, but until json-schema better handles OpenAPIs $ref
specifcation, we chose to stick with defining our schema in python.
"""

# TODO: The type checking is hacky and budget - we should use JSON Schema.

import json

FILETYPES = ['PDF']

class Block:
    def __init__(self, coords=[], text=None, label=None):
        self._type = 'Block'

        # Validate coords
        assert type(coords) == list
        assert len(coords) == 5 # page, x1, y1, x2, y2
        self.coords = coords

        # Validate text
        if text is not None:
            assert type(text) == str
        self.text = text

        # Validate label
        if label is not None:
            assert type(label) == str
        self.label = label

    @staticmethod
    def from_dict(d: dict) -> 'Block':
        return Block(**d)

    @staticmethod
    def loads(s: str) -> 'Block':
        d = json.loads(s)
        return Block.from_dict(d)
    
    def to_dict(self):
        return {
            '_type': 'Block',
            'coords': self.coords,
            'text': self.text,
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict())
    

class Section:
    def __init__(self, blocks=[], title=None, summary=None):
        self._type = 'Section'

        # Validate blocks
        assert type(blocks) == list
        for block in blocks:
            assert type(block) == Block
        self.blocks = blocks

        # Validate title
        if title is not None:
            assert type(title) == Block
        self.title = title

        # Validate summary
        if  summary is not None:
            assert type(summary) == str
        self.summary = summary

    @staticmethod
    def from_dict(d: dict) -> 'Section':
        # Convert title to Block object
        title = d.get('title', '')
        if (title is not None) and (len(title) > 0):
            d['title'] = Block.from_dict(title)

        # Convert blocks to Block objects 
        blocks = d['blocks']
        obj_blocks = [Block.from_dict(block) for block in blocks]
        d['blocks'] = obj_blocks
        return Section(**d)

    @staticmethod
    def loads(s: str) -> 'Section':
        d = json.loads(s)
        return Section.from_dict(d)

    def to_dict(self):
        return {
            '_type': 'Section',
            'blocks': [block.to_dict() for block in self.blocks], 
            'title': self.title.to_dict() if self.title is not None else self.title,
            'summary': self.summary
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict())


class Resource:
    def __init__(self, filetype, source, sections=[], other_blocks=[], title=None, date_created=None):
        self._type = 'Resource'

        # Validate filetype
        assert filetype in FILETYPES
        self.filetype = filetype

        # Validate source
        assert type(source) == dict
        assert (
            (('bucket' in source) and ('key' in source))
            or
            ('url' in source)
            or
            ('data' in source)
        ) # One of S3, Url or Payload source
        self.source = source

        # Validate sections
        assert type(sections) == list
        for section in sections:
            assert type(section) == Section
        self.sections = sections

        # Validate other blocks
        assert type(other_blocks) == list
        for block in other_blocks:
            assert type(block) == Block
        self.other_blocks = other_blocks

        # Validate title
        if title is not None:
            assert type(title) == str
        self.title = title

        # Validate date_created
        if date_created is not None:
            assert type(date_created) == str
        self.date_created = date_created

    @staticmethod
    def from_dict(d: dict) -> 'Resource':
        d['sections'] = [Section.from_dict(section) for section in d['sections']]
        d['other_blocks'] = [Block.from_dict(block) for block in d.get('other_blocks', [])]
        return Resource(**d)

    @staticmethod
    def loads(s: str) -> 'Resource':
        d = json.loads(s)
        return Resource.from_dict(d)

    def to_dict(self) -> dict:
        return {
            '_type': 'Resource',
            'filetype': self.filetype,
            'source': self.source,
            'title': self.title,
            'date_created': self.date_created,
            'sections': [section.to_dict() for section in self.sections],
            'other_blocks': [block.to_dict() for block in self.other_blocks]
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict())