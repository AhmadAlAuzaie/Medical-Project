"""
Database manager for the Baby Risk Certification System.

This module handles all database operations including CRUD operations
for babies, risk assessments, and risk certifications.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from ..models.baby_risk_models import (
    Baby, RiskAssessment, RiskCertification,
    RiskLevel, CertificationStatus
)
from .schema import SCHEMA_SQL


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str = "baby_risk_certification.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
    
    def add_baby(self, baby: Baby) -> int:
        """
        Add a new baby to the database.
        
        Args:
            baby: Baby object to add
            
        Returns:
            ID of the newly created baby record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO babies (name, date_of_birth, gestational_age_weeks, 
                                   birth_weight_grams, medical_record_number)
                VALUES (?, ?, ?, ?, ?)
            """, (
                baby.name,
                baby.date_of_birth.isoformat(),
                baby.gestational_age_weeks,
                baby.birth_weight_grams,
                baby.medical_record_number
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_baby(self, baby_id: int) -> Optional[Baby]:
        """
        Retrieve a baby by ID.
        
        Args:
            baby_id: ID of the baby to retrieve
            
        Returns:
            Baby object or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM babies WHERE id = ?", (baby_id,))
            row = cursor.fetchone()
            
            if row:
                return Baby(
                    id=row[0],
                    name=row[1],
                    date_of_birth=datetime.fromisoformat(row[2]),
                    gestational_age_weeks=row[3],
                    birth_weight_grams=row[4],
                    medical_record_number=row[5]
                )
            return None
    
    def add_risk_assessment(self, assessment: RiskAssessment) -> int:
        """
        Add a new risk assessment to the database.
        
        Args:
            assessment: RiskAssessment object to add
            
        Returns:
            ID of the newly created assessment record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO risk_assessments (baby_id, assessment_date, apgar_score_1min,
                                             apgar_score_5min, has_respiratory_issues,
                                             has_infection, requires_intensive_care,
                                             additional_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.baby_id,
                assessment.assessment_date.isoformat(),
                assessment.apgar_score_1min,
                assessment.apgar_score_5min,
                assessment.has_respiratory_issues,
                assessment.has_infection,
                assessment.requires_intensive_care,
                assessment.additional_notes
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_risk_assessment(self, assessment_id: int) -> Optional[RiskAssessment]:
        """
        Retrieve a risk assessment by ID.
        
        Args:
            assessment_id: ID of the assessment to retrieve
            
        Returns:
            RiskAssessment object or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM risk_assessments WHERE id = ?", (assessment_id,))
            row = cursor.fetchone()
            
            if row:
                return RiskAssessment(
                    id=row[0],
                    baby_id=row[1],
                    assessment_date=datetime.fromisoformat(row[2]),
                    apgar_score_1min=row[3],
                    apgar_score_5min=row[4],
                    has_respiratory_issues=bool(row[5]),
                    has_infection=bool(row[6]),
                    requires_intensive_care=bool(row[7]),
                    additional_notes=row[8]
                )
            return None
    
    def add_risk_certification(self, certification: RiskCertification) -> int:
        """
        Add a new risk certification to the database.
        
        Args:
            certification: RiskCertification object to add
            
        Returns:
            ID of the newly created certification record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO risk_certifications (baby_id, assessment_id, risk_level,
                                                risk_score, certification_status,
                                                certification_date, certified_by, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                certification.baby_id,
                certification.assessment_id,
                certification.risk_level.value,
                certification.risk_score,
                certification.certification_status.value,
                certification.certification_date.isoformat(),
                certification.certified_by,
                certification.notes
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_risk_certification(self, certification_id: int) -> Optional[RiskCertification]:
        """
        Retrieve a risk certification by ID.
        
        Args:
            certification_id: ID of the certification to retrieve
            
        Returns:
            RiskCertification object or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM risk_certifications WHERE id = ?", (certification_id,))
            row = cursor.fetchone()
            
            if row:
                return RiskCertification(
                    id=row[0],
                    baby_id=row[1],
                    assessment_id=row[2],
                    risk_level=RiskLevel(row[3]),
                    risk_score=row[4],
                    certification_status=CertificationStatus(row[5]),
                    certification_date=datetime.fromisoformat(row[6]),
                    certified_by=row[7],
                    notes=row[8]
                )
            return None
    
    def get_certifications_by_baby(self, baby_id: int) -> List[RiskCertification]:
        """
        Retrieve all certifications for a specific baby.
        
        Args:
            baby_id: ID of the baby
            
        Returns:
            List of RiskCertification objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM risk_certifications 
                WHERE baby_id = ? 
                ORDER BY certification_date DESC
            """, (baby_id,))
            rows = cursor.fetchall()
            
            certifications = []
            for row in rows:
                certifications.append(RiskCertification(
                    id=row[0],
                    baby_id=row[1],
                    assessment_id=row[2],
                    risk_level=RiskLevel(row[3]),
                    risk_score=row[4],
                    certification_status=CertificationStatus(row[5]),
                    certification_date=datetime.fromisoformat(row[6]),
                    certified_by=row[7],
                    notes=row[8]
                ))
            return certifications
    
    def get_all_babies(self) -> List[Baby]:
        """
        Retrieve all babies from the database.
        
        Returns:
            List of Baby objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM babies ORDER BY date_of_birth DESC")
            rows = cursor.fetchall()
            
            babies = []
            for row in rows:
                babies.append(Baby(
                    id=row[0],
                    name=row[1],
                    date_of_birth=datetime.fromisoformat(row[2]),
                    gestational_age_weeks=row[3],
                    birth_weight_grams=row[4],
                    medical_record_number=row[5]
                ))
            return babies
