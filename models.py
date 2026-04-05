from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 1. This is your existing Asset table
class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    serial_number = Column(String, unique=True, index=True)
    status = Column(String, default="Available")

# 2. NEW: The Role table (Admin or Employee)
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "Admin"
    permissions = Column(String, default="")  # comma-separated permissions like "delete:asset,view:inventory"
    
    # This links the Role to all Users who have it
    users = relationship("User", back_populates="role")

# 3. NEW: The User table with RBAC
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # This stores the ID of the role (e.g., 1 for Admin)
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    # This allows you to do: user.role.name
    role = relationship("Role", back_populates="users")