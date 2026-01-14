"""
Unit tests for the Baby Risk Certification System.

Tests for data models, risk calculations, and data management.
"""

import unittest
from datetime import datetime, timedelta
from models import (
    Baby, RiskFactor, RiskAssessment, RiskCertification,
    RiskLevel, CertificationStatus
)
from data_manager import DataManager
import tempfile
import shutil


class TestBabyModel(unittest.TestCase):
    """Test cases for Baby model."""
    
    def test_create_valid_baby(self):
        """Test creating a valid baby."""
        baby = Baby(
            id="B001",
            first_name="Test",
            last_name="Baby",
            date_of_birth=datetime(2024, 1, 1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number="MRN001"
        )
        self.assertEqual(baby.id, "B001")
        self.assertEqual(baby.first_name, "Test")
        self.assertEqual(baby.gestational_age_weeks, 38.0)
    
    def test_invalid_gestational_age_low(self):
        """Test that gestational age below 20 weeks raises error."""
        with self.assertRaises(ValueError):
            Baby(
                id="B001",
                first_name="Test",
                last_name="Baby",
                date_of_birth=datetime(2024, 1, 1),
                gestational_age_weeks=15.0,
                birth_weight_grams=3000,
                medical_record_number="MRN001"
            )
    
    def test_invalid_gestational_age_high(self):
        """Test that gestational age above 44 weeks raises error."""
        with self.assertRaises(ValueError):
            Baby(
                id="B001",
                first_name="Test",
                last_name="Baby",
                date_of_birth=datetime(2024, 1, 1),
                gestational_age_weeks=45.0,
                birth_weight_grams=3000,
                medical_record_number="MRN001"
            )
    
    def test_invalid_birth_weight_low(self):
        """Test that birth weight below 300g raises error."""
        with self.assertRaises(ValueError):
            Baby(
                id="B001",
                first_name="Test",
                last_name="Baby",
                date_of_birth=datetime(2024, 1, 1),
                gestational_age_weeks=38.0,
                birth_weight_grams=200,
                medical_record_number="MRN001"
            )
    
    def test_invalid_birth_weight_high(self):
        """Test that birth weight above 6000g raises error."""
        with self.assertRaises(ValueError):
            Baby(
                id="B001",
                first_name="Test",
                last_name="Baby",
                date_of_birth=datetime(2024, 1, 1),
                gestational_age_weeks=38.0,
                birth_weight_grams=7000,
                medical_record_number="MRN001"
            )


class TestRiskFactor(unittest.TestCase):
    """Test cases for RiskFactor model."""
    
    def test_create_valid_risk_factor(self):
        """Test creating a valid risk factor."""
        rf = RiskFactor(
            factor_name="Test Factor",
            severity=5.0,
            description="Test description",
            identified_date=datetime.now()
        )
        self.assertEqual(rf.factor_name, "Test Factor")
        self.assertEqual(rf.severity, 5.0)
    
    def test_invalid_severity_low(self):
        """Test that severity below 0 raises error."""
        with self.assertRaises(ValueError):
            RiskFactor(
                factor_name="Test Factor",
                severity=-1.0,
                description="Test description",
                identified_date=datetime.now()
            )
    
    def test_invalid_severity_high(self):
        """Test that severity above 10 raises error."""
        with self.assertRaises(ValueError):
            RiskFactor(
                factor_name="Test Factor",
                severity=11.0,
                description="Test description",
                identified_date=datetime.now()
            )


class TestRiskAssessment(unittest.TestCase):
    """Test cases for RiskAssessment model."""
    
    def test_calculate_risk_score_no_factors(self):
        """Test risk score calculation with no risk factors."""
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_factors=[]
        )
        score = assessment.calculate_risk_score()
        self.assertEqual(score, 0.0)
    
    def test_calculate_risk_score_single_factor(self):
        """Test risk score calculation with single risk factor."""
        rf = RiskFactor(
            factor_name="Test",
            severity=5.0,
            description="Test",
            identified_date=datetime.now()
        )
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_factors=[rf]
        )
        score = assessment.calculate_risk_score()
        self.assertEqual(score, 50.0)
    
    def test_calculate_risk_score_multiple_factors(self):
        """Test risk score calculation with multiple risk factors."""
        rf1 = RiskFactor(
            factor_name="Test1",
            severity=4.0,
            description="Test1",
            identified_date=datetime.now()
        )
        rf2 = RiskFactor(
            factor_name="Test2",
            severity=6.0,
            description="Test2",
            identified_date=datetime.now()
        )
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_factors=[rf1, rf2]
        )
        score = assessment.calculate_risk_score()
        self.assertEqual(score, 50.0)  # (4 + 6) / 2 * 10 = 50
    
    def test_determine_risk_level_low(self):
        """Test risk level determination for low risk."""
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_score=20.0
        )
        level = assessment.determine_risk_level()
        self.assertEqual(level, RiskLevel.LOW)
    
    def test_determine_risk_level_moderate(self):
        """Test risk level determination for moderate risk."""
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_score=35.0
        )
        level = assessment.determine_risk_level()
        self.assertEqual(level, RiskLevel.MODERATE)
    
    def test_determine_risk_level_high(self):
        """Test risk level determination for high risk."""
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_score=60.0
        )
        level = assessment.determine_risk_level()
        self.assertEqual(level, RiskLevel.HIGH)
    
    def test_determine_risk_level_critical(self):
        """Test risk level determination for critical risk."""
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_score=80.0
        )
        level = assessment.determine_risk_level()
        self.assertEqual(level, RiskLevel.CRITICAL)


