from pydantic import BaseModel

class AssetBase(BaseModel):
    name: str
    category: str
    serial_number: str
    status: str = "Available"

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True