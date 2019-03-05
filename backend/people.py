from flask import Blueprint, jsonify

people_v1 = Blueprint('people_v1', __name__, template_folder='views')

@people_v1.route('/<guid>', methods=['GET'])
def get_person(guid):
    return jsonify({
        'name': 'person'
    })