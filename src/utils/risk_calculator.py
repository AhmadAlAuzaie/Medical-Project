"""
Risk calculation utilities for baby health assessments.

This module implements the risk scoring algorithm based on multiple
clinical factors to determine the risk level for newborns.
"""

from ..models.baby_risk_models import Baby, RiskAssessment, RiskLevel


class RiskCalculator:
    """
    Calculates risk scores and levels for babies based on clinical data.
    
    The risk score is calculated based on multiple factors:
    - Gestational age (premature births are higher risk)
    - Birth weight (low birth weight increases risk)
    - APGAR scores (lower scores indicate higher risk)
    - Clinical conditions (respiratory issues, infections, ICU requirement)
    """
    
    # Risk score thresholds
    LOW_THRESHOLD = 25.0
    MODERATE_THRESHOLD = 50.0
    HIGH_THRESHOLD = 75.0
    
    @staticmethod
    def calculate_risk_score(baby: Baby, assessment: RiskAssessment) -> float:
        """
        Calculate a comprehensive risk score (0-100) based on baby and assessment data.
        
        Args:
            baby: Baby object containing birth information
            assessment: RiskAssessment object containing clinical data
            
        Returns:
            Risk score between 0 and 100
        """
        score = 0.0
        
        # Gestational age component (0-20 points)
        if baby.gestational_age_weeks < 28:
            score += 20  # Extremely premature
        elif baby.gestational_age_weeks < 32:
            score += 15  # Very premature
        elif baby.gestational_age_weeks < 37:
            score += 10  # Premature
        else:
            score += 0   # Term or post-term
        
        # Birth weight component (0-20 points)
        if baby.birth_weight_grams < 1000:
            score += 20  # Extremely low birth weight
        elif baby.birth_weight_grams < 1500:
            score += 15  # Very low birth weight
        elif baby.birth_weight_grams < 2500:
            score += 10  # Low birth weight
        else:
            score += 0   # Normal birth weight
        
        # APGAR score at 1 minute (0-15 points)
        if assessment.apgar_score_1min <= 3:
            score += 15  # Critically low
        elif assessment.apgar_score_1min <= 6:
            score += 10  # Low
        else:
            score += 0   # Normal
        
        # APGAR score at 5 minutes (0-15 points)
        if assessment.apgar_score_5min <= 6:
            score += 15  # Low - indicates persistent problems
        elif assessment.apgar_score_5min <= 8:
            score += 5   # Slightly low
        else:
            score += 0   # Normal
        
        # Clinical conditions (0-30 points total)
        if assessment.requires_intensive_care:
            score += 15
        if assessment.has_respiratory_issues:
            score += 10
        if assessment.has_infection:
            score += 5
        
        # Ensure score is within bounds
        return min(100.0, max(0.0, score))
    
    @classmethod
    def determine_risk_level(cls, risk_score: float) -> RiskLevel:
        """
        Determine the risk level category based on risk score.
        
        Args:
            risk_score: Numeric risk score (0-100)
            
        Returns:
            RiskLevel enum value
        """
        if risk_score < cls.LOW_THRESHOLD:
            return RiskLevel.LOW
        elif risk_score < cls.MODERATE_THRESHOLD:
            return RiskLevel.MODERATE
        elif risk_score < cls.HIGH_THRESHOLD:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    @classmethod
    def calculate_risk(cls, baby: Baby, assessment: RiskAssessment) -> tuple[float, RiskLevel]:
        """
        Calculate both risk score and risk level.
        
        Args:
            baby: Baby object containing birth information
            assessment: RiskAssessment object containing clinical data
            
        Returns:
            Tuple of (risk_score, risk_level)
        """
        risk_score = cls.calculate_risk_score(baby, assessment)
        risk_level = cls.determine_risk_level(risk_score)
        return risk_score, risk_level
