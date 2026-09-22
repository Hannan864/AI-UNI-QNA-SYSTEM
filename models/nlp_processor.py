"""
NLP Processing Module - Phase 9 Implementation
AI Chatbot for University Support
NLTK + spaCy based text preprocessing, intent detection, and entity extraction
"""

import re
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)

# Download required NLTK data (quiet mode)
for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet',
                 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

INTENT_KEYWORDS = {
    'admissions': [
        'admission', 'admissions', 'apply', 'application', 'enroll', 'enrollment',
        'entry test', 'eligibility', 'entrance', 'prospectus', 'documents required',
        'admission process', 'how to apply', 'admission criteria', 'admission deadline'
    ],
    'course_registration': [
        'register', 'registration', 'course registration', 'enroll course',
        'add course', 'drop course', 'credit hour', 'credit hours', 'semester registration',
        'how to register', 'register for courses', 'course enrollment'
    ],
    'examinations': [
        'exam', 'examination', 'exams', 'midterm', 'mid-term', 'final exam',
        'final exams', 'test', 'assessment', 'grade', 'grades', 'grading',
        'gpa', 'cgpa', 'transcript', 'result', 'results', 'marks',
        'exam schedule', 'exam date', 'exam timetable', 'when are exams'
    ],
    'fees': [
        'fee', 'fees', 'tuition', 'payment', 'cost', 'price', 'charge',
        'semester fee', 'admission fee', 'fee structure', 'fee schedule',
        'how much', 'pay fee', 'fee payment', 'installment', 'refund',
        'scholarship', 'financial aid', 'waiver', 'stipend'
    ],
    'academic_policies': [
        'policy', 'policies', 'academic policy', 'academic policies',
        'rule', 'rules', 'regulation', 'regulations', 'academic rules',
        'grading policy', 'attendance', 'attendance policy', 'academic integrity',
        'plagiarism', 'disciplinary', 'code of conduct', 'academic standards'
    ],
    'university_services': [
        'service', 'services', 'facility', 'facilities', 'library',
        'hostel', 'hostel accommodation', 'transport', 'bus', 'canteen',
        'lab', 'laboratory', 'computer lab', 'wifi', 'internet',
        'health', 'medical', 'counseling', 'career', 'placement',
        'sport', 'sports', 'gym', 'auditorium'
    ],
    'courses': [
        'course', 'courses', 'program', 'programs', 'degree', 'degrees',
        'bs', 'bscs', 'bsit', 'bba', 'mba', 'ms', 'mphil', 'phd',
        'bachelor', 'master', 'doctorate', 'computer science',
        'software engineering', 'data science', 'engineering',
        'department', 'faculty', 'what courses', 'offered', 'available programs'
    ],
    'schedules': [
        'schedule', 'timetable', 'time table', 'class timing', 'class schedule',
        'hours', 'office hours', 'timing', 'calendar',
        'academic calendar', 'semester start', 'semester end',
        'holiday', 'holidays', 'vacation', 'break'
    ],
    'contact': [
        'contact', 'phone', 'email', 'address', 'office', 'reach',
        'helpline', 'support', 'help desk', 'helpdesk', 'where is',
        'location', 'map', 'directions'
    ],
    'faq': [
        'frequently asked', 'common question', 'faq', 'faqs',
        'general information', 'overview', 'about iiui', 'about university'
    ],
}

UNIVERSITY_ENTITIES = {
    'programs': [
        'bscs', 'bs cs', 'bsit', 'bs it', 'bs se', 'bs software',
        'bs data science', 'bs ds', 'bs mathematics', 'bs math',
        'bba', 'mba', 'bs accounting', 'bs finance',
        'bs electrical engineering', 'bs civil engineering', 'bs mechanical engineering',
        'bs psychology', 'bs sociology', 'bs international relations',
        'bs english', 'bs arabic', 'bs urdu',
        'bs islamic studies', 'bs shariah',
        'bachelor', 'master', 'doctorate', 'phd', 'mphil', 'ms',
    ],
    'semesters': [
        'first semester', 'second semester', 'third semester', 'fourth semester',
        'fifth semester', 'sixth semester', 'seventh semester', 'eighth semester',
        'semester 1', 'semester 2', 'semester 3', 'semester 4',
        'semester 5', 'semester 6', 'semester 7', 'semester 8',
        '1st semester', '2nd semester', '3rd semester', '4th semester',
        'fall', 'spring', 'summer',
        'fall 2025', 'fall 2026', 'spring 2026', 'spring 2027',
    ],
    'exam_types': [
        'midterm', 'mid-term', 'mid term', 'final', 'finals',
        'final exam', 'final exams', 'midterm exam', 'viva', 'oral',
        'practical', 'lab exam', 'quiz', 'assignment', 'presentation',
    ],
    'departments': [
        'computer science', 'software engineering', 'data science',
        'electrical engineering', 'civil engineering', 'mechanical engineering',
        'business administration', 'accounting', 'finance',
        'psychology', 'sociology', 'international relations',
        'english', 'arabic', 'urdu', 'islamic studies', 'shariah',
        'mathematics', 'physics', 'chemistry',
    ],
    'fee_terms': [
        'fee', 'fees', 'tuition', 'payment', 'installment',
        'admission fee', 'semester fee', 'lab fee', 'library fee',
    ],
}


