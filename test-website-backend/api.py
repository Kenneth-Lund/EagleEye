from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Hidden_Data(Resource):
    def get(self):
        return {
            'sensitive_data': ['Username', 'Password', 'email']
    }

api.add_resource(Hidden_Data, '/get-data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
