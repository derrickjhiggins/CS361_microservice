from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Sample data for demonstration purposes (replace this with your actual data)
user_data = {
    # 'user1': {'password': 'pass123', 'encrypted_message': 'encrypted_msg_1'},
    # 'user2': {'password': 'pass456', 'encrypted_message': 'encrypted_msg_2'}
}

class AuthenticationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        if username not in user_data:
            return {'error': 'Invalid username'}, 401

        elif password not in user_data[username]:
            return {'error': 'Invalid password'}, 401

        encrypted_message = user_data[username][password]

        response_data = {'username': username, 'encrypted_message': encrypted_message}
        return response_data, 200

class RegistrationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        parser.add_argument('encrypted_message', type=str, required=True, help='Encrypted message is required')
        args = parser.parse_args()

        username = args['username']
        password = args['password']
        encrypted_message = args['encrypted_message']

        if username not in user_data:
            user_data[username] = {}

        user_data[username][password] = encrypted_message

        return {'message': 'User registered successfully'}, 201

api.add_resource(AuthenticationResource, '/authenticate')
api.add_resource(RegistrationResource, '/register')

if __name__ == '__main__':
    app.run(port=5000)
