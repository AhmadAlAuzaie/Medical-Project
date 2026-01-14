"""
Sample data script for the Baby Risk Certification System.

This script demonstrates how to use the system and creates sample data.
"""

from datetime import datetime, timedelta
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.baby_risk_system import BabyRiskCertificationSystem


def create_sample_data():
    """Create sample retrospective data for baby risk certifications."""
    
    # Initialize the system
    system = BabyRiskCertificationSystem("sample_baby_risk.db")
    
    print("Creating sample retrospective data...")
    print("-" * 60)
    
    # Sample Baby 1: Low risk - full term, healthy
    baby1_id = system.register_baby(
        name="Emma Johnson",
        date_of_birth=datetime(2025, 6, 15),
        gestational_age_weeks=39.5,
        birth_weight_grams=3400,
        medical_record_number="MRN001234"
    )
    print(f"✓ Registered Baby 1 (ID: {baby1_id}): Emma Johnson - Full term, healthy")
    
    assessment1_id = system.record_assessment(
        baby_id=baby1_id,
        assessment_date=datetime(2025, 6, 15, 10, 30),
        apgar_score_1min=9,
        apgar_score_5min=10,
        has_respiratory_issues=False,
        has_infection=False,
        requires_intensive_care=False,
        additional_notes="Normal delivery, no complications"
    )
    print(f"  ✓ Recorded assessment (ID: {assessment1_id})")
    
    cert1_id = system.certify_risk(
        baby_id=baby1_id,
        assessment_id=assessment1_id,
        certified_by="Dr. Sarah Smith",
        certification_date=datetime(2025, 6, 15, 12, 0),
        notes="Low risk, cleared for standard post-natal care"
    )
    print(f"  ✓ Created certification (ID: {cert1_id})")
    
    # Sample Baby 2: Moderate risk - slightly premature
    baby2_id = system.register_baby(
        name="Liam Martinez",
        date_of_birth=datetime(2025, 7, 20),
        gestational_age_weeks=35.0,
        birth_weight_grams=2300,
        medical_record_number="MRN002345"
    )
    print(f"\n✓ Registered Baby 2 (ID: {baby2_id}): Liam Martinez - Premature, low birth weight")
    
    assessment2_id = system.record_assessment(
        baby_id=baby2_id,
        assessment_date=datetime(2025, 7, 20, 8, 15),
        apgar_score_1min=7,
        apgar_score_5min=9,
        has_respiratory_issues=True,
        has_infection=False,
        requires_intensive_care=False,
        additional_notes="Mild respiratory distress, resolved with oxygen support"
    )
    print(f"  ✓ Recorded assessment (ID: {assessment2_id})")
    
    cert2_id = system.certify_risk(
        baby_id=baby2_id,
        assessment_id=assessment2_id,
        certified_by="Dr. Michael Chen",
        certification_date=datetime(2025, 7, 20, 14, 30),
        notes="Moderate risk due to prematurity and respiratory issues"
    )
    print(f"  ✓ Created certification (ID: {cert2_id})")
    
    # Sample Baby 3: High risk - very premature, NICU required
    baby3_id = system.register_baby(
        name="Sophia Williams",
        date_of_birth=datetime(2025, 8, 10),
        gestational_age_weeks=30.0,
        birth_weight_grams=1400,
        medical_record_number="MRN003456"
    )
    print(f"\n✓ Registered Baby 3 (ID: {baby3_id}): Sophia Williams - Very premature, NICU")
    
    assessment3_id = system.record_assessment(
        baby_id=baby3_id,
        assessment_date=datetime(2025, 8, 10, 3, 45),
        apgar_score_1min=5,
        apgar_score_5min=7,
        has_respiratory_issues=True,
        has_infection=False,
        requires_intensive_care=True,
        additional_notes="Emergency C-section, requires ventilation support"
    )
    print(f"  ✓ Recorded assessment (ID: {assessment3_id})")
    
    cert3_id = system.certify_risk(
        baby_id=baby3_id,
        assessment_id=assessment3_id,
        certified_by="Dr. Sarah Smith",
        certification_date=datetime(2025, 8, 10, 6, 0),
        notes="High risk, requires intensive monitoring and respiratory support"
    )
    print(f"  ✓ Created certification (ID: {cert3_id})")
    
    # Sample Baby 4: Critical risk - extremely premature
    baby4_id = system.register_baby(
        name="Noah Anderson",
        date_of_birth=datetime(2025, 9, 5),
        gestational_age_weeks=26.5,
        birth_weight_grams=850,
        medical_record_number="MRN004567"
    )
    print(f"\n✓ Registered Baby 4 (ID: {baby4_id}): Noah Anderson - Extremely premature")
    
    assessment4_id = system.record_assessment(
        baby_id=baby4_id,
        assessment_date=datetime(2025, 9, 5, 1, 20),
        apgar_score_1min=3,
        apgar_score_5min=6,
        has_respiratory_issues=True,
        has_infection=True,
        requires_intensive_care=True,
        additional_notes="Extremely premature, multiple complications, infection suspected"
    )
    print(f"  ✓ Recorded assessment (ID: {assessment4_id})")
    
    cert4_id = system.certify_risk(
        baby_id=baby4_id,
        assessment_id=assessment4_id,
        certified_by="Dr. Michael Chen",
        certification_date=datetime(2025, 9, 5, 4, 15),
        notes="Critical risk, requires maximum intensive care and specialist consultation"
    )
    print(f"  ✓ Created certification (ID: {cert4_id})")
    
    print("\n" + "=" * 60)
    print("Sample data created successfully!")
    print(f"Database location: sample_baby_risk.db")
    print("=" * 60)
    
    # Display summary
    print("\nSummary of Risk Certifications:")
    print("-" * 60)
    
    for baby_id in [baby1_id, baby2_id, baby3_id, baby4_id]:
        baby = system.get_baby(baby_id)
        certifications = system.get_baby_certifications(baby_id)
        
        if certifications:
            cert = certifications[0]
            print(f"\n{baby.name} (MRN: {baby.medical_record_number})")
            print(f"  DOB: {baby.date_of_birth.strftime('%Y-%m-%d')}")
            print(f"  Gestational Age: {baby.gestational_age_weeks} weeks")
            print(f"  Birth Weight: {baby.birth_weight_grams}g")
            print(f"  Risk Level: {cert.risk_level.value.upper()}")
            print(f"  Risk Score: {cert.risk_score:.1f}/100")
            print(f"  Certified By: {cert.certified_by}")


if __name__ == "__main__":
    create_sample_data()
