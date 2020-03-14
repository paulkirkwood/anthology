#coding: utf-8

import datetime as dt

from slugify import slugify
from feature.database import (Model, SurrogatePK, db, Column, reference_col, relationship)

class Band(Model, SurrogatePK):
    __tablename__ = 'band'

    id   = db.Column(db.Integer, primary_key=True)
    slug = Column(db.Text, unique=True)
    name = Column(db.String(100), nullable=False)

    albums = relationship('Album', backref=db.backref('band'), lazy='dynamic')

    def __init__(self, name, slug=None, **kwargs):
        db.Model.__init__(self, name=name, slug=slug or slugify(name), **kwargs)

class Album(Model, SurrogatePK):
    __tablename__ = 'album'

    id           = db.Column(db.Integer, primary_key=True)
    slug         = Column(db.Text, unique=True, nullable=False)
    title        = Column(db.Text, nullable=False)
    release_date = Column(db.DateTime, nullable=False)
    band_id      = reference_col('band', nullable=False)

    def __init__(self, band, release_date, title, slug=None, **kwargs):
        db.Model.__init__(self, band=band, release_date=release_date, slug=slug or slugify(title),
            title=title, **kwargs)
