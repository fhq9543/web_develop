#!/usr/bin/env python
from app import create_app
from app.devices import devices
from mylog import logger

app = create_app('config')
app.register_blueprint(devices, url_prefix='/devices')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
