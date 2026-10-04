from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


def find_event(event_id):
    """Return the Event with this id, or None if there isn't one."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def next_id():
    """Next free id: one more than the highest existing id."""
    return max((event.id for event in events), default=0) + 1


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Events API"})


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_event = Event(next_id(), data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
    