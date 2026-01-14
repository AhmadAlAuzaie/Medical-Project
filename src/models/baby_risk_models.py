"""
Data models for the Baby Risk Certification System.

This module defines the core data structures for managing retrospective data
on risk certification for babies.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class RiskLevel(Enum):
    """Risk level classification for baby health assessments."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CertificationStatus(Enum):
    """Status of the risk certification process."""
    PENDING = "pending"
    CERTIFIED = "certified"
    UNDER_REVIEW = "under_review"
    REJECTED = "rejected"


@dataclass
class Baby:
    """
    Represents a baby in the risk certification system.
    
    Attributes:
        id: Unique identifier for the baby
        name: Baby's name
        date_of_birth: Baby's date of birth
        gestational_age_weeks: Gestational age at birth in weeks
        birth_weight_grams: Birth weight in grams
        medical_record_number: Hospital medical record number
    """
    id: Optional[int]
    name: str
    date_of_birth: datetime
    gestational_age_weeks: float
    birth_weight_grams: int
    medical_record_number: str


@dataclass
class RiskAssessment:
    """
    Represents a risk assessment for a baby.
    
    Attributes:
        id: Unique identifier for the assessment
        baby_id: Foreign key to the baby
        assessment_date: Date when assessment was performed
        apgar_score_1min: APGAR score at 1 minute
        apgar_score_5min: APGAR score at 5 minutes
        has_respiratory_issues: Whether baby has respiratory problems
        has_infection: Whether baby has signs of infection
        requires_intensive_care: Whether baby requires NICU care
        additional_notes: Any additional medical notes
    """
    id: Optional[int]
    baby_id: int
    assessment_date: datetime
    apgar_score_1min: int
    apgar_score_5min: int
    has_respiratory_issues: bool
    has_infection: bool
    requires_intensive_care: bool
    additional_notes: Optional[str] = None


@dataclass
class RiskCertification:
    """
    Represents a risk certification record.
    
    Attributes:
        id: Unique identifier for the certification
        baby_id: Foreign key to the baby
        assessment_id: Foreign key to the risk assessment
        risk_level: Calculated risk level
        risk_score: Numeric risk score (0-100)
        certification_status: Status of certification
        certification_date: Date when certification was issued
        certified_by: Name of certifying healthcare professional
        notes: Additional certification notes
    """
    id: Optional[int]
    baby_id: int
    assessment_id: int
    risk_level: RiskLevel
    risk_score: float
    certification_status: CertificationStatus
    certification_date: datetime
    certified_by: str
    notes: Optional[str] = None
