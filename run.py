import os
from app import create_app
from werkzeug.serving import run_simple

app = create_app()

if __name__ == "__main__":
    print('Running app....')
    run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True, use_evalex=True)