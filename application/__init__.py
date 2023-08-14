from flask import Flask
from app import home, create_phone, get_all_phones, get_phone, update_phone, delete_phone
app = Flask(__name__)

app.config.from_pyfile("config.py")

app.add_url_rule("/", view_func=home)
app.add_url_rule("/phones", view_func=create_phone)
app.add_url_rule("/phones", view_func=get_all_phones)
app.add_url_rule("/phones/<int:phone_id>", view_func=get_phone)
app.add_url_rule("/phones/<int:phone_id>", view_func=update_phone)
app.add_url_rule("/phones/<int:phone_id>", view_func=delete_phone)
