## test_project_management.py

import unittest
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from cyber_reasoning_system.project_management import ProjectManagement

class TestProjectManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_management = ProjectManagement()
        cls.engine = cls.project_management._connect_to_db()
        cls.metadata = MetaData()
        cls.projects = Table('projects', cls.metadata, autoload_with=cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.session.execute(self.projects.delete())
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_create_project(self):
        response = self.project_management.create_project('Test Project')
        self.assertEqual(response, {"message": "Project 'Test Project' created successfully."})

        response = self.project_management.create_project('Test Project')
        self.assertEqual(response, {"error": "Project 'Test Project' already exists."})

    def test_update_project(self):
        self.project_management.create_project('Test Project')

        response = self.project_management.update_project('Test Project', 'Updated Project')
        self.assertEqual(response, {"message": "Project 'Test Project' updated successfully to 'Updated Project'."})

        response = self.project_management.update_project('Nonexistent Project', 'Updated Project')
        self.assertEqual(response, {"error": "Project 'Nonexistent Project' does not exist or 'Updated Project' is already used by another project."})

    def test_delete_project(self):
        self.project_management.create_project('Test Project')

        response = self.project_management.delete_project('Test Project')
        self.assertEqual(response, {"message": "Project 'Test Project' deleted successfully."})

        response = self.project_management.delete_project('Test Project')
        self.assertEqual(response, {"error": "Project 'Test Project' does not exist."})

    def test_list_projects(self):
        response = self.project_management.list_projects()
        self.assertEqual(response, {"error": "No projects found."})

        self.project_management.create_project('Test Project')

        response = self.project_management.list_projects()
        self.assertEqual(response, {"projects": ['Test Project']})


if __name__ == '__main__':
    unittest.main()
