from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Contact

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<user>:<passwd>@<ip_servidor>:<port>/<database_name>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://contactuser:sabrinalabruja@localhost:3306/contactlist'

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) #  init migrate upgrade downgrade

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/apis/fake/contact/agenda', methods=['GET'])
def all_agendas():
    contacts = Contact.query.with_entities(Contact.agenda_slug).distinct()
    agendas = []
    for agenda in contacts:
        agendas.append(agenda[0])
    return jsonify(agendas), 200

@app.route('/apis/fake/contact/agenda/<agenda_slug>', methods=['GET', 'DELETE'])
def all_contacts_by_agenda(agenda_slug):
    agendas = Contact.query.filter_by(agenda_slug=agenda_slug).all()
    if request.method == 'GET':
        if agendas:
            agendas = list(map(lambda agenda: agenda.serialize(), agendas))
            return jsonify(agendas), 200
        else:
            return jsonify({"msg": "No agenda with that slug found"}), 404

    if request.method == "DELETE":
        if agendas:
            agendas.delete()
            return jsonify({"msg": f"Agenda {agenda_slug} has been deleted"}), 200
        else:
            return jsonify({"msg": "No agenda with that slug found"}), 404
    
@app.route('/apis/fake/contact/<int:contact_id>', methods=['GET', 'PUT', 'DELETE'])
def contact(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first()
    if request.method == 'GET':
        if contact:
            return jsonify(contact.serialize()), 200
        else:
            return jsonify({"msg": "No contact with that id found"}), 404
    if request.method == 'DELETE':
        if contact:
            contact.delete()
            return jsonify({"msg": f"Contact with {contact_id} has been deleted"}), 200
        else:
            return jsonify({"msg": "No contact with that id found"}), 404

    if request.method == "PUT":
        if contact:
            full_name = request.json.get('full_name')
            email = request.json.get('email')
            agenda_slug = request.json.get('agenda_slug')
            address = request.json.get('address')
            phone = request.json.get('phone')

            if not full_name:
                return jsonify({"msg": "Full name is required"}), 400
            if not email:
                return jsonify({"msg": "Email required"}), 400
            if not agenda_slug:
                return jsonify({"msg": "Agenda slug is required"}), 400
            if not address:
                return jsonify({"msg": "Address is required"}), 400
            if not phone:
                return jsonify({"msg": "Phone is required"}), 400
            
            contact.full_name = full_name
            contact.email = email
            contact.agenda_slug = agenda_slug
            contact.address = address
            contact.phone = phone
            contact.update()

            return jsonify({"msg": f"Contact with id {contact_id} has been updated"}), 200

        else:
            return jsonify({"msg": "Id was not found in our database"}),  404
        
@app.route('/apis/fake/contact', methods=['POST'])
def create_contact():
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    agenda_slug = request.json.get('agenda_slug')
    address = request.json.get('address')
    phone = request.json.get('phone')

    contact = Contact.query.filter_by(agenda_slug=agenda_slug).first()
    if contact:
        return jsonify({"msg": "agenda already exists"})
    else:
        if not full_name:
            return jsonify({"msg": "Full name is required"}), 400
        if not email:
            return jsonify({"msg": "Email required"}), 400
        if not agenda_slug:
            return jsonify({"msg": "Agenda slug is required"}), 400
        if not address:
            return jsonify({"msg": "Address is required"}), 400
        if not phone:
            return jsonify({"msg": "Phone is required"}), 400

        contact = Contact()
        contact.full_name = full_name
        contact.email = email
        contact.agenda_slug = agenda_slug
        contact.address = address
        contact.phone = phone
        contact.save()

        return jsonify(contact.serialize()), 201

if __name__ == '__main__':
    manager.run()