class TestRiskCertification(unittest.TestCase):
    """Test cases for RiskCertification model."""
    
    def test_is_valid_certified(self):
        """Test certification validity check for valid certification."""
        cert = RiskCertification(
            certification_id="C001",
            baby_id="B001",
            assessment_id="A001",
            certification_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=30),
            status=CertificationStatus.CERTIFIED
        )
        self.assertTrue(cert.is_valid())
    
    def test_is_valid_expired_status(self):
        """Test certification validity check for expired status."""
        cert = RiskCertification(
            certification_id="C001",
            baby_id="B001",
            assessment_id="A001",
            certification_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=30),
            status=CertificationStatus.EXPIRED
        )
        self.assertFalse(cert.is_valid())
    
    def test_is_valid_past_date(self):
        """Test certification validity check for past expiration date."""
        cert = RiskCertification(
            certification_id="C001",
            baby_id="B001",
            assessment_id="A001",
            certification_date=datetime.now() - timedelta(days=60),
            valid_until=datetime.now() - timedelta(days=30),
            status=CertificationStatus.CERTIFIED
        )
        self.assertFalse(cert.is_valid())
        self.assertEqual(cert.status, CertificationStatus.EXPIRED)


class TestDataManager(unittest.TestCase):
    """Test cases for DataManager."""
    
    def setUp(self):
        """Set up temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.dm = DataManager(data_directory=self.temp_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)
    
    def test_add_and_get_baby(self):
        """Test adding and retrieving a baby."""
        baby = Baby(
            id="B001",
            first_name="Test",
            last_name="Baby",
            date_of_birth=datetime(2024, 1, 1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number="MRN001"
        )
        self.dm.add_baby(baby)
        retrieved = self.dm.get_baby("B001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.first_name, "Test")
    
    def test_get_nonexistent_baby(self):
        """Test retrieving a baby that doesn't exist."""
        retrieved = self.dm.get_baby("B999")
        self.assertIsNone(retrieved)
    
    def test_add_and_get_assessment(self):
        """Test adding and retrieving an assessment."""
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_factors=[]
        )
        self.dm.add_assessment(assessment)
        retrieved = self.dm.get_assessment("A001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.assessment_id, "A001")
    
    def test_get_assessments_for_baby(self):
        """Test getting all assessments for a baby."""
        a1 = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_factors=[]
        )
        a2 = RiskAssessment(
            assessment_id="A002",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_factors=[]
        )
        a3 = RiskAssessment(
            assessment_id="A003",
            baby_id="B002",
            assessment_date=datetime.now(),
            risk_factors=[]
        )
        self.dm.add_assessment(a1)
        self.dm.add_assessment(a2)
        self.dm.add_assessment(a3)
        
        assessments = self.dm.get_assessments_for_baby("B001")
        self.assertEqual(len(assessments), 2)
    
    def test_get_babies_by_risk_level(self):
        """Test getting babies filtered by risk level."""
        # Add babies
        b1 = Baby(
            id="B001",
            first_name="Low",
            last_name="Risk",
            date_of_birth=datetime(2024, 1, 1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number="MRN001"
        )
        b2 = Baby(
            id="B002",
            first_name="High",
            last_name="Risk",
            date_of_birth=datetime(2024, 1, 1),
            gestational_age_weeks=32.0,
            birth_weight_grams=1800,
            medical_record_number="MRN002"
        )
        self.dm.add_baby(b1)
        self.dm.add_baby(b2)
        
        # Add assessments with different risk levels
        a1 = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_score=20.0,
            overall_risk_level=RiskLevel.LOW
        )
        a2 = RiskAssessment(
            assessment_id="A002",
            baby_id="B002",
            assessment_date=datetime.now(),
            risk_score=60.0,
            overall_risk_level=RiskLevel.HIGH
        )
        self.dm.add_assessment(a1)
        self.dm.add_assessment(a2)
        
        low_risk_babies = self.dm.get_babies_by_risk_level(RiskLevel.LOW)
        high_risk_babies = self.dm.get_babies_by_risk_level(RiskLevel.HIGH)
        
        self.assertEqual(len(low_risk_babies), 1)
        self.assertEqual(len(high_risk_babies), 1)
        self.assertEqual(low_risk_babies[0].id, "B001")
        self.assertEqual(high_risk_babies[0].id, "B002")
    
    def test_get_statistics(self):
        """Test statistics generation."""
        # Add some test data
        baby = Baby(
            id="B001",
            first_name="Test",
            last_name="Baby",
            date_of_birth=datetime(2024, 1, 1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number="MRN001"
        )
        self.dm.add_baby(baby)
        
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime.now(),
            risk_score=30.0,
            overall_risk_level=RiskLevel.MODERATE
        )
        self.dm.add_assessment(assessment)
        
        cert = RiskCertification(
            certification_id="C001",
            baby_id="B001",
            assessment_id="A001",
            certification_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=30),
            status=CertificationStatus.CERTIFIED
        )
        self.dm.add_certification(cert)
        
        stats = self.dm.get_statistics()
        self.assertEqual(stats['total_babies'], 1)
        self.assertEqual(stats['total_assessments'], 1)
        self.assertEqual(stats['total_certifications'], 1)
        self.assertEqual(stats['valid_certifications'], 1)
    
    def test_save_and_load_json(self):
        """Test saving and loading data from JSON."""
        # Add test data
        baby = Baby(
            id="B001",
            first_name="Test",
            last_name="Baby",
            date_of_birth=datetime(2024, 1, 1),
            gestational_age_weeks=38.0,
            birth_weight_grams=3000,
            medical_record_number="MRN001"
        )
        self.dm.add_baby(baby)
        
        rf = RiskFactor(
            factor_name="Test Factor",
            severity=5.0,
            description="Test",
            identified_date=datetime(2024, 1, 1)
        )
        assessment = RiskAssessment(
            assessment_id="A001",
            baby_id="B001",
            assessment_date=datetime(2024, 1, 1),
            risk_factors=[rf]
        )
        self.dm.add_assessment(assessment)
        
        # Save to JSON
        self.dm.save_to_json("test_data.json")
        
        # Create new manager and load
        dm2 = DataManager(data_directory=self.temp_dir)
        dm2.load_from_json("test_data.json")
        
        # Verify data was loaded correctly
        loaded_baby = dm2.get_baby("B001")
        self.assertIsNotNone(loaded_baby)
        self.assertEqual(loaded_baby.first_name, "Test")
        
        loaded_assessment = dm2.get_assessment("A001")
        self.assertIsNotNone(loaded_assessment)
        self.assertEqual(len(loaded_assessment.risk_factors), 1)


if __name__ == "__main__":
    unittest.main()
