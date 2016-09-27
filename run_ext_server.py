""" Run External Server """

# Do not use in production!
# See http://flask.pocoo.org/docs/0.11/deploying/#deployment

from src import app
from config import ExternalConfig

if __name__ == "__main__":
    app.config.from_object(ExternalConfig)
    # IMPORTANT: DEBUG MUST NEVER BE TRUE ON EXTERNAL MACHINES!
    app.run(host='0.0.0.0', port=80, debug=False)

