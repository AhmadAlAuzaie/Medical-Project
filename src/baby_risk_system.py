"""
Baby Risk Certification System

Main module for managing retrospective data on risk certification for babies.
Provides functionality to record, assess, and certify risk levels for newborns
based on clinical data.
"""

from datetime import datetime
from typing import List, Optional

from .models.baby_risk_models import (
    Baby, RiskAssessment, RiskCertification,
    RiskLevel, CertificationStatus
)
from .database.database_manager import DatabaseManager
from .utils.risk_calculator import RiskCalculator


class BabyRiskCertificationSystem:
    """
    Main system for managing baby risk certifications.
    
    This system provides a complete workflow for:
    1. Registering babies with birth information
    2. Recording clinical risk assessments
    3. Calculating risk scores and levels
    4. Issuing risk certifications
    """
    
    def __init__(self, db_path: str = "baby_risk_certification.db"):
        """
        Initialize the certification system.
        
        Args:
            db_path: Path to the database file
        """
        self.db = DatabaseManager(db_path)
        self.risk_calculator = RiskCalculator()
    
    def register_baby(self, name: str, date_of_birth: datetime,
                     gestational_age_weeks: float, birth_weight_grams: int,
                     medical_record_number: str) -> int:
        """
        Register a new baby in the system.
        
        Args:
            name: Baby's name
            date_of_birth: Date of birth
            gestational_age_weeks: Gestational age at birth in weeks
            birth_weight_grams: Birth weight in grams
            medical_record_number: Hospital medical record number
            
        Returns:
            ID of the newly registered baby
        """
        baby = Baby(
            id=None,
            name=name,
            date_of_birth=date_of_birth,
            gestational_age_weeks=gestational_age_weeks,
            birth_weight_grams=birth_weight_grams,
            medical_record_number=medical_record_number
        )
        return self.db.add_baby(baby)
    
    def record_assessment(self, baby_id: int, assessment_date: datetime,
                         apgar_score_1min: int, apgar_score_5min: int,
                         has_respiratory_issues: bool, has_infection: bool,
                         requires_intensive_care: bool,
                         additional_notes: Optional[str] = None) -> int:
        """
        Record a risk assessment for a baby.
        
        Args:
            baby_id: ID of the baby
            assessment_date: Date of assessment
            apgar_score_1min: APGAR score at 1 minute (0-10)
            apgar_score_5min: APGAR score at 5 minutes (0-10)
            has_respiratory_issues: Whether baby has respiratory problems
            has_infection: Whether baby has infection
            requires_intensive_care: Whether baby requires NICU care
            additional_notes: Optional additional notes
            
        Returns:
            ID of the newly created assessment
        """
        assessment = RiskAssessment(
            id=None,
            baby_id=baby_id,
            assessment_date=assessment_date,
            apgar_score_1min=apgar_score_1min,
            apgar_score_5min=apgar_score_5min,
            has_respiratory_issues=has_respiratory_issues,
            has_infection=has_infection,
            requires_intensive_care=requires_intensive_care,
            additional_notes=additional_notes
        )
        return self.db.add_risk_assessment(assessment)
    
    def certify_risk(self, baby_id: int, assessment_id: int,
                    certified_by: str, certification_date: Optional[datetime] = None,
                    notes: Optional[str] = None) -> int:
        """
        Create a risk certification based on baby and assessment data.
        
        This method automatically calculates the risk score and level.
        
        Args:
            baby_id: ID of the baby
            assessment_id: ID of the risk assessment
            certified_by: Name of the certifying healthcare professional
            certification_date: Date of certification (defaults to now)
            notes: Optional certification notes
            
        Returns:
            ID of the newly created certification
            
        Raises:
            ValueError: If baby or assessment not found
        """
        # Retrieve baby and assessment data
        baby = self.db.get_baby(baby_id)
        assessment = self.db.get_risk_assessment(assessment_id)
        
        if not baby:
            raise ValueError(f"Baby with ID {baby_id} not found")
        if not assessment:
            raise ValueError(f"Assessment with ID {assessment_id} not found")
        
        # Calculate risk score and level
        risk_score, risk_level = self.risk_calculator.calculate_risk(baby, assessment)
        
        # Create certification
        certification = RiskCertification(
            id=None,
            baby_id=baby_id,
            assessment_id=assessment_id,
            risk_level=risk_level,
            risk_score=risk_score,
            certification_status=CertificationStatus.CERTIFIED,
            certification_date=certification_date or datetime.now(),
            certified_by=certified_by,
            notes=notes
        )
        
        return self.db.add_risk_certification(certification)
    
    def get_baby_certifications(self, baby_id: int) -> List[RiskCertification]:
        """
        Get all certifications for a specific baby.
        
        Args:
            baby_id: ID of the baby
            
        Returns:
            List of RiskCertification objects
        """
        return self.db.get_certifications_by_baby(baby_id)
    
    def get_all_babies(self) -> List[Baby]:
        """
        Get all registered babies.
        
        Returns:
            List of Baby objects
        """
        return self.db.get_all_babies()
    
    def get_baby(self, baby_id: int) -> Optional[Baby]:
        """
        Get a specific baby by ID.
        
        Args:
            baby_id: ID of the baby
            
        Returns:
            Baby object or None if not found
        """
        return self.db.get_baby(baby_id)
