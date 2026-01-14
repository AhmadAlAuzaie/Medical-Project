"""
Integration tests for the Baby Risk Certification System.
"""

import pytest
import os
import tempfile
from datetime import datetime
from src.baby_risk_system import BabyRiskCertificationSystem
from src.models.baby_risk_models import RiskLevel, CertificationStatus


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
def system(temp_db):
    """Create a certification system with temporary database."""
    return BabyRiskCertificationSystem(temp_db)


def test_complete_workflow_low_risk(system):
    """Test complete workflow for a low-risk baby."""
    # Register baby
    baby_id = system.register_baby(
        name="Emma Johnson",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=39.0,
        birth_weight_grams=3500,
        medical_record_number="MRN001"
    )
    assert baby_id > 0
    
    # Record assessment
    assessment_id = system.record_assessment(
        baby_id=baby_id,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=9,
        apgar_score_5min=10,
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False,
        additional_notes="Normal delivery"
    )
    assert assessment_id > 0
    
    # Create certification
    cert_id = system.certify_risk(
        baby_id=baby_id,
        assessment_id=assessment_id,
        certified_by="Dr. Smith",
        notes="Low risk baby"
    )
    assert cert_id > 0
    
    # Verify certification
    certifications = system.get_baby_certifications(baby_id)
    assert len(certifications) == 1
    assert certifications[0].risk_level == RiskLevel.LOW
    assert certifications[0].certification_status == CertificationStatus.CERTIFIED


def test_complete_workflow_high_risk(system):
    """Test complete workflow for a high-risk baby."""
    # Register premature baby
    baby_id = system.register_baby(
        name="Noah Anderson",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=30.0,
        birth_weight_grams=1400,
        medical_record_number="MRN002"
    )
    
    # Record assessment with complications
    assessment_id = system.record_assessment(
        baby_id=baby_id,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=5,
        apgar_score_5min=7,
        has_respiratory_issues=True,
        has_infection=False,
        requires_intensive_care=True,
        additional_notes="Premature, requires NICU"
    )
    
    # Create certification
    cert_id = system.certify_risk(
        baby_id=baby_id,
        assessment_id=assessment_id,
        certified_by="Dr. Chen",
        notes="High risk, intensive monitoring required"
    )
    
    # Verify certification
    certifications = system.get_baby_certifications(baby_id)
    assert len(certifications) == 1
    assert certifications[0].risk_level == RiskLevel.HIGH
    assert certifications[0].risk_score == 70.0


def test_multiple_certifications_per_baby(system):
    """Test that a baby can have multiple certifications over time."""
    # Register baby
    baby_id = system.register_baby(
        name="Sophia Williams",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=35.0,
        birth_weight_grams=2300,
        medical_record_number="MRN003"
    )
    
    # First assessment - moderate risk
    assessment1_id = system.record_assessment(
        baby_id=baby_id,
        assessment_date=datetime(2025, 1, 1),
        apgar_score_1min=7,
        apgar_score_5min=9,
        has_respiratory_issues=True,
        has_infection=False,
        requires_intensive_care=False
    )
    
    cert1_id = system.certify_risk(
        baby_id=baby_id,
        assessment_id=assessment1_id,
        certified_by="Dr. Smith",
        certification_date=datetime(2025, 1, 1)
    )
    
    # Second assessment - improved
    assessment2_id = system.record_assessment(
        baby_id=baby_id,
        assessment_date=datetime(2025, 1, 3),
        apgar_score_1min=8,
        apgar_score_5min=10,
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False
    )
    
    cert2_id = system.certify_risk(
        baby_id=baby_id,
        assessment_id=assessment2_id,
        certified_by="Dr. Smith",
        certification_date=datetime(2025, 1, 3)
    )
    
    # Verify multiple certifications
    certifications = system.get_baby_certifications(baby_id)
    assert len(certifications) == 2


def test_get_baby_details(system):
    """Test retrieving baby details."""
    baby_id = system.register_baby(
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN004"
    )
    
    baby = system.get_baby(baby_id)
    assert baby is not None
    assert baby.name == "Test Baby"
    assert baby.gestational_age_weeks == 38.0
    assert baby.birth_weight_grams == 3000


def test_get_all_babies(system):
    """Test retrieving all registered babies."""
    # Register multiple babies
    for i in range(3):
        system.register_baby(
            name=f"Baby {i}",
            date_of_birth=datetime(2025, 1, i+1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number=f"MRN{i:03d}"
        )
    
    all_babies = system.get_all_babies()
    assert len(all_babies) == 3


def test_certification_without_baby_raises_error(system):
    """Test that certification fails if baby doesn't exist."""
    with pytest.raises(ValueError, match="Baby with ID .* not found"):
        system.certify_risk(
            baby_id=9999,
            assessment_id=1,
            certified_by="Dr. Test"
        )


def test_certification_without_assessment_raises_error(system):
    """Test that certification fails if assessment doesn't exist."""
    baby_id = system.register_baby(
        name="Test Baby",
        date_of_birth=datetime(2025, 1, 1),
        gestational_age_weeks=38.0,
        birth_weight_grams=3000,
        medical_record_number="MRN999"
    )
    
    with pytest.raises(ValueError, match="Assessment with ID .* not found"):
        system.certify_risk(
            baby_id=baby_id,
            assessment_id=9999,
            certified_by="Dr. Test"
        )
