from flask import Flask
from flask_restful import Resource, Api
import random

app = Flask(__name__)
api = Api(app)

class Hidden_Data(Resource):
    def get(self):

        digit = str(random.randint(0, 9))

        number = digit + digit + digit + '-' + digit + digit + digit + '-' + digit + digit + digit + digit + digit

        digit2 = str(random.randint(0, 9))

        social = "1" + "2" + "3" + '-' + digit2 + digit2 + '-' + digit2 + "1" + "2" + digit2

        email = "test" + digit + digit2 + "@gmail.com"

        return {
            'sensitive_data': ['Phone: ' + number, 'SSN: ' + social, 'Email: ' + email]
    }

api.add_resource(Hidden_Data, '/get-data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
