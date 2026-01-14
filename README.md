# Medical-Project: Baby Risk Certification System

A comprehensive system for managing retrospective data on risk certification for babies. This system enables healthcare professionals to record, assess, and certify risk levels for newborns based on clinical data.

## Features

- **Baby Registration**: Record essential birth information including gestational age, birth weight, and medical record numbers
- **Risk Assessment**: Document clinical assessments including APGAR scores, respiratory status, infections, and intensive care requirements
- **Automated Risk Scoring**: Calculate risk scores (0-100) based on multiple clinical factors
- **Risk Level Classification**: Automatically classify babies into risk categories (Low, Moderate, High, Critical)
- **Certification Management**: Issue and track risk certifications with healthcare professional attribution
- **Data Persistence**: SQLite database for reliable data storage and retrieval
- **Comprehensive Testing**: Full test suite covering models, calculations, database operations, and integration

## Project Structure

```
Medical-Project/
├── src/
│   ├── models/              # Data models for babies, assessments, and certifications
│   ├── database/            # Database schema and management
│   ├── utils/               # Risk calculation utilities
│   └── baby_risk_system.py  # Main system orchestration
├── tests/                   # Comprehensive test suite
├── data/                    # Sample data and utilities
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AhmadAlAuzaie/Medical-Project.git
cd Medical-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from datetime import datetime
from src.baby_risk_system import BabyRiskCertificationSystem

# Initialize the system
system = BabyRiskCertificationSystem()

# Register a baby
baby_id = system.register_baby(
    name="Emma Johnson",
    date_of_birth=datetime(2025, 6, 15),
    gestational_age_weeks=39.5,
    birth_weight_grams=3400,
    medical_record_number="MRN001234"
)

# Record a risk assessment
assessment_id = system.record_assessment(
    baby_id=baby_id,
    assessment_date=datetime(2025, 6, 15),
    apgar_score_1min=9,
    apgar_score_5min=10,
    has_respiratory_issues=False,
    has_infection=False,
    requires_intensive_care=False,
    additional_notes="Normal delivery, no complications"
)

# Create risk certification (automatically calculates risk)
cert_id = system.certify_risk(
    baby_id=baby_id,
    assessment_id=assessment_id,
    certified_by="Dr. Sarah Smith",
    notes="Low risk, cleared for standard post-natal care"
)

# Retrieve certifications
certifications = system.get_baby_certifications(baby_id)
for cert in certifications:
    print(f"Risk Level: {cert.risk_level.value}")
    print(f"Risk Score: {cert.risk_score}/100")
```

### Creating Sample Data

Run the sample data script to populate the database with example cases:

```bash
python data/create_sample_data.py
```

This creates four sample babies representing different risk levels:
- **Low Risk**: Full-term baby with normal birth weight and excellent APGAR scores
- **Moderate Risk**: Premature baby with respiratory issues
- **High Risk**: Very premature baby requiring NICU care
- **Critical Risk**: Extremely premature baby with multiple complications

## Risk Scoring Algorithm

The system calculates risk scores based on the following factors:

### Gestational Age (0-20 points)
- < 28 weeks: 20 points (Extremely premature)
- 28-32 weeks: 15 points (Very premature)
- 32-37 weeks: 10 points (Premature)
- ≥ 37 weeks: 0 points (Term)

### Birth Weight (0-20 points)
- < 1000g: 20 points (Extremely low)
- 1000-1500g: 15 points (Very low)
- 1500-2500g: 10 points (Low)
- ≥ 2500g: 0 points (Normal)

### APGAR Score at 1 Minute (0-15 points)
- 0-3: 15 points (Critically low)
- 4-6: 10 points (Low)
- 7-10: 0 points (Normal)

### APGAR Score at 5 Minutes (0-15 points)
- 0-6: 15 points (Low - persistent problems)
- 7-8: 5 points (Slightly low)
- 9-10: 0 points (Normal)

### Clinical Conditions (0-30 points)
- Requires intensive care: 15 points
- Has respiratory issues: 10 points
- Has infection: 5 points

### Risk Level Classification
- **Low**: Score < 25
- **Moderate**: Score 25-49
- **High**: Score 50-74
- **Critical**: Score ≥ 75

## Testing

Run the test suite to verify the system:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_risk_calculator.py

# Run with coverage report
pytest --cov=src tests/
```

## Data Models

### Baby
- ID, name, date of birth
- Gestational age (weeks)
- Birth weight (grams)
- Medical record number

### Risk Assessment
- Baby ID (foreign key)
- Assessment date
- APGAR scores (1 min, 5 min)
- Clinical conditions (respiratory, infection, ICU)
- Additional notes

### Risk Certification
- Baby ID, Assessment ID (foreign keys)
- Risk level (Low/Moderate/High/Critical)
- Risk score (0-100)
- Certification status
- Certified by (healthcare professional)
- Certification date and notes

## Database Schema

The system uses SQLite with three main tables:
- `babies`: Stores baby birth information
- `risk_assessments`: Records clinical assessments
- `risk_certifications`: Tracks risk certifications

See `src/database/schema.py` for the complete schema definition.

## Contributing

This is a medical data management system. When contributing:
1. Maintain data validation and integrity
2. Follow existing code structure and patterns
3. Add tests for new functionality
4. Update documentation as needed
5. Never commit actual patient data

## License

This project is for educational and demonstration purposes.

## Disclaimer

This system is for retrospective data management and educational purposes only. It should not be used as the sole basis for medical decisions without proper clinical oversight and validation.
