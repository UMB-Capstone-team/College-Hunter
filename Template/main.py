# main file (to run)
# (create_app is the flask initialized in init.py)
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