class NLPProcessor:
    """NLP Processing Module for university query understanding."""

    def __init__(self):
        self._ensure_nltk_data()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.nlp = None  # Lazy-loaded to avoid startup delay

    def _ensure_nltk_data(self):
        for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet',
                         'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass

    def _ensure_spacy(self):
        if self.nlp is not None:
            return
        try:
            import spacy
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                logger.info("Downloading spaCy model en_core_web_sm...")
                spacy.cli.download('en_core_web_sm')
                self.nlp = spacy.load('en_core_web_sm')
        except ImportError:
            logger.warning("spaCy not available. Using keyword-based fallback.")
        except Exception as e:
            logger.warning(f"spaCy model loading failed: {e}")

    def preprocess_text(self, text):
        if not text or not text.strip():
            return ''
        try:
            tokens = word_tokenize(text.lower())
            processed_tokens = [
                self.lemmatizer.lemmatize(token)
                for token in tokens
                if token.isalpha() and token not in self.stop_words
            ]
            return ' '.join(processed_tokens)
        except Exception as e:
            logger.error(f"Preprocessing error: {e}")
            return text.lower().strip()

    def clean_text(self, text):
        if not text or not text.strip():
            return ''
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def tokenize(self, text):
        if not text:
            return []
        try:
            return word_tokenize(text.lower())
        except Exception:
            return text.lower().split()

    def detect_intent(self, text):
        if not text or not text.strip():
            return {'intent': 'unknown', 'confidence': 0.0}

        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)

        intent_scores = {}
        for intent, keywords in INTENT_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in cleaned:
                    score += 2
                elif any(token in keyword.split() for token in tokens):
                    score += 1
            if score > 0:
                intent_scores[intent] = score

        if not intent_scores:
            return {'intent': 'unknown', 'confidence': 0.0}

        best_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[best_intent]
        total_possible = len(INTENT_KEYWORDS.get(best_intent, [])) * 2
        confidence = min(max_score / max(total_possible * 0.3, 1), 0.99)

        if max_score >= 4:
            confidence = min(confidence + 0.2, 0.99)

        return {'intent': best_intent, 'confidence': round(confidence, 2)}

    def extract_entities(self, text):
        entities = {
            'programs': [], 'semesters': [], 'exam_types': [],
            'departments': [], 'fee_terms': [], 'dates': [],
            'organizations': [], 'locations': [],
        }
        if not text:
            return entities

        self._ensure_spacy()
        cleaned = self.clean_text(text)
        for entity_type, keywords in UNIVERSITY_ENTITIES.items():
            for keyword in keywords:
                if keyword in cleaned:
                    if keyword not in entities.get(entity_type, []):
                        entities[entity_type].append(keyword)

        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ == 'ORG' and ent.text not in entities['organizations']:
                        entities['organizations'].append(ent.text)
                    elif ent.label_ == 'DATE' and ent.text not in entities['dates']:
                        entities['dates'].append(ent.text)
                    elif ent.label_ in ('GPE', 'LOC') and ent.text not in entities['locations']:
                        entities['locations'].append(ent.text)
            except Exception as e:
                logger.warning(f"spaCy entity extraction failed: {e}")

        return entities

    def get_keywords(self, text, top_n=5):
        if not text:
            return []
        self._ensure_spacy()
        if self.nlp:
            try:
                doc = self.nlp(text)
                keywords = [
                    token.lemma_.lower()
                    for token in doc
                    if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop
                ]
                return list(dict.fromkeys(keywords))[:top_n]
            except Exception:
                pass
        tokens = self.tokenize(text)
        return [t for t in tokens if t not in self.stop_words][:top_n]

    def calculate_similarity(self, text1, text2):
        self._ensure_spacy()
        if not self.nlp or not text1 or not text2:
            return 0.0
        try:
            return self.nlp(text1).similarity(self.nlp(text2))
        except Exception:
            return 0.0

    def process_query(self, text):
        if not text or not str(text).strip():
            return {
                'original_text': text or '',
                'cleaned_text': '',
                'tokens': [],
                'intent': 'unknown',
                'intent_confidence': 0.0,
                'entities': {},
                'keywords': [],
            }
        text = str(text).strip()
        intent_result = self.detect_intent(text)
        entities = self.extract_entities(text)
        keywords = self.get_keywords(text)
        cleaned = self.clean_text(text)
        tokens = self.tokenize(text)

        return {
            'original_text': text,
            'cleaned_text': cleaned,
            'tokens': tokens,
            'intent': intent_result['intent'],
            'intent_confidence': intent_result['confidence'],
            'entities': entities,
            'keywords': keywords,
        }
