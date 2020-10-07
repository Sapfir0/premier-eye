app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

# Optional, for adding batch query support (used in Apollo-Client)
app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    batch=True
))