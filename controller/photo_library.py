import json
import mimetypes
import uuid
import os
import io
import falcon
import utils.local_logger as log

_CHUNK_SIZE_IN_BYTES = 4096  # maximum chunk size of an inputted image


class Library():
    def __init__(self, save_path):
        self.save_path = save_path
        self.image_document = []
        # to initialize contents on start-up
        for _, _, files in os.walk(self.save_path):
            if len(files) is not 0:
                for f in files:
                    self.image_document.append('href: {}'.format(f))

    def on_get(self, req, resp):
        resp.body = json.dumps(self.image_document, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        try:
            extension = mimetypes.guess_extension(req.content_type)
            if extension != '.png':
                raise falcon.HTTPBadRequest(
                    '400 Bad Request',
                    'Content-Type is not specified as proper image type of .png, instead of type {}'
                    .format(extension))

            image_name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=extension)
            image_path = os.path.join(self.save_path, image_name)

            with io.open(image_path, 'wb') as image_file:
                while True:
                    chunk = req.bounded_stream.read(_CHUNK_SIZE_IN_BYTES)
                    if not chunk:
                        break
                    image_file.write(chunk)

                self.image_document.append('href: {}'.format(image_name))
                resp.location = '/images/{}'.format(image_name)
                resp.status = falcon.HTTP_200
        except falcon.HTTPInternalServerError as e:
            log.log(
                __name__, {
                    "module": "photo_library_POST_content",
                    "code": falcon.HTTP_500,
                    "input": 'Exception of {0} on input {1}'.format(e, req)
                }, 40)


class Image():
    def __init__(self, save_path):
        self.save_path = save_path

    #get for one specific image (with image output)
    def on_get(self, req, resp, name):
        library = Library(self.save_path)
        if library.image_document.__contains__('href: {}'.format(name)):
            image_path = os.path.join(library.save_path, name)
            resp.content_type = 'image/png'
            resp.stream = io.open(image_path, 'rb')
            resp.status = falcon.HTTP_200
        else:
            log.log(
                __name__, {
                    "module": "photo_library_get_image",
                    "code": falcon.HTTP_400,
                    "input": req
                }, 30)
