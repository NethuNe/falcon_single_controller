import falcon
from controller.photo_library import Library, Image





#set-up logging

#app.add_route()s to add functionality : get & post & delete(if)
api = application = falcon.API()
images = Library('./savedImages') # need a file-path
imageRetrieval = Image()
api.add_route('/images', images)
api.add_route('/images/{name}', imageRetrieval)