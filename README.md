# Medical Project: Retrospective Data on Risk Certification for Babies

A comprehensive system for managing and analyzing retrospective data on risk certification for newborn babies. This system helps healthcare providers track, assess, and certify risk levels for babies based on various medical factors.

## Overview

This project provides a complete solution for:
- Recording baby information and medical history
- Conducting risk assessments based on multiple factors
- Calculating risk scores and levels automatically
- Issuing and managing risk certifications
- Analyzing retrospective data for research and quality improvement

## Features

### Core Functionality
- **Baby Registration**: Store comprehensive baby information including gestational age, birth weight, and medical record numbers
- **Risk Assessment**: Evaluate babies based on multiple risk factors with severity scoring
- **Automated Risk Calculation**: Automatically calculate overall risk scores (0-100) and risk levels (Low, Moderate, High, Critical)
- **Risk Certification**: Issue official certifications with recommendations and validity periods
- **Data Management**: Load and save data in JSON format for retrospective analysis
- **Statistics & Reporting**: Generate statistics on risk distributions and certification status

### Data Models

#### Baby
- Unique identifier
- Personal information (name, date of birth)
- Medical data (gestational age, birth weight)
- Medical record number

#### Risk Assessment
- Multiple risk factors with individual severity scores (0-10)
- Overall risk score (0-100)
- Risk level classification (Low/Moderate/High/Critical)
- Assessment metadata (date, assessor, notes)

#### Risk Certification
- Links to baby and assessment
- Certification validity period
- Status tracking (Pending, Certified, Requires Review, Expired)
- Medical recommendations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

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

### Running the Demo

The main script demonstrates all system capabilities:

```bash
python main.py
```

This will:
1. Load sample data from `data/sample_data.json`
2. Display system statistics
3. Show individual baby records with assessments and certifications
4. Add a new baby with risk assessment
5. Generate and save updated data
6. Display babies grouped by risk level

### Using the System Programmatically

```python
from datetime import datetime, timedelta
from models import Baby, RiskAssessment, RiskFactor, RiskCertification
from data_manager import DataManager

# Initialize data manager
dm = DataManager()

# Create a new baby
baby = Baby(
    id="B001",
    first_name="Emma",
    last_name="Johnson",
    date_of_birth=datetime(2024, 3, 15, 8, 30),
    gestational_age_weeks=38.5,
    birth_weight_grams=3200,
    medical_record_number="MRN001234"
)
dm.add_baby(baby)

# Create risk factors
risk_factors = [
    RiskFactor(
        factor_name="Mild Jaundice",
        severity=3.0,
        description="Mild jaundice detected",
        identified_date=datetime.now()
    )
]

# Create risk assessment
assessment = RiskAssessment(
    assessment_id="A001",
    baby_id="B001",
    assessment_date=datetime.now(),
    risk_factors=risk_factors,
    assessed_by="Dr. Sarah Chen"
)
dm.add_assessment(assessment)

# Create certification
certification = RiskCertification(
    certification_id="C001",
    baby_id="B001",
    assessment_id="A001",
    certification_date=datetime.now(),
    valid_until=datetime.now() + timedelta(days=90),
    certified_by="Dr. Sarah Chen",
    recommendations=["Monitor jaundice daily", "Follow-up in 2 weeks"]
)
dm.add_certification(certification)

# Save all data
dm.save_to_json("risk_certification_data.json")

# Get statistics
stats = dm.get_statistics()
print(f"Total babies: {stats['total_babies']}")
```

## Data Structure

### Sample Data Format

The system uses JSON for data storage. See `data/sample_data.json` for examples.

```json
{
  "babies": [
    {
      "id": "B001",
      "first_name": "Emma",
      "last_name": "Johnson",
      "date_of_birth": "2024-03-15T08:30:00",
      "gestational_age_weeks": 38.5,
      "birth_weight_grams": 3200,
      "medical_record_number": "MRN001234"
    }
  ],
  "assessments": [...],
  "certifications": [...]
}
```

## Risk Scoring System

### Risk Levels
- **Low (0-24)**: Minimal risk factors, standard care recommended
- **Moderate (25-49)**: Some risk factors present, enhanced monitoring
- **High (50-74)**: Significant risk factors, intensive monitoring required
- **Critical (75-100)**: Severe risk factors, immediate intervention needed

### Risk Score Calculation
The overall risk score is calculated as:
1. Each risk factor has a severity score (0-10)
2. Average severity across all factors is calculated
3. Score is normalized to 0-100 scale
4. Risk level is determined based on score thresholds

## Project Structure

```
Medical-Project/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── models.py                # Data models (Baby, RiskAssessment, etc.)
├── data_manager.py          # Data management and persistence
├── main.py                  # Demo script
└── data/
    ├── sample_data.json     # Sample data for testing
    └── risk_certification_data.json  # Generated data file
```

## Use Cases

### Retrospective Data Analysis
- Import historical baby records for analysis
- Identify patterns in risk factors
- Evaluate outcomes based on risk levels
- Generate reports for quality improvement

### Clinical Decision Support
- Standardize risk assessment procedures
- Provide consistent risk scoring
- Track certification validity
- Generate evidence-based recommendations

### Research Applications
- Collect structured retrospective data
- Analyze risk factor correlations
- Study outcomes across risk levels
- Support epidemiological studies

## Data Validation

The system includes built-in validation:
- Gestational age must be between 20-44 weeks
- Birth weight must be between 300-6000 grams
- Risk factor severity must be between 0-10
- All dates are validated for proper format

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available for medical and research purposes.

## Contact

For questions or support, please contact the repository maintainer.

## Disclaimer

This system is intended for retrospective data collection and analysis. It should not be used as the sole basis for clinical decision-making without proper medical oversight and validation.
