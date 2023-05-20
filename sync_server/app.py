from waitress import serve
from flask import Flask

app = Flask(__name__)


@app.post('/predict')
def predict():
    return {'message': 'Predict!'}


serve(
    host='0.0.0.0',
    port=9090,
    app=app
)
