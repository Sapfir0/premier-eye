from flask_restplus import Api, Resource, fields
from controllers.gallery.routes import api as galleryApi


api = Api(
    title='Premier-eye API',
    version='0.1',
    description='Small API for object detecton',
)

api.add_namespace(galleryApi)