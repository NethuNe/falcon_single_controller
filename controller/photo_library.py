import falcon
import json
import mimetypes #read
import uuid #read
import os
import io

_CHUNK_SIZE_IN_BYTES = 4096 # maximum byte size of an inputted image

class Library(object):
    


    def __init__(self, save_path):
        self.save_path = save_path
        Library.image_document = {
            'images': []
        }
        # to initialize contents on start-up
        # takes parent of this path, appends path from parent to saving folder
        Library.path = os.path.join(os.path.realpath('..'), 'falcon_single_controller/savedImages')
        for root, directory, file in os.walk(self.path):
            if len(file) is not 0:
                #index into file name
               self.image_document['images'].append('href: ' + file[0])
    
    
    def on_get(self, req, resp):
        resp.body = json.dumps(self.image_document, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        #sanitize input for only image file types? currently doesn't
        #currently requires content type is specified as image png, otherwise assumes JSON?
        extension = mimetypes.guess_extension(req.content_type)
        if extension != '.png': #todo fix this to return properly formed http 400 response
            error_message = 'Content-Type is not specified as proper image type of png, instead of type ' + str(extension)
            raise falcon.HTTPBadRequest('400 Bad Request', error_message)
        else:
            image_name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=extension)
            image_path = os.path.join(self.save_path, image_name)

            with io.open(image_path, 'wb') as image_file:
                while True:
                    chunk = req.stream.read(_CHUNK_SIZE_IN_BYTES)
                    if not chunk:
                        break
                    image_file.write(chunk)
                self.image_document['images'].append('href: ' + image_name)
                resp.status = falcon.HTTP_200
                resp.location = '/images/' + image_name


class Image():
    #get to return one specific image instead of the list of them
    def on_get(self, req, resp, name):
        if Library.image_document['images'].__contains__('href: ' + name):
            print(name)
            image_path = os.path.join(Library.path, name)
            print(image_path)
            resp.content_type = mimetypes.guess_type(image_path)[0]
            resp.stream = io.open(image_path, 'rb')
