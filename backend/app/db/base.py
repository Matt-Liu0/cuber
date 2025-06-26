"""
Global SQLAlchemy Base for the CUBER project.
All ORM models should inherit from `Base`.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()