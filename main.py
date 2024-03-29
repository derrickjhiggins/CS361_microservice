from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Sample data for demonstration purposes (replace this with your actual data)
user_data = {
    # 'username1': {'password': 'pass123', 'encrypted_message': 'encrypted_msg_1'},
    # 'username2': {'password': 'pass456', 'encrypted_message': 'encrypted_msg_2'}
}


class AuthenticationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        if username not in user_data or user_data[username]['password'] != password:
            return {'error': 'Invalid credentials'}, 401

        encrypted_message = user_data[username]['encrypted_message']

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

        if username in user_data:
            return {'error': 'Username already exists'}, 400

        user_data[username] = {'password': password, 'encrypted_message': encrypted_message}

        return {'message': 'User registered successfully'}, 201


class SaveMessageResource(Resource):
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
            return {'error': 'Invalid credentials'}, 401

        user_data[username] = {'password': password, 'encrypted_message': encrypted_message}

        return {'message': 'Message saved successfully'}, 200


class GetMessageResource(Resource):
    def get(self, username):
        if username in user_data:
            encrypted_message = user_data[username]['encrypted_message']
            return {'username': username, 'encrypted_message': encrypted_message}, 200
        else:
            return {'error': 'Username not found'}, 404


api.add_resource(AuthenticationResource, '/authenticate')
api.add_resource(RegistrationResource, '/register')
api.add_resource(SaveMessageResource, '/save_message')
api.add_resource(GetMessageResource, '/get_message/<string:username>')

if __name__ == '__main__':
    app.run(port=5000)
