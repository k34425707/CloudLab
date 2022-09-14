from flask_restful import Resource

class test(Resource):
    def get(self):
        return {
            'message': 'Hello Wrold!',
            'method':'get'
        }, 200
    def post(self):
        return {
            'message': 'Hello Wrold!',
            'method':'post'
        }, 200
    
    def put(self):
        return {
            'message': 'Hello Wrold!',
            'method':'update'
        }, 200

    def delete(self):
        return {
            'message': 'Hello Wrold!',
            'method':'delete'
        }, 200