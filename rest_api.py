from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage (list of dicts)
users = []

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "User Management API is running"}), 200


# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    # Basic validation
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and Email are required"}), 400

    # Create new user with auto-generated ID
    user_id = len(users) + 1
    new_user = {
        "id": user_id,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201


# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


# Get user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


# Update user by ID
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify(user), 200


# Delete user by ID
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    updated_users = [u for u in users if u["id"] != user_id]

    if len(updated_users) == len(users):
        return jsonify({"error": "User not found"}), 404

    users = updated_users
    return jsonify({"message": f"User {user_id} deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
