# from sqlalchemy import  Column, Integer, String, Date, Boolean, ForeignKey
# from database import Base
# from sqlalchemy.orm import relationship


# class Category(Base):
#     __tablename__ = 'categories'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False, index=True)
#     description = Column(String, nullable=True)
#     created_by = Column(String, nullable=False)
#     updated_by = Column(String, nullable=True)
#     create_date = Column(Date, nullable=False)
#     update_date = Column(Date, nullable=True)
#     is_active = Column(Boolean, default=True, nullable=False)
    
#     sub_categories = relationship("SubCategory", back_populates="category")
#     advertisements = relationship("Advertisement", back_populates="category")

# class SubCategory(Base):
#     __tablename__ = 'sub_categories'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False, index=True)
#     description = Column(String, nullable=True)
#     created_by = Column(String, nullable=False)
#     updated_by = Column(String, nullable=True)
#     create_date = Column(Date, nullable=False)
#     update_date = Column(Date, nullable=True)
#     is_active = Column(Boolean, default=True, nullable=False)
#     category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
#     category = relationship("Category", back_populates="sub_categories")
#     advertisements = relationship("Advertisement", back_populates="sub_category")

# class Advertisement(Base):
#     __tablename__ = 'advertisements'
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     url = Column(String, nullable=False)
#     image_url = Column(String, nullable=True)
#     description = Column(String, nullable=True)
#     category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
#     sub_category_id = Column(Integer, ForeignKey('sub_categories.id'), nullable=False)
#     location = Column(String, nullable=True)
#     day = Column(Date, nullable=False)
#     price = Column(Integer, nullable=False)
#     transaction_type = Column(String, nullable=False)
#     is_wanted = Column(Boolean, default=False, nullable=False)
#     created_by = Column(String, nullable=False)
#     updated_by = Column(String, nullable=True)
#     create_date = Column(Date, nullable=False)
#     update_date = Column(Date, nullable=True)
    
#     category = relationship("Category", back_populates="advertisements")
#     sub_category = relationship("SubCategory", back_populates="advertisements")