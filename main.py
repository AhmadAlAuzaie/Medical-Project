#!/usr/bin/env python3
"""
Main script for Baby Risk Certification System.

This script demonstrates the functionality of the retrospective data
collection system for baby risk certifications.
"""

from datetime import datetime, timedelta
from models import Baby, RiskAssessment, RiskFactor, RiskCertification, RiskLevel, CertificationStatus
from data_manager import DataManager


def print_separator(char="=", length=70):
    """Print a separator line."""
    print(char * length)


def print_baby_info(baby: Baby):
    """Print detailed information about a baby."""
    print(f"\nBaby ID: {baby.id}")
    print(f"Name: {baby.first_name} {baby.last_name}")
    print(f"Date of Birth: {baby.date_of_birth.strftime('%Y-%m-%d')}")
    print(f"Gestational Age: {baby.gestational_age_weeks} weeks")
    print(f"Birth Weight: {baby.birth_weight_grams}g")
    print(f"Medical Record #: {baby.medical_record_number}")


def print_assessment_info(assessment: RiskAssessment):
    """Print detailed information about a risk assessment."""
    print(f"\nAssessment ID: {assessment.assessment_id}")
    print(f"Assessment Date: {assessment.assessment_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"Risk Score: {assessment.risk_score:.1f}/100")
    print(f"Risk Level: {assessment.overall_risk_level.value.upper()}")
    print(f"Assessed By: {assessment.assessed_by}")
    
    if assessment.risk_factors:
        print(f"\nRisk Factors ({len(assessment.risk_factors)}):")
        for rf in assessment.risk_factors:
            print(f"  - {rf.factor_name} (Severity: {rf.severity}/10)")
            print(f"    {rf.description}")
    else:
        print("\nNo risk factors identified")
    
    if assessment.notes:
        print(f"\nNotes: {assessment.notes}")


def print_certification_info(certification: RiskCertification):
    """Print detailed information about a certification."""
    print(f"\nCertification ID: {certification.certification_id}")
    print(f"Certification Date: {certification.certification_date.strftime('%Y-%m-%d')}")
    print(f"Valid Until: {certification.valid_until.strftime('%Y-%m-%d')}")
    print(f"Status: {certification.status.value.upper()}")
    print(f"Certified By: {certification.certified_by}")
    print(f"Currently Valid: {'Yes' if certification.is_valid() else 'No'}")
    
    if certification.recommendations:
        print(f"\nRecommendations:")
        for i, rec in enumerate(certification.recommendations, 1):
            print(f"  {i}. {rec}")


def demonstrate_system():
    """Demonstrate the Baby Risk Certification System."""
    print_separator()
    print("BABY RISK CERTIFICATION SYSTEM - RETROSPECTIVE DATA DEMO")
    print_separator()
    
    # Initialize data manager
    dm = DataManager()
    
    # Load sample data
    print("\n[1] Loading sample data from JSON file...")
    dm.load_from_json("sample_data.json")
    print(f"✓ Loaded {len(dm.babies)} babies, {len(dm.assessments)} assessments, "
          f"{len(dm.certifications)} certifications")
    
    # Display statistics
    print("\n[2] System Statistics:")
    print_separator("-")
    stats = dm.get_statistics()
    print(f"Total Babies: {stats['total_babies']}")
    print(f"Total Assessments: {stats['total_assessments']}")
    print(f"Total Certifications: {stats['total_certifications']}")
    print(f"Valid Certifications: {stats['valid_certifications']}")
    print("\nRisk Level Distribution:")
    for level, count in stats['risk_level_distribution'].items():
        print(f"  {level.capitalize()}: {count}")
    
    # Display individual baby records
    print("\n[3] Individual Baby Records:")
    print_separator("-")
    
    for baby_id in sorted(dm.babies.keys()):
        baby = dm.get_baby(baby_id)
        print_baby_info(baby)
        
        # Get assessments for this baby
        assessments = dm.get_assessments_for_baby(baby_id)
        if assessments:
            print(f"\n  Assessments for {baby.first_name}:")
            for assessment in assessments:
                print_assessment_info(assessment)
        
        # Get certifications for this baby
        certifications = dm.get_certifications_for_baby(baby_id)
        if certifications:
            print(f"\n  Certifications for {baby.first_name}:")
            for cert in certifications:
                print_certification_info(cert)
        
        print_separator("-")
    
    # Demonstrate adding a new baby with risk assessment
    print("\n[4] Adding New Baby to System:")
    print_separator("-")
    
    new_baby = Baby(
        id="B004",
        first_name="Noah",
        last_name="Brown",
        date_of_birth=datetime(2024, 5, 1, 9, 0),
        gestational_age_weeks=36.0,
        birth_weight_grams=2500,
        medical_record_number="MRN001237"
    )
    dm.add_baby(new_baby)
    print(f"✓ Added new baby: {new_baby.first_name} {new_baby.last_name}")
    
    # Create assessment for new baby
    risk_factors = [
        RiskFactor(
            factor_name="Moderate Prematurity",
            severity=5.0,
            description="Born at 36 weeks, slightly premature",
            identified_date=datetime(2024, 5, 1, 9, 0)
        ),
        RiskFactor(
            factor_name="Borderline Low Birth Weight",
            severity=4.0,
            description="Birth weight 2500g, at lower limit of normal",
            identified_date=datetime(2024, 5, 1, 9, 0)
        )
    ]
    
    new_assessment = RiskAssessment(
        assessment_id="A004",
        baby_id="B004",
        assessment_date=datetime(2024, 5, 1, 11, 0),
        risk_factors=risk_factors,
        assessed_by="Dr. Emily Thompson",
        notes="Late preterm infant requiring monitoring"
    )
    dm.add_assessment(new_assessment)
    print(f"✓ Created risk assessment with {len(risk_factors)} risk factors")
    print(f"  Risk Score: {new_assessment.risk_score:.1f}/100")
    print(f"  Risk Level: {new_assessment.overall_risk_level.value.upper()}")
    
    # Create certification for new baby
    new_certification = RiskCertification(
        certification_id="C004",
        baby_id="B004",
        assessment_id="A004",
        certification_date=datetime(2024, 5, 1, 14, 0),
        valid_until=datetime(2024, 8, 1, 14, 0),
        certified_by="Dr. Emily Thompson",
        recommendations=[
            "Monitor weight gain closely",
            "Weekly pediatric check-ups for first month",
            "Ensure adequate nutrition and feeding support"
        ]
    )
    dm.add_certification(new_certification)
    print(f"✓ Issued risk certification (valid until {new_certification.valid_until.strftime('%Y-%m-%d')})")
    
    # Save updated data
    print("\n[5] Saving Data:")
    print_separator("-")
    dm.save_to_json("risk_certification_data.json")
    print("✓ All data saved to data/risk_certification_data.json")
    
    # Display updated statistics
    print("\n[6] Updated System Statistics:")
    print_separator("-")
    final_stats = dm.get_statistics()
    print(f"Total Babies: {final_stats['total_babies']}")
    print(f"Total Assessments: {final_stats['total_assessments']}")
    print(f"Total Certifications: {final_stats['total_certifications']}")
    print(f"Valid Certifications: {final_stats['valid_certifications']}")
    
    # Show babies by risk level
    print("\n[7] Babies Grouped by Risk Level:")
    print_separator("-")
    for risk_level in RiskLevel:
        babies_at_level = dm.get_babies_by_risk_level(risk_level)
        print(f"\n{risk_level.value.upper()} Risk ({len(babies_at_level)} babies):")
        for baby in babies_at_level:
            print(f"  - {baby.first_name} {baby.last_name} (ID: {baby.id})")
    
    print("\n")
    print_separator()
    print("DEMO COMPLETED SUCCESSFULLY")
    print_separator()


if __name__ == "__main__":
    try:
        demonstrate_system()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
