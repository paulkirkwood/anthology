# coding: utf-8

import datetime as dt

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields

from feature.exceptions import InvalidUsage
from .models import Album, Band
from .serializers import (album_schema, album_schemas, band_schema, band_schemas)

blueprint = Blueprint('bands', __name__)

@blueprint.route('/api/bands', methods=('GET',))
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(band_schemas)
def get_bands(limit=20, offset=0):
    res = Band.query
    return res.offset(offset).limit(limit).all()

@blueprint.route('/api/bands', methods=('POST',))
@use_kwargs(band_schema)
@marshal_with(band_schema)
def make_band(name):
    band = Band(name=name)
    band.save()
    return band

@blueprint.route('/api/bands/<slug>', methods=('GET',))
@marshal_with(band_schema)
def get_band(slug):
    band = Band.query.filter_by(slug=slug).first()
    if not band:
        raise InvalidUsage.band_not_found()
    return band

@blueprint.route('/api/bands/<slug>/albums', methods=('GET',))
@marshal_with(album_schemas)
def get_albums(slug):
    band = Band.query.filter_by(slug=slug).first()
    if not band:
        raise InvalidUsage.band_not_found()
    return band.albums

@blueprint.route('/api/bands/<slug>/albums', methods=('POST',))
@use_kwargs(album_schema)
@marshal_with(album_schema)
def make_album_on_band(slug, release_date, title, **kwargs):
    band = Band.query.filter_by(slug=slug).first()
    if not band:
        raise InvalidUsage.band_not_found()
    album = Album(band, release_date, title, **kwargs)
    album.save()
    return album

@blueprint.route('/api/bands/<band_slug>/albums/<album_slug>', methods=('GET',))
@marshal_with(album_schema)
def get_album(band_slug, album_slug):
    band = Band.query.filter_by(slug=band_slug).first()
    if not band:
        raise InvalidUsage.band_not_found()

    album = band.albums.filter_by(slug=album_slug).first()
    if not album:
        raise InvalidUsage.album_not_found()
    return album
