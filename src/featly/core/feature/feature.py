from .defs import ValueType, FeatureType

from pydantic import BaseModel, Field
from datetime import datetime

from typing import (
    Any,
    Dict,
    List,
    Optional,
)

class Feature(BaseModel):
    name: str = Field(..., description="Feature name")
    description: Optional[str] = Field(None, description="Feature description")
    value_type: ValueType = Field(..., description="Data type of the feature")
    feature_type: FeatureType = Field(..., description="Type of the feature")
    entity: str = Field(..., description="Entity this feature belongs to")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    version: str = Field(default="1.0.0", description="Feature version")
    tags: List[str] = Field(default_factory=list, description="Tags for feature categorization")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def update_version(self, new_version: str):
        """Update feature version and updated_at timestamp"""
        self.version = new_version
        self.updated_at = datetime.utcnow()