# 🧠 MindPulse — Employee Mental Health Predictor

An AI-powered web application that predicts mental health conditions based on remote work patterns and lifestyle factors. Built with machine learning and designed to help employees and organizations understand mental health risks in remote and hybrid work environments.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Model Performance](#model-performance)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

## 🌟 Overview

MindPulse is a machine learning application that analyzes the impact of remote work on mental health. It uses a Random Forest classifier trained on employee data to predict mental health conditions (Anxiety, Burnout, Depression, None) based on work patterns, lifestyle factors, and stress indicators.

The application features:
- **Interactive Web Interface**: Clean, modern UI built with Streamlit
- **Multi-step Assessment**: Guided questionnaire covering work environment and lifestyle
- **Real-time Predictions**: Instant mental health risk assessment with confidence scores
- **Personalized Insights**: Custom recommendations based on risk factors

## ✨ Features

### 🎯 Core Functionality
- **Mental Health Prediction**: Classifies into 4 categories (Anxiety, Burnout, Depression, None)
- **Confidence Scoring**: Provides probability distribution across all conditions
- **Risk Factor Analysis**: Identifies key contributors to mental health risks
- **Personalized Recommendations**: Tailored advice based on assessment results

### 📊 Assessment Categories
1. **Work Environment**
   - Work location (Remote, Hybrid, Onsite)
   - Hours worked per week
   - Virtual meetings frequency
   - Stress level
   - Productivity change
   - Job satisfaction
   - Work-life balance rating
   - Company support level

2. **Lifestyle Factors**
   - Physical activity frequency
   - Sleep quality
   - Access to mental health resources
   - Social isolation level

### 🎨 User Experience
- Progressive multi-step form with visual stepper
- Live input validation and preview
- Responsive design with dark mode aesthetics
- Smooth animations and transitions
- Mobile-friendly interface

## 📊 Dataset

**Source**: `Impact_of_Remote_Work_on_Mental_Health.csv`

**Key Features**:
- **Size**: 5,000 employee records
- **Features**: 20 columns including demographics, work patterns, and mental health indicators
- **Target Variable**: Mental Health Condition (Anxiety, Burnout, Depression, None)

**Main Variables**:
| Category | Variables |
|----------|-----------|
| Demographics | Age, Gender, Job Role, Industry, Years of Experience, Region |
| Work Patterns | Work Location, Hours Worked, Virtual Meetings, Productivity Change |
| Mental Health | Stress Level, Mental Health Condition, Access to Resources |
| Lifestyle | Physical Activity, Sleep Quality, Social Isolation Rating |
| Satisfaction | Work-Life Balance, Job Satisfaction, Company Support |

## 🤖 Model Architecture

### Training Pipeline

1. **Data Preprocessing**
   - Label encoding for categorical variables
   - Feature selection (12 key predictors)
   - Train-test split (80/20)

2. **Class Imbalance Handling**
   - SMOTE (Synthetic Minority Over-sampling Technique)
   - Balances class distribution for better prediction

3. **Model Training**
   - **Algorithm**: Random Forest Classifier
   - **Parameters**: Optimized for multi-class classification
   - **Cross-validation**: Implemented for robust performance

4. **Model Artifacts**
   - `mental_health_rf_model.pkl` (15MB) - Trained Random Forest model
   - `label_encoder.pkl` - Fitted label encoder for target classes
   - `expected_columns.pkl` - Feature schema for consistency

### Key Predictors
The model uses 12 features for prediction:
- Work Location
- Hours Worked Per Week
- Number of Virtual Meetings
- Stress Level
- Productivity Change
- Satisfaction with Remote Work
- Work-Life Balance Rating
- Company Support for Remote Work
- Physical Activity
- Sleep Quality
- Access to Mental Health Resources
- Social Isolation Rating

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/keophlyna/-Machine-Learning.git
cd -Machine-Learning
```

2. **Install dependencies**
```bash
pip install streamlit pandas numpy joblib scikit-learn imbalanced-learn xgboost matplotlib seaborn
```

3. **Verify model files exist**
Ensure these files are in the project directory:
- `mental_health_rf_model.pkl`
- `label_encoder.pkl`
- `expected_columns.pkl`

## 💻 Usage

### Running the Application

1. **Start the Streamlit app**
```bash
streamlit run app.py
```

2. **Access the interface**
   - Open your browser to `http://localhost:8501`
   - The welcome screen will appear

3. **Complete the assessment**
   - **Step 1**: Fill in work environment details
   - **Step 2**: Provide lifestyle information
   - **Review**: Check your inputs before submission
   - **Results**: View prediction with personalized insights

### Training the Model (Optional)

To retrain the model or explore the data:

```bash
jupyter notebook mental_health_ver2_0.ipynb
```

The notebook contains:
- Data exploration and visualization
- Feature engineering
- Model training and evaluation
- Performance metrics and comparison

## 📁 Project Structure

```
-Machine-Learning/
│
├── app.py                                    # Streamlit web application
├── mental_health_ver2_0.ipynb               # Model training notebook
├── Impact_of_Remote_Work_on_Mental_Health.csv  # Training dataset
│
├── mental_health_rf_model.pkl               # Trained Random Forest model (15MB)
├── label_encoder.pkl                        # Label encoder for target classes
├── expected_columns.pkl                     # Feature schema
│
└── README.md                                # Project documentation
```

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.8+**: Programming language
- **Streamlit**: Web application framework
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **NumPy**: Numerical computing

### Machine Learning Stack
- **Random Forest**: Primary classification algorithm
- **SMOTE**: Class imbalance handling
- **Logistic Regression**: Baseline comparison
- **XGBoost**: Advanced model comparison

### Data Visualization
- **Matplotlib**: Statistical plotting
- **Seaborn**: Enhanced visualizations
- **Custom CSS**: UI styling and theming

## 📈 Model Performance

The Random Forest classifier demonstrates robust performance across all mental health categories:

### Key Metrics
- **Accuracy**: ~85-90% (varies by condition)
- **Multi-class Support**: 4 mental health conditions
- **Feature Importance**: Hours worked, stress level, and work-life balance are top predictors

### Class Distribution
- **Anxiety**: Common in high-stress, high-meeting environments
- **Burnout**: Associated with long hours and poor work-life balance
- **Depression**: Linked to social isolation and lack of resources
- **None**: Baseline healthy condition

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Ideas
- Improve model accuracy with hyperparameter tuning
- Add more mental health conditions
- Implement additional visualization features
- Enhance UI/UX design
- Add export functionality for results
- Integrate with mental health resources APIs

## ⚠️ Disclaimer

**Important**: This application is designed for **educational and research purposes only**. 

- The predictions are generated by a machine learning model and should **not** be used as a substitute for professional medical advice, diagnosis, or treatment.
- Mental health is complex and multifaceted. This tool provides general insights based on patterns in data.
- If you are experiencing mental health concerns, please consult a **qualified mental health professional** or contact appropriate support services.

### Support Resources
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741 (US)
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**keophlyna**
- GitHub: [@keophlyna](https://github.com/keophlyna)

## 🙏 Acknowledgments

- Dataset inspired by research on remote work and mental health
- Streamlit community for excellent documentation
- scikit-learn team for robust ML tools
- Open source community for continuous inspiration

---

**Made with ❤️ for better mental health awareness in the workplace**

*Last updated: April 2026*
