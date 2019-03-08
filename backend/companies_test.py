import unittest
import uuid

from backend import create_app
from backend.tests import RestTest
from backend.db import get_db

class CompaniesIntegrationTest(RestTest):
    def insert_company(self, name):
        company = {
            'index': 0,
            'name': name
        }
        self.db.companies.insert_one(company)
        return company

    def insert_company_employee(self, company, employee_name):
        company_employee = {
            'name': employee_name
        }
        company_employee['company'] = {
            'index': company['index'],
            'name': company['name']
        }
        company_employee['guid'] = str(uuid.uuid4())

        self.db.people.insert_one(company_employee)
        return company_employee

    # GET /v1/companies/:name/employees

    def test_company_employees_wrong_company_name_returns_400(self):
        # Company names should always have uppercase charaters only
        response = self.client.get('/v1/companies/LUNA_Corp/employees')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Invalid ompany name format, should only contain uppercase characters')

    def test_company_employees_nonexistant_company_should_return_404(self):
        response = self.client.get('/v1/companies/LUNA/employees')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Company LUNA not found')

    def test_company_employees_empty_company_should_return_empty_list(self):
        self.insert_company('EOLIA')

        response = self.client.get('/v1/companies/EOLIA/employees')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(data, [])

    def test_company_employees_should_return_employees_list(self):
        company = self.insert_company('EOLIA')
        employee1 = self.insert_company_employee(company, 'Julia Woberts')
        employee2 = self.insert_company_employee(company, 'Jenny Laurence')
        response = self.client.get('/v1/companies/EOLIA/employees')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        ids = list(map(lambda p: p['guid'], data))
        self.assertListEqual(ids, [employee1['guid'], employee2['guid']])
