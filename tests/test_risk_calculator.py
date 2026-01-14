"""
Unit tests for the risk calculation utilities.
"""

import pytest
from datetime import datetime
from src.models.baby_risk_models import Baby, RiskAssessment, RiskLevel
from src.utils.risk_calculator import RiskCalculator


def test_risk_calculator_low_risk():
    """Test risk calculation for a low-risk baby."""
    baby = Baby(
        id=1,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=39.0,  # Full term
        birth_weight_grams=3500,      # Normal weight
        medical_record_number="MRN001"
    )
    
    assessment = RiskAssessment(
        id=1,
        baby_id=1,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=9,  # Excellent
        apgar_score_5min=10, # Excellent
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False
    )
    
    calculator = RiskCalculator()
    score, level = calculator.calculate_risk(baby, assessment)
    
    assert score == 0.0
    assert level == RiskLevel.LOW


def test_risk_calculator_moderate_risk():
    """Test risk calculation for a moderate-risk baby."""
    baby = Baby(
        id=1,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=35.0,  # Premature
        birth_weight_grams=2300,      # Low birth weight
        medical_record_number="MRN002"
    )
    
    assessment = RiskAssessment(
        id=1,
        baby_id=1,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=7,
        apgar_score_5min=9,
        has_respiratory_issues=True,
        has_infection=False,
        requires_intensive_care=False
    )
    
    calculator = RiskCalculator()
    score, level = calculator.calculate_risk(baby, assessment)
    
    assert score == 30.0  # 10 (gestational) + 10 (weight) + 10 (respiratory)
    assert level == RiskLevel.MODERATE


def test_risk_calculator_high_risk():
    """Test risk calculation for a high-risk baby."""
    baby = Baby(
        id=1,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=30.0,  # Very premature
        birth_weight_grams=1400,      # Very low birth weight
        medical_record_number="MRN003"
    )
    
    assessment = RiskAssessment(
        id=1,
        baby_id=1,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=5,
        apgar_score_5min=7,
        has_respiratory_issues=True,
        has_infection=False,
        requires_intensive_care=True
    )
    
    calculator = RiskCalculator()
    score, level = calculator.calculate_risk(baby, assessment)
    
    # 15 (gestational) + 15 (weight) + 10 (apgar1) + 5 (apgar5) + 10 (respiratory) + 15 (icu) = 70
    assert score == 70.0
    assert level == RiskLevel.HIGH


def test_risk_calculator_critical_risk():
    """Test risk calculation for a critical-risk baby."""
    baby = Baby(
        id=1,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=27.0,  # Extremely premature
        birth_weight_grams=900,       # Extremely low birth weight
        medical_record_number="MRN004"
    )
    
    assessment = RiskAssessment(
        id=1,
        baby_id=1,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=3,
        apgar_score_5min=6,
        has_respiratory_issues=True,
        has_infection=True,
        requires_intensive_care=True
    )
    
    calculator = RiskCalculator()
    score, level = calculator.calculate_risk(baby, assessment)
    
    # 20 (gestational) + 20 (weight) + 15 (apgar1) + 15 (apgar5) + 10 (respiratory) + 5 (infection) + 15 (icu) = 100
    assert score == 100.0
    assert level == RiskLevel.CRITICAL


def test_risk_level_thresholds():
    """Test risk level determination based on score thresholds."""
    calculator = RiskCalculator()
    
    assert calculator.determine_risk_level(0.0) == RiskLevel.LOW
    assert calculator.determine_risk_level(24.9) == RiskLevel.LOW
    assert calculator.determine_risk_level(25.0) == RiskLevel.MODERATE
    assert calculator.determine_risk_level(49.9) == RiskLevel.MODERATE
    assert calculator.determine_risk_level(50.0) == RiskLevel.HIGH
    assert calculator.determine_risk_level(74.9) == RiskLevel.HIGH
    assert calculator.determine_risk_level(75.0) == RiskLevel.CRITICAL
    assert calculator.determine_risk_level(100.0) == RiskLevel.CRITICAL


def test_calculate_risk_score_bounds():
    """Test that risk scores stay within 0-100 bounds."""
    calculator = RiskCalculator()
    
    # Create worst case scenario
    baby = Baby(
        id=1,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=25.0,
        birth_weight_grams=500,
        medical_record_number="MRN005"
    )
    
    assessment = RiskAssessment(
        id=1,
        baby_id=1,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=0,
        apgar_score_5min=0,
        has_respiratory_issues=True,
        has_infection=True,
        requires_intensive_care=True
    )
    
    score = calculator.calculate_risk_score(baby, assessment)
    
    assert 0.0 <= score <= 100.0
