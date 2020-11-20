from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<user>:<passwd>@<ip_servidor>:<port>/<database_name>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lrodriguez:derek.15@localhost:3306/contactlist'

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) #  init migrate upgrade downgrade

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/apis/fake/contact/agenda', methods=['GET'])
def all_agendas():
    pass

@app.route('/apis/fake/contact/agenda/<agenda_slug>', methods=['GET', 'DELETE'])
def all_contacts_by_agenda(agenda_slug):
    pass

@app.route('/apis/fake/contact/<int:contact_id>', methods=['GET', 'PUT', 'DELETE'])
def contact(contact_id):
    pass

@app.route('/apis/fake/contact', methods=['POST'])
def create_contact():
    pass


if __name__ == '__main__':
    manager.run()