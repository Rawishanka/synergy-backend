from sqlalchemy import  Column, Integer, LargeBinary, String, Date, Boolean, ForeignKey, func, Text, ARRAY, JSON
from database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)
    create_date = Column(Date, nullable=False, default=func.current_date())
    update_date = Column(Date, nullable=True, default=func.current_date(), onupdate=func.current_date())
    is_active = Column(Boolean, default=True, nullable=False)
    
    sub_categories = relationship("SubCategory", back_populates="category")
    advertisements = relationship("Advertisement", back_populates="category")

class SubCategory(Base):
    __tablename__ = 'sub_categories'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)
    create_date = Column(Date, nullable=False, default=func.current_date())
    update_date = Column(Date, nullable=True, default=func.current_date(), onupdate=func.current_date())
    is_active = Column(Boolean, default=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    category = relationship("Category", back_populates="sub_categories")
    advertisements = relationship("Advertisement", back_populates="sub_category")

class Advertisement(Base):
    __tablename__ = 'advertisements'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=True) 
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    sub_category_id = Column(Integer, ForeignKey('sub_categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    location = Column(String, nullable=True)
    day = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    is_wanted = Column(Boolean, default=False, nullable=False)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)
    create_date = Column(Date, nullable=False, default=func.current_date())
    update_date = Column(Date, nullable=True, default=func.current_date(), onupdate=func.current_date())
    
    category = relationship("Category", back_populates="advertisements")
    sub_category = relationship("SubCategory", back_populates="advertisements")
    users = relationship("User", back_populates="advertisements" )
    images = relationship("Image", back_populates="advertisements")
    
    
class RawListing(Base):
    __tablename__ = 'raw_listings'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    meta_data = Column(Text)
    price = Column(Text)
    attributes = Column(ARRAY(Text))
    description = Column(Text)
    url = Column(Text, unique=True, nullable=False)
    breadcrumbs = Column(ARRAY(Text))
    image_urls = Column(ARRAY(Text))
    additional_data = Column(JSON)
    combined_text = Column(Text)
    fetched = Column(Boolean, default=False) 

    def __repr__(self):
        return f"<RawListing(title={self.title}, url={self.url})>"
    

# Image Model
class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    image_data = Column(LargeBinary, nullable=False)

    advertisements = relationship("Advertisement", back_populates="images")