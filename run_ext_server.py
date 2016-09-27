""" Run External Server """

# Do not use in production!
# See http://flask.pocoo.org/docs/0.11/deploying/#deployment

from src import app
from config import ExtConfig

if __name__ == "__main__":
    app.config.from_object(ExtConfig)
    # IMPORTANT: DEBUG MUST NEVER BE TRUE ON EXTERNALLY VISIBLE SERVERS!
    app.run(host='0.0.0.0', port=80, threaded=True, debug=False)

