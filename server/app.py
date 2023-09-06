from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method =='GET':
        messages= []
        for message in Message.query.all():
            messages_dict=message.to_dict()
            messages.append(messages_dict)

        response=make_response (
            messages,
            200
        )
        return response

    elif request.method == 'POST':
        request_dict=request.get_json()
        new_message=Message(
            body =request_dict.get("body"),
            username=request_dict.get("username")
        )
        db.session.add(new_message)
        db.session.commit ()
        messages_dict = new_message.to_dict ()
        response = make_response(
            messages_dict,
            201
        )
        return response

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    messages = Message.query.filter(Message.id==id).first()

    if request.method == 'PATCH': 
        request_dict =request.get_json()
        for attr in request_dict:
            setattr(messages, attr, request_dict.get(attr))
        db.session.add(messages)
        db.session.commit ()

        messages_dict=messages.to_dict()
        response = make_response(
            messages_dict,
        200
        )
        return response

    elif request.method == 'DELETE':
        db.session.delete(messages)
        db.session.commit()
        response_body={
            "delete":True,
            "message": "message is removed."
        }
        response= make_response (
            response_body,
            200

        )
        return response

if __name__ == '__main__':
    app.run(port=5555)
