import sqlite3
from flask import jsonify, request, Flask

app = Flask(__name__)

DATABASE = "app/phones.db"


# Create connection to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


# Create phones table if it doesn't exist
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS phones (
                        phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        contact_name TEXT,
                        phone_value TEXT)"""
    )
    conn.commit()


@app.route("/")
def home():
    return "Hello, World!"
# Create
@app.route("/phones", methods=["POST"])
def create_phone():
    data = request.get_json()
    contact_name = data.get("contact_name")
    phone_value = data.get("phone_value")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phones (contact_name, phone_value) VALUES (?, ?)", (contact_name, phone_value))
    conn.commit()

    return jsonify({"message": "Phone created successfully"})


# Read all
@app.route("/phones", methods=["GET"])
def get_all_phones():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phones")
    phones = cursor.fetchall()
    results = [{"phone_id": phone[0], "contact_name": phone[1], "phone_value": phone[2]} for phone in phones]

    return jsonify(results)


# Read
@app.route("/phones/<int:phone_id>", methods=["GET"])
def get_phone(phone_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phones WHERE phone_id = ?", (phone_id,))
    phone = cursor.fetchone()

    if phone is None:
        return jsonify({"message": "Phone not found"})

    result = {"phone_id": phone[0], "contact_name": phone[1], "phone_value": phone[2]}

    return jsonify(result)


# Update
@app.route("/phones/<int:phone_id>", methods=["PUT"])
def update_phone(phone_id):
    data = request.get_json()
    contact_name = data.get("contact_name")
    phone_value = data.get("phone_value")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE phones SET contact_name = ?, phone_value = ? WHERE phone_id = ?", (contact_name, phone_value, phone_id)
    )
    conn.commit()

    return jsonify({"message": f"Phone with id {phone_id} updated successfully"})


# Delete
@app.route("/phones/<int:phone_id>", methods=["DELETE"])
def delete_phone(phone_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM phones WHERE phone_id = ?", (phone_id,))
    conn.commit()

    return jsonify({"message": f"Phone with id {phone_id} deleted successfully"})


# Initialize database and create table
create_table()

if __name__ == "__main__":
    app.run(port=5050)
