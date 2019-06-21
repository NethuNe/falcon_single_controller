import falcon
from controller.photo_library import Image, Library
import utils.local_logger

_SAVE_PATH = './savedImages'
#app routes for photo_library
api = application = falcon.API()
api.add_route('/images', Library(_SAVE_PATH))
api.add_route('/images/{name}', Image(_SAVE_PATH))