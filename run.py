import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    print('Setting up board')
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)