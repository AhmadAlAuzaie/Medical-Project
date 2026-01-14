"""
Unit tests for the database manager.
"""

import pytest
import os
import tempfile
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.models.baby_risk_models import (
    Baby, RiskAssessment, RiskCertification,
    RiskLevel, CertificationStatus
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def db_manager(temp_db):
    """Create a database manager with temporary database."""
    return DatabaseManager(temp_db)


def test_database_initialization(temp_db):
    """Test that database is initialized with proper schema."""
    db = DatabaseManager(temp_db)
    assert os.path.exists(temp_db)


def test_add_and_get_baby(db_manager):
    """Test adding and retrieving a baby."""
    baby = Baby(
        id=None,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN12345"
    )
    
    baby_id = db_manager.add_baby(baby)
    assert baby_id > 0
    
    retrieved_baby = db_manager.get_baby(baby_id)
    assert retrieved_baby is not None
    assert retrieved_baby.name == "Test Baby"
    assert retrieved_baby.gestational_age_weeks == 38.0
    assert retrieved_baby.birth_weight_grams == 3000
    assert retrieved_baby.medical_record_number == "MRN12345"


def test_add_and_get_risk_assessment(db_manager):
    """Test adding and retrieving a risk assessment."""
    # First add a baby
    baby = Baby(
        id=None,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN12345"
    )
    baby_id = db_manager.add_baby(baby)
    
    # Add assessment
    assessment = RiskAssessment(
        id=None,
        baby_id=baby_id,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=8,
        apgar_score_5min=9,
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False,
        additional_notes="Test notes"
    )
    
    assessment_id = db_manager.add_risk_assessment(assessment)
    assert assessment_id > 0
    
    retrieved_assessment = db_manager.get_risk_assessment(assessment_id)
    assert retrieved_assessment is not None
    assert retrieved_assessment.baby_id == baby_id
    assert retrieved_assessment.apgar_score_1min == 8
    assert retrieved_assessment.apgar_score_5min == 9
    assert not retrieved_assessment.has_respiratory_issues


def test_add_and_get_risk_certification(db_manager):
    """Test adding and retrieving a risk certification."""
    # Add baby
    baby = Baby(
        id=None,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN12345"
    )
    baby_id = db_manager.add_baby(baby)
    
    # Add assessment
    assessment = RiskAssessment(
        id=None,
        baby_id=baby_id,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=8,
        apgar_score_5min=9,
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False
    )
    assessment_id = db_manager.add_risk_assessment(assessment)
    
    # Add certification
    certification = RiskCertification(
        id=None,
        baby_id=baby_id,
        assessment_id=assessment_id,
        risk_level=RiskLevel.LOW,
        risk_score=15.0,
        certification_status=CertificationStatus.CERTIFIED,
        certification_date=datetime(2025, 1, 1),
        certified_by="Dr. Test",
        notes="Test certification"
    )
    
    cert_id = db_manager.add_risk_certification(certification)
    assert cert_id > 0
    
    retrieved_cert = db_manager.get_risk_certification(cert_id)
    assert retrieved_cert is not None
    assert retrieved_cert.baby_id == baby_id
    assert retrieved_cert.assessment_id == assessment_id
    assert retrieved_cert.risk_level == RiskLevel.LOW
    assert retrieved_cert.risk_score == 15.0
    assert retrieved_cert.certified_by == "Dr. Test"


def test_get_certifications_by_baby(db_manager):
    """Test retrieving all certifications for a baby."""
    # Add baby
    baby = Baby(
        id=None,
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN12345"
    )
    baby_id = db_manager.add_baby(baby)
    
    # Add multiple assessments and certifications
    for i in range(3):
        assessment = RiskAssessment(
            id=None,
            baby_id=baby_id,
            assessment_date=datetime(2025, 1, i+1),
            apgar_score_1min=8,
            apgar_score_5min=9,
            has_respiratory_issues=False,
            has_infection=False,
            requires_intensive_care=False
        )
        assessment_id = db_manager.add_risk_assessment(assessment)
        
        certification = RiskCertification(
            id=None,
            baby_id=baby_id,
            assessment_id=assessment_id,
            risk_level=RiskLevel.LOW,
            risk_score=15.0,
            certification_status=CertificationStatus.CERTIFIED,
            certification_date=datetime(2025, 1, i+1),
            certified_by="Dr. Test"
        )
        db_manager.add_risk_certification(certification)
    
    certifications = db_manager.get_certifications_by_baby(baby_id)
    assert len(certifications) == 3


def test_get_all_babies(db_manager):
    """Test retrieving all babies."""
    # Add multiple babies
    for i in range(5):
        baby = Baby(
            id=None,
            name=f"Baby {i}",
            date_of_birth=datetime(2025, 1, i+1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number=f"MRN{i:05d}"
        )
        db_manager.add_baby(baby)
    
    all_babies = db_manager.get_all_babies()
    assert len(all_babies) == 5


def test_get_nonexistent_baby(db_manager):
    """Test retrieving a baby that doesn't exist."""
    baby = db_manager.get_baby(9999)
    assert baby is None
