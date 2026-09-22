"""
Machine Learning Model Module - Phase 10 Implementation
AI Chatbot for University Support
Scikit-learn based intent classification using TF-IDF + Logistic Regression
"""

import os
import json
import pickle
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

# Model storage paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'ml_artifacts')
MODEL_PATH = os.path.join(MODEL_DIR, 'intent_classifier.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
METADATA_PATH = os.path.join(MODEL_DIR, 'model_metadata.json')
TRAINING_DATA_PATH = os.path.join(MODEL_DIR, 'training_data.json')

# Confidence threshold
CONFIDENCE_THRESHOLD = 0.25


# ==================== TRAINING DATA ====================

UNIVERSITY_TRAINING_DATA = [
    # Admissions
    ("What is the admission process?", "admissions"),
    ("How do I apply to IIUI?", "admissions"),
    ("What are the admission requirements?", "admissions"),
    ("When is the admission deadline?", "admissions"),
    ("What documents are needed for admission?", "admissions"),
    ("How can I enroll at IIUI?", "admissions"),
    ("What is the entry test for admission?", "admissions"),
    ("Tell me about admission criteria", "admissions"),
    ("What is the eligibility for admission?", "admissions"),
    ("How to get admission in IIUI?", "admissions"),
    ("Is there an entrance exam?", "admissions"),
    ("When does admission start?", "admissions"),
    ("What is the admission procedure?", "admissions"),
    ("Can I apply online for admission?", "admissions"),
    ("What are the admission dates?", "admissions"),

    # Course Registration
    ("How do I register for courses?", "course_registration"),
    ("What is the course registration process?", "course_registration"),
    ("When can I register for next semester?", "course_registration"),
    ("How to add a course?", "course_registration"),
    ("Can I drop a course after registration?", "course_registration"),
    ("What are credit hours?", "course_registration"),
    ("How many courses can I take?", "course_registration"),
    ("When is semester registration?", "course_registration"),
    ("I need to register for courses", "course_registration"),
    ("Course enrollment process", "course_registration"),
    ("How to enroll in courses?", "course_registration"),
    ("What is the last date for course registration?", "course_registration"),

    # Examinations
    ("When are the final exams?", "examinations"),
    ("What is the exam schedule?", "examinations"),
    ("When are midterm exams?", "examinations"),
    ("How is the grading system?", "examinations"),
    ("What is the GPA calculation?", "examinations"),
    ("When will results be announced?", "examinations"),
    ("What is the examination policy?", "examinations"),
    ("Where can I find exam dates?", "examinations"),
    ("How do I check my grades?", "examinations"),
    ("What are the exam rules?", "examinations"),
    ("When is the final examination?", "examinations"),
    ("Tell me about midterm schedule", "examinations"),
    ("What is the CGPA requirement?", "examinations"),
    ("How to get transcript?", "examinations"),

    # Fees
    ("What is the fee structure?", "fees"),
    ("How much is the tuition fee?", "fees"),
    ("What are the fees for BS Computer Science?", "fees"),
    ("When is the fee payment deadline?", "fees"),
    ("Can I pay fees in installments?", "fees"),
    ("What is the admission fee?", "fees"),
    ("Tell me about scholarship options", "fees"),
    ("Are there any financial aid programs?", "fees"),
    ("What is the fee refund policy?", "fees"),
    ("How to pay semester fee?", "fees"),
    ("What is the cost of the program?", "fees"),
    ("Is there a fee waiver available?", "fees"),
    ("How much does BBA cost?", "fees"),
    ("What are the payment methods?", "fees"),

    # Academic Policies
    ("What are the academic policies?", "academic_policies"),
    ("What is the attendance policy?", "academic_policies"),
    ("What are the university rules?", "academic_policies"),
    ("What is the grading policy?", "academic_policies"),
    ("What is the plagiarism policy?", "academic_policies"),
    ("What is the academic code of conduct?", "academic_policies"),
    ("What happens if I fail a course?", "academic_policies"),
    ("What are the disciplinary rules?", "academic_policies"),
    ("Tell me about academic integrity", "academic_policies"),
    ("What is the leave policy?", "academic_policies"),
    ("What are the promotion criteria?", "academic_policies"),
    ("How many courses can I fail?", "academic_policies"),

    # University Services
    ("What services does the university offer?", "university_services"),
    ("Is there a library on campus?", "university_services"),
    ("Tell me about hostel facilities", "university_services"),
    ("What sports facilities are available?", "university_services"),
    ("Is there free WiFi on campus?", "university_services"),
    ("What is the computer lab like?", "university_services"),
    ("Is there a health center?", "university_services"),
    ("What about career services?", "university_services"),
    ("Tell me about campus facilities", "university_services"),
    ("Is there transport service?", "university_services"),
    ("What medical facilities are available?", "university_services"),
    ("Are there counseling services?", "university_services"),

    # Courses
    ("What courses are offered?", "courses"),
    ("What programs does IIUI offer?", "courses"),
    ("Tell me about BS Computer Science", "courses"),
    ("What is the BSIT program?", "courses"),
    ("What departments are there?", "courses"),
    ("What are the available degrees?", "courses"),
    ("Tell me about the BBA program", "courses"),
    ("What engineering programs are offered?", "courses"),
    ("How many semesters in BS program?", "courses"),
    ("What is the course content for BS CS?", "courses"),
    ("Tell me about software engineering degree", "courses"),
    ("What faculties does IIUI have?", "courses"),

    # Schedules
    ("What is the class schedule?", "schedules"),
    ("When do classes start?", "schedules"),
    ("What are the office hours?", "schedules"),
    ("When is the academic calendar?", "schedules"),
    ("What are the semester dates?", "schedules"),
    ("When does the fall semester start?", "schedules"),
    ("What are the university timings?", "schedules"),
    ("When are holidays?", "schedules"),
    ("What is the summer schedule?", "schedules"),
    ("Tell me about the academic calendar", "schedules"),
    ("When does spring semester begin?", "schedules"),

    # Contact
    ("How can I contact the university?", "contact"),
    ("What is the university phone number?", "contact"),
    ("Where is IIUI located?", "contact"),
    ("What is the email for admissions office?", "contact"),
    ("Where is the admin office?", "contact"),
    ("How can I reach student affairs?", "contact"),
    ("What is the helpdesk number?", "contact"),
    ("Give me the university address", "contact"),
    ("Where is the registrar office?", "contact"),

    # FAQ
    ("Tell me about IIUI", "faq"),
    ("What is IIUI?", "faq"),
    ("About the university", "faq"),
    ("General information about IIUI", "faq"),
    ("What kind of university is IIUI?", "faq"),
    ("Overview of IIUI", "faq"),

    # Unknown / non-university
    ("Tell me a joke", "unknown"),
    ("What is the weather today?", "unknown"),
    ("Who won the football match?", "unknown"),
    ("xyzabc123", "unknown"),
    ("Hello", "unknown"),
    ("Hi there", "unknown"),
    ("Thanks", "unknown"),
    ("Good morning", "unknown"),
]


class MLClassifier:
    """Machine Learning intent classifier using TF-IDF + Logistic Regression."""

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metadata = {}
        self.is_trained = False
        os.makedirs(MODEL_DIR, exist_ok=True)
        self._load_model()

    def _load_model(self):
        """Load a previously trained model from disk."""
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                with open(VECTORIZER_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                if os.path.exists(METADATA_PATH):
                    with open(METADATA_PATH, 'r') as f:
                        self.metadata = json.load(f)
                self.is_trained = True
                logger.info(f"ML model loaded: {self.metadata.get('accuracy', 'unknown')} accuracy")
                return
        except Exception as e:
            logger.warning(f"Could not load ML model: {e}")

        # Train with default data if no model exists
        self.train(UNIVERSITY_TRAINING_DATA)

    def train(self, training_data=None):
        """Train the intent classification model.

        Args:
            training_data: List of (text, intent) tuples. Uses built-in data if None.
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            import numpy as np
        except ImportError as e:
            logger.error(f"Scikit-learn not available: {e}")
            return False

        if training_data is None:
            training_data = UNIVERSITY_TRAINING_DATA

        texts = [t[0] for t in training_data]
        labels = [t[1] for t in training_data]

        if len(texts) < 10:
            logger.warning("Not enough training data")
            return False

        # Feature extraction
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=1,
        )
        X = self.vectorizer.fit_transform(texts)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # Train model
        self.model = LogisticRegression(
            max_iter=1000,
            C=1.0,
            solver='lbfgs',
            multi_class='multinomial',
            random_state=42,
        )
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        try:
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        except Exception:
            precision = recall = f1 = accuracy

        self.metadata = {
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1, 4),
            'dataset_size': len(texts),
            'num_intents': len(set(labels)),
            'train_size': len(y_train),
            'test_size': len(y_test),
            'trained_at': datetime.now().isoformat(),
            'intents': sorted(set(labels)),
        }

        # Save model
        self._save_model()
        self.is_trained = True

        logger.info(f"Model trained: accuracy={accuracy:.4f}, f1={f1:.4f}")
        return True

    def _save_model(self):
        """Save the trained model and vectorizer to disk."""
        try:
            with open(MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            with open(VECTORIZER_PATH, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            with open(METADATA_PATH, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    def predict(self, text):
        """Predict the intent of a text query.

        Returns:
            dict with 'intent', 'confidence', and 'probabilities' (if available).
        """
        if not self.is_trained or not self.model or not self.vectorizer:
            return {'intent': 'unknown', 'confidence': 0.0}

        if not text or not text.strip():
            return {'intent': 'unknown', 'confidence': 0.0}

        try:
            X = self.vectorizer.transform([text])
            intent = self.model.predict(X)[0]

            # Get probability scores
            probs = self.model.predict_proba(X)[0]
            confidence = float(max(probs))

            # Apply threshold
            if confidence < CONFIDENCE_THRESHOLD:
                return {'intent': 'unknown', 'confidence': round(confidence, 3)}

            # Build probability dict
            prob_dict = {}
            for cls, prob in zip(self.model.classes_, probs):
                if prob > 0.05:
                    prob_dict[cls] = round(float(prob), 3)

            return {
                'intent': intent,
                'confidence': round(confidence, 3),
                'probabilities': prob_dict,
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'intent': 'unknown', 'confidence': 0.0}

    def get_status(self):
        """Get model status information."""
        return {
            'is_trained': self.is_trained,
            'accuracy': self.metadata.get('accuracy', 0),
            'precision': self.metadata.get('precision', 0),
            'recall': self.metadata.get('recall', 0),
            'f1_score': self.metadata.get('f1_score', 0),
            'dataset_size': self.metadata.get('dataset_size', 0),
            'num_intents': self.metadata.get('num_intents', 0),
            'intents': self.metadata.get('intents', []),
            'trained_at': self.metadata.get('trained_at', ''),
        }

    def retrain(self, additional_data=None):
        """Retrain the model with original + additional data."""
        all_data = list(UNIVERSITY_TRAINING_DATA)
        if additional_data:
            all_data.extend(additional_data)
        return self.train(all_data)
