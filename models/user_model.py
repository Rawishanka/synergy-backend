from sqlalchemy import Column, Integer, String, Boolean, Date, func
from sqlalchemy.orm import relationship
from database import Base 


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, nullable=True, index=True)
    first_name = Column(String, nullable=True, index=True)
    last_name = Column(String, nullable=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)
    create_date = Column(Date, nullable=False, default=func.current_date())
    update_date = Column(Date, nullable=True, default=func.current_date(), onupdate=func.current_date())
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relationships (Example: A user can create advertisements)
    advertisements = relationship("Advertisement", back_populates="users")