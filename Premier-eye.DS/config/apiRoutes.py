
galleryRoutes = {
    'upload': (lambda filename: f'/gallery/image/{filename}'),
    'postInfo': (lambda filename: f'/imageInfo/{filename}/info'),
    'log': '/events/log',
    'logs': '/events/logs'
}