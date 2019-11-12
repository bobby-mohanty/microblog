from app import create_app, db, cli
from app.models import Users, Post

from flask_cors import CORS

app = create_app()
CORS(app)
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Post': Post}
