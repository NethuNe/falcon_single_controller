import falcon
from controller.photo_library import Library





#set-up logging

#app.add_route()s to add functionality : get & post & delete(if)
api = application = falcon.API()
images = Library('./savedImages') # need a file-path
api.add_route('/images', images)