"""
Data models for Baby Risk Certification System.

This module defines the core data structures for managing retrospective
data on risk certification for babies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict


class RiskLevel(Enum):
    """Risk level classification for babies."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CertificationStatus(Enum):
    """Status of risk certification."""
    PENDING = "pending"
    CERTIFIED = "certified"
    REQUIRES_REVIEW = "requires_review"
    EXPIRED = "expired"


@dataclass
class Baby:
    """
    Represents a baby in the risk certification system.
    
    Attributes:
        id: Unique identifier for the baby
        first_name: Baby's first name
        last_name: Baby's last name
        date_of_birth: Date of birth
        gestational_age_weeks: Gestational age at birth (in weeks)
        birth_weight_grams: Birth weight in grams
        medical_record_number: Hospital medical record number
    """
    id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gestational_age_weeks: float
    birth_weight_grams: int
    medical_record_number: str
    
    def __post_init__(self):
        """Validate baby data after initialization."""
        if self.gestational_age_weeks < 20 or self.gestational_age_weeks > 44:
            raise ValueError("Gestational age must be between 20 and 44 weeks")
        if self.birth_weight_grams < 300 or self.birth_weight_grams > 6000:
            raise ValueError("Birth weight must be between 300 and 6000 grams")


@dataclass
class RiskFactor:
    """
    Represents a specific risk factor for a baby.
    
    Attributes:
        factor_name: Name of the risk factor
        severity: Numerical severity score (0-10)
        description: Description of the risk factor
        identified_date: When this risk factor was identified
    """
    factor_name: str
    severity: float
    description: str
    identified_date: datetime
    
    def __post_init__(self):
        """Validate risk factor data."""
        if self.severity < 0 or self.severity > 10:
            raise ValueError("Severity must be between 0 and 10")


@dataclass
class RiskAssessment:
    """
    Comprehensive risk assessment for a baby.
    
    Attributes:
        assessment_id: Unique identifier for this assessment
        baby_id: Reference to the baby being assessed
        assessment_date: Date of the assessment
        risk_factors: List of identified risk factors
        overall_risk_level: Calculated overall risk level
        risk_score: Numerical risk score (0-100)
        notes: Additional notes from healthcare provider
        assessed_by: Name of healthcare provider who performed assessment
    """
    assessment_id: str
    baby_id: str
    assessment_date: datetime
    risk_factors: List[RiskFactor] = field(default_factory=list)
    overall_risk_level: RiskLevel = RiskLevel.LOW
    risk_score: float = 0.0
    notes: str = ""
    assessed_by: str = ""
    
    def calculate_risk_score(self) -> float:
        """
        Calculate the overall risk score based on risk factors.
        
        Returns:
            Risk score between 0 and 100
        """
        if not self.risk_factors:
            return 0.0
        
        # Calculate weighted average of risk factors
        total_severity = sum(factor.severity for factor in self.risk_factors)
        avg_severity = total_severity / len(self.risk_factors)
        
        # Convert to 0-100 scale
        risk_score = avg_severity * 10
        
        self.risk_score = min(100.0, max(0.0, risk_score))
        return self.risk_score
    
    def determine_risk_level(self) -> RiskLevel:
        """
        Determine the overall risk level based on risk score.
        
        Returns:
            RiskLevel enum value
        """
        score = self.risk_score if self.risk_score > 0 else self.calculate_risk_score()
        
        if score < 25:
            self.overall_risk_level = RiskLevel.LOW
        elif score < 50:
            self.overall_risk_level = RiskLevel.MODERATE
        elif score < 75:
            self.overall_risk_level = RiskLevel.HIGH
        else:
            self.overall_risk_level = RiskLevel.CRITICAL
        
        return self.overall_risk_level


@dataclass
class RiskCertification:
    """
    Official risk certification for a baby.
    
    Attributes:
        certification_id: Unique identifier for this certification
        baby_id: Reference to the baby
        assessment_id: Reference to the risk assessment
        certification_date: Date certification was issued
        valid_until: Expiration date of certification
        status: Current status of certification
        certified_by: Healthcare provider who certified
        recommendations: List of recommendations based on risk assessment
    """
    certification_id: str
    baby_id: str
    assessment_id: str
    certification_date: datetime
    valid_until: datetime
    status: CertificationStatus = CertificationStatus.CERTIFIED
    certified_by: str = ""
    recommendations: List[str] = field(default_factory=list)
    
    def is_valid(self) -> bool:
        """
        Check if the certification is currently valid.
        
        Returns:
            True if certification is valid and not expired
        """
        if self.status == CertificationStatus.EXPIRED:
            return False
        
        if datetime.now() > self.valid_until:
            self.status = CertificationStatus.EXPIRED
            return False
        
        return self.status == CertificationStatus.CERTIFIED
    
    def check_expiration(self) -> None:
        """Update status if certification has expired."""
        if datetime.now() > self.valid_until and self.status == CertificationStatus.CERTIFIED:
            self.status = CertificationStatus.EXPIRED
