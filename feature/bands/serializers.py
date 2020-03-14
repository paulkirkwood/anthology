# coding: utf-8
        
from marshmallow import Schema, fields, pre_load, post_dump

class BandSchema(Schema):
    name = fields.Str()
    slug = fields.Str()
    band = fields.Nested('self', exclude=('band',), default=True, load_only=True)

    @pre_load
    def make_band(self, data, **kwargs):
        return data['band']

    @post_dump
    def dump_band(self, data, **kwargs):
        return {'band': data}

    class Meta:
        strict = True

class BandSchemas(BandSchema):

    @post_dump
    def dump_band(self, data, **kwargs):
        return data

    @post_dump(pass_many=True)
    def dump_bands(self, data, many, **kwargs):
        return {'bands': data}

class AlbumSchema(Schema):
    band         = fields.Nested(BandSchema)
    release_date = fields.DateTime()
    slug         = fields.Str()
    title        = fields.Str()

    album = fields.Nested('self', exclude=('album',), default=True, load_only=True)

    @pre_load
    def make_album(self, data, **kwargs):
        return data['album']

    @post_dump
    def dump_album(self, data, **kwargs):
        data['band'] = data['band']['band']
        return {'album': data}

    class Meta:
        strict = True

class AlbumSchemas(AlbumSchema):

    @post_dump
    def dump_album(self, data, **kwargs):
        data['band'] = data['band']['band']
        return data

    @post_dump(pass_many=True)
    def make_album(self, data, many, **kwargs):
        return {'albums': data}

band_schema   = BandSchema()
band_schemas  = BandSchemas(many=True)
album_schema  = AlbumSchema()
album_schemas = AlbumSchemas(many=True)
