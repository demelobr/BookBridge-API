import logging
from flask import request
from sql_alchemy import db
from app import create_app

app = create_app()

# Configuração básica de logs
logging.basicConfig(filename='app.log', level=logging.INFO)

@app.before_request
def log_request_info():
    app.logger.info(f'Request URL: {request.url}')
    app.logger.info(f'Request Method: {request.method}')
    app.logger.info(f'Client IP: {request.remote_addr}')
    app.logger.info(f'Request Headers: {request.headers}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)