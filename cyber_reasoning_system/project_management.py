## project_management.py
from typing import Dict, Optional
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


class ProjectManagement:
    def __init__(self):
        self.engine = self._connect_to_db()
        self.metadata = MetaData()
        self.projects = Table('projects', self.metadata, autoload_with=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    def _connect_to_db():
        return create_engine('sqlite:///projects.db')

    def create_project(self, project: str) -> Dict[str, str]:
        """
        Create a new project in the database.
        """
        session = self.Session()
        try:
            session.execute(self.projects.insert().values(name=project))
            session.commit()
            return {"message": f"Project '{project}' created successfully."}
        except IntegrityError:
            session.rollback()
            return {"error": f"Project '{project}' already exists."}
        finally:
            session.close()

    def update_project(self, project: str, new_name: str) -> Dict[str, str]:
        """
        Update the name of an existing project in the database.
        """
        session = self.Session()
        try:
            session.execute(self.projects.update().where(self.projects.c.name == project).values(name=new_name))
            session.commit()
            return {"message": f"Project '{project}' updated successfully to '{new_name}'."}
        except IntegrityError:
            session.rollback()
            return {"error": f"Project '{project}' does not exist or '{new_name}' is already used by another project."}
        finally:
            session.close()

    def delete_project(self, project: str) -> Dict[str, str]:
        """
        Delete an existing project from the database.
        """
        session = self.Session()
        result = session.execute(self.projects.delete().where(self.projects.c.name == project))
        session.commit()
        session.close()
        if result.rowcount > 0:
            return {"message": f"Project '{project}' deleted successfully."}
        else:
            return {"error": f"Project '{project}' does not exist."}

    def list_projects(self) -> Dict[str, Optional[str]]:
        """
        List all projects in the database.
        """
        session = self.Session()
        result = session.execute(self.projects.select())
        projects = [row['name'] for row in result]
        session.close()
        if projects:
            return {"projects": projects}
        else:
            return {"error": "No projects found."}
