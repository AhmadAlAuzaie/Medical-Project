"""
Data management system for Baby Risk Certification.

This module handles storage, retrieval, and management of baby risk
certification data in a retrospective data collection system.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from models import Baby, RiskAssessment, RiskCertification, RiskFactor, RiskLevel, CertificationStatus


class DataManager:
    """
    Manages persistence and retrieval of baby risk certification data.
    
    This class handles loading and saving data to JSON files for
    retrospective data analysis.
    """
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize the data manager.
        
        Args:
            data_directory: Directory where data files will be stored
        """
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(exist_ok=True)
        
        self.babies: Dict[str, Baby] = {}
        self.assessments: Dict[str, RiskAssessment] = {}
        self.certifications: Dict[str, RiskCertification] = {}
    
    def add_baby(self, baby: Baby) -> None:
        """
        Add a baby to the system.
        
        Args:
            baby: Baby object to add
        """
        self.babies[baby.id] = baby
    
    def add_assessment(self, assessment: RiskAssessment) -> None:
        """
        Add a risk assessment to the system.
        
        Args:
            assessment: RiskAssessment object to add
        """
        # Calculate risk score and level
        assessment.calculate_risk_score()
        assessment.determine_risk_level()
        self.assessments[assessment.assessment_id] = assessment
    
    def add_certification(self, certification: RiskCertification) -> None:
        """
        Add a risk certification to the system.
        
        Args:
            certification: RiskCertification object to add
        """
        # Check expiration before adding
        certification.check_expiration()
        self.certifications[certification.certification_id] = certification
    
    def get_baby(self, baby_id: str) -> Optional[Baby]:
        """
        Retrieve a baby by ID.
        
        Args:
            baby_id: ID of the baby to retrieve
            
        Returns:
            Baby object if found, None otherwise
        """
        return self.babies.get(baby_id)
    
    def get_assessment(self, assessment_id: str) -> Optional[RiskAssessment]:
        """
        Retrieve a risk assessment by ID.
        
        Args:
            assessment_id: ID of the assessment to retrieve
            
        Returns:
            RiskAssessment object if found, None otherwise
        """
        return self.assessments.get(assessment_id)
    
    def get_certification(self, certification_id: str) -> Optional[RiskCertification]:
        """
        Retrieve a certification by ID.
        
        Args:
            certification_id: ID of the certification to retrieve
            
        Returns:
            RiskCertification object if found, None otherwise
        """
        return self.certifications.get(certification_id)
    
    def get_assessments_for_baby(self, baby_id: str) -> List[RiskAssessment]:
        """
        Get all risk assessments for a specific baby.
        
        Args:
            baby_id: ID of the baby
            
        Returns:
            List of RiskAssessment objects for the baby
        """
        return [
            assessment for assessment in self.assessments.values()
            if assessment.baby_id == baby_id
        ]
    
    def get_certifications_for_baby(self, baby_id: str) -> List[RiskCertification]:
        """
        Get all certifications for a specific baby.
        
        Args:
            baby_id: ID of the baby
            
        Returns:
            List of RiskCertification objects for the baby
        """
        return [
            cert for cert in self.certifications.values()
            if cert.baby_id == baby_id
        ]
    
    def get_babies_by_risk_level(self, risk_level: RiskLevel) -> List[Baby]:
        """
        Get all babies with a specific risk level in their most recent assessment.
        
        Args:
            risk_level: Risk level to filter by
            
        Returns:
            List of Baby objects matching the risk level
        """
        babies_with_risk = []
        
        for baby in self.babies.values():
            assessments = self.get_assessments_for_baby(baby.id)
            if assessments:
                # Get most recent assessment
                latest_assessment = max(assessments, key=lambda a: a.assessment_date)
                if latest_assessment.overall_risk_level == risk_level:
                    babies_with_risk.append(baby)
        
        return babies_with_risk
    
    def get_statistics(self) -> Dict:
        """
        Generate statistics about the data in the system.
        
        Returns:
            Dictionary containing various statistics
        """
        stats = {
            "total_babies": len(self.babies),
            "total_assessments": len(self.assessments),
            "total_certifications": len(self.certifications),
            "risk_level_distribution": {
                "low": len(self.get_babies_by_risk_level(RiskLevel.LOW)),
                "moderate": len(self.get_babies_by_risk_level(RiskLevel.MODERATE)),
                "high": len(self.get_babies_by_risk_level(RiskLevel.HIGH)),
                "critical": len(self.get_babies_by_risk_level(RiskLevel.CRITICAL))
            },
            "valid_certifications": sum(
                1 for cert in self.certifications.values() if cert.is_valid()
            )
        }
        
        return stats
    
    def _serialize_datetime(self, obj):
        """Helper to serialize datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj
    
    def save_to_json(self, filename: str = "risk_certification_data.json") -> None:
        """
        Save all data to a JSON file.
        
        Args:
            filename: Name of the file to save to
        """
        filepath = self.data_directory / filename
        
        data = {
            "babies": [
                {
                    "id": b.id,
                    "first_name": b.first_name,
                    "last_name": b.last_name,
                    "date_of_birth": b.date_of_birth.isoformat(),
                    "gestational_age_weeks": b.gestational_age_weeks,
                    "birth_weight_grams": b.birth_weight_grams,
                    "medical_record_number": b.medical_record_number
                }
                for b in self.babies.values()
            ],
            "assessments": [
                {
                    "assessment_id": a.assessment_id,
                    "baby_id": a.baby_id,
                    "assessment_date": a.assessment_date.isoformat(),
                    "risk_factors": [
                        {
                            "factor_name": rf.factor_name,
                            "severity": rf.severity,
                            "description": rf.description,
                            "identified_date": rf.identified_date.isoformat()
                        }
                        for rf in a.risk_factors
                    ],
                    "overall_risk_level": a.overall_risk_level.value,
                    "risk_score": a.risk_score,
                    "notes": a.notes,
                    "assessed_by": a.assessed_by
                }
                for a in self.assessments.values()
            ],
            "certifications": [
                {
                    "certification_id": c.certification_id,
                    "baby_id": c.baby_id,
                    "assessment_id": c.assessment_id,
                    "certification_date": c.certification_date.isoformat(),
                    "valid_until": c.valid_until.isoformat(),
                    "status": c.status.value,
                    "certified_by": c.certified_by,
                    "recommendations": c.recommendations
                }
                for c in self.certifications.values()
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_json(self, filename: str = "risk_certification_data.json") -> None:
        """
        Load data from a JSON file.
        
        Args:
            filename: Name of the file to load from
        """
        filepath = self.data_directory / filename
        
        if not filepath.exists():
            return
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load babies
        for baby_data in data.get("babies", []):
            baby = Baby(
                id=baby_data["id"],
                first_name=baby_data["first_name"],
                last_name=baby_data["last_name"],
                date_of_birth=datetime.fromisoformat(baby_data["date_of_birth"]),
                gestational_age_weeks=baby_data["gestational_age_weeks"],
                birth_weight_grams=baby_data["birth_weight_grams"],
                medical_record_number=baby_data["medical_record_number"]
            )
            self.add_baby(baby)
        
        # Load assessments
        for assessment_data in data.get("assessments", []):
            risk_factors = [
                RiskFactor(
                    factor_name=rf["factor_name"],
                    severity=rf["severity"],
                    description=rf["description"],
                    identified_date=datetime.fromisoformat(rf["identified_date"])
                )
                for rf in assessment_data["risk_factors"]
            ]
            
            assessment = RiskAssessment(
                assessment_id=assessment_data["assessment_id"],
                baby_id=assessment_data["baby_id"],
                assessment_date=datetime.fromisoformat(assessment_data["assessment_date"]),
                risk_factors=risk_factors,
                overall_risk_level=RiskLevel(assessment_data["overall_risk_level"]),
                risk_score=assessment_data["risk_score"],
                notes=assessment_data["notes"],
                assessed_by=assessment_data["assessed_by"]
            )
            self.add_assessment(assessment)
        
        # Load certifications
        for cert_data in data.get("certifications", []):
            certification = RiskCertification(
                certification_id=cert_data["certification_id"],
                baby_id=cert_data["baby_id"],
                assessment_id=cert_data["assessment_id"],
                certification_date=datetime.fromisoformat(cert_data["certification_date"]),
                valid_until=datetime.fromisoformat(cert_data["valid_until"]),
                status=CertificationStatus(cert_data["status"]),
                certified_by=cert_data["certified_by"],
                recommendations=cert_data["recommendations"]
            )
            self.add_certification(certification)
