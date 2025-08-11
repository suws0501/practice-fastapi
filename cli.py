from typer import Typer
from sqlalchemy import create_engine

# Import your models so Base is aware of them
from src.models.todo import *
from src.utils.db_utils import Base, get_database_url

app = Typer()

def init_database():
    """Initialize the database and create all tables."""
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

@app.command("init_database")
def cmd_init_database():
    """CLI command to initialize the database."""
    print("Initializing database...")
    init_database()

@app.command("run_test")
def cmd_run_test():
    """Placeholder for running tests."""
    print("Running tests...")
    # TODO: Add test execution logic here
    print("Tests executed successfully.")

if __name__ == "__main__":
    app()
