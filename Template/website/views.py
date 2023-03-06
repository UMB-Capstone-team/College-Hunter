# stores main views, or URL endpoints for front end
from flask import Blueprint

# file is a blueprint of app (bunch of urls defined in it)
views = Blueprint('views', __name__)

# im thinking its giving errors right now because of this file?