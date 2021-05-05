
galleryRoutes = {
    'upload': (lambda filename: f'/gallery/image/{filename}'),
    'postInfo': (lambda filename: f'/image/{filename}/info'),
    'log': '/events/log',
    'logs': '/events/logs'
}