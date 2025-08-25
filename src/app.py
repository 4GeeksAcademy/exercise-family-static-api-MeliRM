

from flask import Flask, jsonify, request
from datastructures import FamilyStructure

app = Flask(__name__)


jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})


def json_error(message: str, status: int):
    return jsonify({"error": message}), status



@app.route("/members", methods=["GET"])
def get_members():
    try:
        return jsonify(jackson_family.get_all_members()), 200
    except Exception as e:
        return json_error(str(e), 500)


@app.route("/members/<int:member_id>", methods=["GET"])
def get_one_member(member_id: int):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return json_error("Member not found", 404)
        
        return jsonify({
            "id": member["id"],
            "first_name": member["first_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }), 200
    except Exception as e:
        return json_error(str(e), 500)



@app.route("/members", methods=["POST"])
def add_member():
    try:
        if not request.is_json:
            return json_error("Content-Type must be application/json", 400)
        data = request.get_json(silent=True)
        if data is None:
            return json_error("Invalid JSON body", 400)

        created = jackson_family.add_member(data)
        return jsonify(created), 200
    except ValueError as ve:
        return json_error(str(ve), 400)
    except Exception as e:
        return json_error(str(e), 500)



@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id: int):
    try:
        deleted = jackson_family.delete_member(member_id)
        if not deleted:
            return json_error("Member not found", 404)
        return jsonify({"done": True}), 200
    except Exception as e:
        return json_error(str(e), 500)



@app.errorhandler(404)
def handle_404(_):
    return json_error("Not found", 404)

@app.errorhandler(400)
def handle_400(_):
    return json_error("Bad request", 400)

@app.errorhandler(500)
def handle_500(_):
    return json_error("Server error", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3245, debug=True)

