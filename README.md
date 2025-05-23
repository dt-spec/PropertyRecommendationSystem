# Property Recommendation System

A machine learning-based system that recommends the top 3 most comparable properties for a given subject property. The system analyzes property features and provides explanations for its recommendations.

## Features

- Recommends top 3 comparable properties based on property features
- Provides human-readable explanations for each recommendation
- Evaluates recommendations using Precision@3 metric
- Handles missing data and various data formats
- Includes a demo script for quick testing

## Project Structure

```
.
├── data/                   # Dataset directory
│   ├── val_processed.json  # Validation dataset
│   └── train_processed.json # Training dataset
├── src/                    # Source code
│   ├── recommender.py      # Recommendation logic
│   ├── evaluator.py        # Evaluation metrics
│   └── explainability.py   # Explanation generation
├── main.py                 # Main script
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd PropertyRecommendationSystem
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Script
```bash
python main.py
```
This will evaluate the recommendation system on the validation dataset and show the average Precision@3 score.

### Running the Demo
```bash
python demo.py
```
This will demonstrate the recommendation system on a single appraisal from the validation dataset.

## How It Works

1. **Feature Extraction**: The system extracts key features from properties:
   - Gross Living Area (GLA)
   - Lot Size
   - Number of Bedrooms
   - Number of Bathrooms
   - Year Built

2. **Recommendation**: Uses Euclidean distance to find the most similar properties based on these features.

3. **Explanation**: Provides human-readable explanations for each recommendation, such as:
   - Similar GLA
   - Close lot size
   - Same number of bedrooms
   - Similar number of bathrooms
   - Similar year built
   - Recent sale date

## Requirements

- Python 3.6+
- numpy
- scikit-learn 