from flask import Blueprint, jsonify
from backend.store import people as people_store, companies as companies_store
from backend.validation import validate_company_name

companies_v1 = Blueprint('companies_v1', __name__)

@companies_v1.route('/<name>/employees', methods=['GET'])
def get_company_employees(name):
    validate_company_name(name)
    
    # check if the company exists
    company = companies_store.get_by_name(name)

    people = people_store.get_people_by_company_name(company['name'])
    return jsonify(people)


