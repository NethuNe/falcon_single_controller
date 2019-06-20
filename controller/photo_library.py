import falcon
import json
import mimetypes #read
import uuid #read
import os
import io

class Library(object):

    _CHUNK_SIZE_IN_BYTES = 4096 # maximum byte size of an inputted image

    def __init__(self, save_path):
        self.save_path = save_path
        self.image_document = {
            'images': []
        }
        # to initialize contents on start-up
        self.path = "'falcon_single_controller/savedImages'"
        for image in os.walk(self.path):
            self.image_document['images'].append("'href': " + image)
    
    def on_get(self, req, resp):
        #currently returns entirety of image document
        resp.body = json.dumps(self.image_document, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        #sanitize input for only image file types? currently doesn't
        extension = mimetypes.guess_extension(req.content_type)
        image_name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=extension)
        image_path = os.path.join(self.save_path, image_name)

        with io.open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(self._CHUNK_SIZE_IN_BYTES)
                if not chunk:
                    break
                image_file.write(chunk)
            self.image_document['images'].append("'href': " + image_name)
            resp.status = falcon.HTTP_200
            resp.location = '/images/' + image_name

    #def on_delete(self, req, resp):
        #image_to_delete = req. how to index to one particular image / parse a req file