from flask import jsonify

def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}

UNKNOWN_ERROR = template([], code=500)
ALBUM_NOT_FOUND = template(['Album not found'], code=404)
BAND_NOT_FOUND = template(['Band not found'], code=404)
SONG_EXISTS = template(['Song already exists'], code=404)
SONG_NOT_FOUND = template(['Song not found'], code=404)

class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def album_not_found(cls):
        return cls(**ALBUM_NOT_FOUND)

    @classmethod
    def band_not_found(cls):
        return cls(**BAND_NOT_FOUND)

    @classmethod
    def song_already_exists(cls):
        return cls(**SONG_EXISTS)

    @classmethod
    def song_not_found(cls):
        return cls(**SONG_NOT_FOUND)
