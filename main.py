from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, database, schemas

# 1. Initialize the Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="OptiAsset Management System API",
    description="Enterprise Asset Tracking with Role-Based Access Control.",
    version="1.2.0"
)

# --- DATABASE SEEDING ---
def seed_database():
    db = database.SessionLocal()
    try:
        # 1. Create Admin Role if it doesn't exist
        admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
        if not admin_role:
            admin_role = models.Role(name="Admin", permissions="create:asset,delete:asset,view:inventory")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print("Default 'Admin' role created.")

        # 2. Create Admin User (ID 1) if it doesn't exist
        admin_user = db.query(models.User).filter(models.User.id == 1).first()
        if not admin_user:
            # We hardcode ID 1 because main.py RequirePrivilege hardcodes the filter User.id == 1
            admin_user = models.User(id=1, email="admin@optivault.com", hashed_password="hashed_placeholder_password", role_id=admin_role.id)
            db.add(admin_user)
            db.commit()
            print("Default Admin user (ID: 1) created.")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    seed_database()

# --- CORS CONFIGURATION ---
# This allows your Next.js frontend (on port 3000) to talk to this backend (on port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Local frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# 2. Database Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. THE VAULT: Security Gatekeeper (RBAC)
def RequirePrivilege(required_permission: str):
    def require_privilege_dependency(db: Session = Depends(get_db)):
        # For now, we simulate a logged-in user. 
        # In a full system, this would come from a JWT Token.
        user = db.query(models.User).filter(models.User.id == 1).first() 
        
        if not user or not user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied: No role assigned."
            )
            
        user_permissions = user.role.permissions.split(",") if user.role.permissions else []
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access Denied: You require '{required_permission}' privilege."
            )
        return user
    return require_privilege_dependency

# --- ASSET ENDPOINTS ---

@app.get("/assets/", response_model=List[schemas.Asset])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Asset).offset(skip).limit(limit).all()

@app.post("/assets/", response_model=schemas.Asset, dependencies=[Depends(RequirePrivilege("create:asset"))])
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = models.Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@app.delete("/assets/{asset_id}", dependencies=[Depends(RequirePrivilege("delete:asset"))])
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return {"message": f"Asset {asset_id} deleted successfully"}

# --- USER & ROLE ENDPOINTS (For Setup) ---

@app.post("/roles/")
def create_role(name: str, permissions: str = "", db: Session = Depends(get_db)):
    new_role = models.Role(name=name, permissions=permissions)
    db.add(new_role)
    db.commit()
    return new_role