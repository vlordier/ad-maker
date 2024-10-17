# state_schemas.py
from pydantic import BaseModel, Field, conint, constr, ValidationError, validator
from typing import List, Optional

class MainState(BaseModel):
    ad_duration: Optional[conint(ge=0, le=60)] = None  # Ad duration must be between 0-60 seconds
    ad_channel: Optional[constr(min_length=3, max_length=30)] = None  # Channel name
    ad_theme: Optional[constr(min_length=10, max_length=200)] = None  # Theme description (50 words approx.)
    
    ad_concept: Optional[str] = None  # Generated Ad Concept
    storyboard: Optional[List[str]] = None  # Generated Storyboard scenes

    retry_counts: dict = Field(default_factory=dict)  # Retry counts for each step
    task_success: bool = False  # Success status of each task
    messages: List[str] = Field(default_factory=list)  # List of messages for LLM feedback

    @validator('ad_duration')
    def validate_duration(cls, value):
        if value is None or not (0 <= value <= 60):
            raise ValueError('Ad Duration must be between 0 and 60 seconds.')
        return value
    
    @validator('ad_theme')
    def validate_theme(cls, value):
        if len(value.split()) < 10:
            raise ValueError('Ad Theme should be at least 10 words.')
        return value

    @validator('ad_channel')
    def validate_channel(cls, value):
        if value not in ['Facebook', 'Instagram', 'TikTok']:
            raise ValueError('Invalid Ad Channel. Choose from Facebook, Instagram, TikTok.')
        return value
