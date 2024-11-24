from flask import Flask, jsonify, request
from models import Event
from database import db, init_db

app = Flask(__name__)
init_db(app)

# Create an Event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    new_event = Event(
        title=data['title'],
        description=data.get('description', ''),
        date_time=data['date_time'],
        location=data['location'],
        organizer_id=data['organizer_id']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created", "event": new_event.event_id}), 201

# Get All Events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        "event_id": event.event_id,
        "title": event.title,
        "description": event.description,
        "date_time": event.date_time,
        "location": event.location,
        "organizer_id": event.organizer_id
    } for event in events])

# Update an Event
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.date_time = data.get('date_time', event.date_time)
    event.location = data.get('location', event.location)
    event.organizer_id = data.get('organizer_id', event.organizer_id)

    db.session.commit()
    return jsonify({"message": "Event updated"})

# Delete an Event
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})

if __name__ == '__main__':
    app.run(debug=True)
