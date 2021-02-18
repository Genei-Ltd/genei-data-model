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
    def __init__(self, coords: list, **kwargs) -> 'Block':
        """
        Object to represent an atomic segment of a resource, ie a line of text.

        Args:
            coords: list
                5-tuple of (page, x1, y1, x2, y2)
            _type: str
                Optional; Acts as a discriminator and validator. Always 'Block'.
            text: str
                Optional; Raw text string of the block.
            label: str
                Optional; Detectron label assigned to the block. One of
                [text, title, list, figure, table]

        Returns:
            The initialized Block object. 
        """

        self.coords = coords
        assert type(coords) == list
        assert len(coords) == 5 # page, x1, y1, x2, y2

        _type = kwargs.get('_type', 'Block')
        assert _type == 'Block'
        self._type = _type

        self.text = kwargs.get('text', None)
        if self.text is not None:
            assert type(self.text) == str

        self.label = kwargs.get('label', None)
        if self.label is not None:
            assert self.label in ['text', 'title', 'list', 'figure', 'table']

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
            'label': self.label,
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict())
    

class Section:
    def __init__(self, _type=None, blocks=None, title=None, summary=None):
        """
        Object that groups Block objects into semantically similar regions.

        Args:
            _type: str
                Optional; Acts as a discriminator and validator. Always 'Section'.
            blocks: list
                Optional; List of blocks the section contains. If None blocks
                will be intialised to the empty list.
            title: Block
                Optional; A block to flag as the heading of the section.
            summary: str
                Optional; Raw text string of the block.

        Returns:
            The initialized Section object. 
        """
        self._type = _type
        if self._type is None:
            self._type = 'Section'
        else:
            assert self._type == 'Section'

        # Validate blocks
        self.blocks = blocks
        if self.blocks is None:
            self.blocks = []
        assert type(self.blocks) == list
        for block in self.blocks:
            assert type(block) == Block

        # Validate title
        self.title = title
        if self.title is not None:
            assert type(self.title) == Block

        # Validate summary
        self.summary = summary
        if  self.summary is not None:
            assert type(self.summary) == str

    @staticmethod
    def from_dict(d: dict) -> 'Section':
        # Convert title to Block object
        title = d.get('title')
        if title is not None:
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
    def __init__(self, _type=None, filetype=None, source=None, sections=None, title=None, date_created=None, **kwargs):
        _type = kwargs.get('_type', 'Resource')
        assert _type == 'Resource'
        self._type = _type

        # Validate filetype
        self.filetype = filetype
        if self.filetype is not None:
            assert filetype in FILETYPES

        # Validate source
        self.source = source
        if self.source is not None:
            assert type(source) == dict
            assert (
                (('bucket' in source) and ('key' in source))
                or
                ('url' in source)
                or
                ('data' in source)
            ) # One of S3, Url or Payload source

        # Validate sections
        self.sections = sections
        if self.sections is None:
            self.sections = []
        else:
            assert type(sections) == list
            for section in sections:
                assert type(section) == Section

        # Validate title
        self.title = title
        if self.title is not None:
            assert type(title) == str

        # Validate date_created
        self.date_created = date_created
        if date_created is not None:
            assert type(date_created) == str

    @staticmethod
    def from_dict(d: dict) -> 'Resource':
        d['sections'] = [Section.from_dict(section) for section in d['sections']]
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
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict())