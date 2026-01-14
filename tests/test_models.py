"""
Unit tests for the Baby Risk Certification System models.
"""

import pytest
from datetime import datetime
from src.models.baby_risk_models import (
    Baby, RiskAssessment, RiskCertification,
    RiskLevel, CertificationStatus
)


def test_baby_creation():
    """Test creating a Baby object."""
    baby = Baby(
        id=1,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN12345"
    )
    
    assert baby.id == 1
    assert baby.name == "Test Baby"
    assert baby.gestational_age_weeks == 38.0
    assert baby.birth_weight_grams == 3000
    assert baby.medical_record_number == "MRN12345"


def test_risk_assessment_creation():
    """Test creating a RiskAssessment object."""
    assessment = RiskAssessment(
        id=1,
        baby_id=1,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=8,
        apgar_score_5min=9,
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False,
        additional_notes="Normal assessment"
    )
    
    assert assessment.id == 1
    assert assessment.baby_id == 1
    assert assessment.apgar_score_1min == 8
    assert assessment.apgar_score_5min == 9
    assert not assessment.has_respiratory_issues
    assert not assessment.has_infection
    assert not assessment.requires_intensive_care


def test_risk_certification_creation():
    """Test creating a RiskCertification object."""
    cert = RiskCertification(
        id=1,
        baby_id=1,
        assessment_id=1,
        risk_level=RiskLevel.LOW,
        risk_score=15.0,
        certification_status=CertificationStatus.CERTIFIED,
        certification_date=datetime(2025, 1, 1),
        certified_by="Dr. Test",
        notes="Test certification"
    )
    
    assert cert.id == 1
    assert cert.baby_id == 1
    assert cert.assessment_id == 1
    assert cert.risk_level == RiskLevel.LOW
    assert cert.risk_score == 15.0
    assert cert.certification_status == CertificationStatus.CERTIFIED
    assert cert.certified_by == "Dr. Test"


def test_risk_level_enum():
    """Test RiskLevel enum values."""
    assert RiskLevel.LOW.value == "low"
    assert RiskLevel.MODERATE.value == "moderate"
    assert RiskLevel.HIGH.value == "high"
    assert RiskLevel.CRITICAL.value == "critical"


def test_certification_status_enum():
    """Test CertificationStatus enum values."""
    assert CertificationStatus.PENDING.value == "pending"
    assert CertificationStatus.CERTIFIED.value == "certified"
    assert CertificationStatus.UNDER_REVIEW.value == "under_review"
    assert CertificationStatus.REJECTED.value == "rejected"
