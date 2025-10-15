from sqlalchemy.orm import Session
from . import models

def get_cv(db: Session, cv_id: int):
    """
    Retrieves a single CV record from the database by its ID.

    Args:
        db (Session): The database session.
        cv_id (int): The primary key ID of the CV to retrieve.

    Returns:
        models.CV | None: The CV object if found, otherwise None.
    """
    return db.query(models.CV).filter(models.CV.id == cv_id).first()

def create_cv(db: Session, filename: str, content: str) -> models.CV:
    """
    Creates a new CV record in the database.

    Args:
        db (Session): The database session.
        filename (str): The name of the uploaded CV file.
        content (str): The parsed text content of the CV.

    Returns:
        models.CV: The newly created and committed CV object.
    """
    db_cv = models.CV(filename=filename, content=content)
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    return db_cv
