from flask import Blueprint, request, jsonify
from models import Event, db

event_blueprint = Blueprint('event', __name__)

@event_blueprint.route('/event', methods=['POST'])
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
    return jsonify({"message": "Event created", "event_id": new_event.event_id}), 201

@event_blueprint.route('/events', methods=['GET'])
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

@event_blueprint.route('/event/<string:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    return jsonify({
        "event_id": event.event_id,
        "title": event.title,
        "description": event.description,
        "date_time": event.date_time,
        "location": event.location,
        "organizer_id": event.organizer_id
    })

@event_blueprint.route('/event/<string:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    
    data = request.json
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.date_time = data.get('date_time', event.date_time)
    event.location = data.get('location', event.location)
    db.session.commit()
    return jsonify({"message": "Event updated"})

@event_blueprint.route('/event/<string:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})
