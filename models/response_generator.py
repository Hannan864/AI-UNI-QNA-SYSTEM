"""
Response Generation Module - Phase 11 Implementation
AI Chatbot for University Support
Matches user intent with best possible response from Knowledge Base / FAQ / ML predictions
"""

import logging
from database.db import DatabaseManager

logger = logging.getLogger(__name__)

# Fallback responses for unknown queries
FALLBACK_RESPONSES = [
    "I couldn't confidently identify your university-related query. Please try asking about admissions, courses, examinations, fees, academic policies, schedules, or university services.",
    "I'm not sure I understand. You can ask about:\n- Admissions process\n- Course registration\n- Examination schedules\n- Fee structure\n- Academic policies\n- University services",
    "That's outside my university support scope. Please ask about admissions, courses, fees, exams, schedules, or campus services.",
]

# Intent-to-category mapping for knowledge base / FAQ lookup
INTENT_CATEGORY_MAP = {
    'admissions': ['Admissions', 'Admission'],
    'course_registration': ['Courses', 'Registration'],
    'examinations': ['Examinations', 'Exams', 'Academic'],
    'fees': ['Fees', 'Fee', 'Scholarship'],
    'academic_policies': ['Academic', 'Policies', 'Rules'],
    'university_services': ['Services', 'Facilities', 'General'],
    'courses': ['Courses', 'Programs', 'General'],
    'schedules': ['Schedule', 'Academic', 'General'],
    'contact': ['Contact', 'General'],
    'faq': ['General', 'FAQ'],
}


class ResponseGenerator:
    """Response Generation Module.

    Uses NLP intent detection + ML predictions + Knowledge Base/FAQ
    to generate the best matching response for university queries.
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.fallback_responses = FALLBACK_RESPONSES

    def generate_response(self, nlp_result, ml_result=None):
        """Generate a response using NLP results, ML predictions, and knowledge base.

        Args:
            nlp_result: dict from NLPProcessor.process_query()
            ml_result: dict from MLClassifier.predict() (optional)

        Returns:
            dict with 'answer', 'confidence', 'source', 'intent', 'entities'
        """
        intent = nlp_result.get('intent', 'unknown')
        nlp_confidence = nlp_result.get('intent_confidence', 0.0)
        entities = nlp_result.get('entities', {})
        keywords = nlp_result.get('keywords', [])
        original_text = nlp_result.get('original_text', '')

        # Use ML prediction if available and higher confidence
        ml_intent = None
        ml_confidence = 0.0
        if ml_result:
            ml_intent = ml_result.get('intent', 'unknown')
            ml_confidence = ml_result.get('confidence', 0.0)

        # Choose the best intent (ML takes priority if confident)
        if ml_intent and ml_confidence > nlp_confidence and ml_intent != 'unknown':
            final_intent = ml_intent
            final_confidence = ml_confidence
        else:
            final_intent = intent
            final_confidence = nlp_confidence

        # If unknown intent, return fallback
        if final_intent == 'unknown' or final_confidence < 0.2:
            import random
            return {
                'answer': random.choice(self.fallback_responses),
                'confidence': 0.1,
                'source': 'Fallback',
                'intent': 'unknown',
                'entities': entities,
                'keywords': keywords,
            }

        # Try to find matching KB/FAQ entries
        categories = INTENT_CATEGORY_MAP.get(final_intent, ['General'])

        # Search knowledge base
        for category in categories:
            kb_results = self.db.get_all_knowledge(category=category, status='active')
            if kb_results:
                best = kb_results[0]
                return {
                    'answer': best['answer'],
                    'confidence': min(final_confidence + 0.3, 0.95),
                    'source': f"Knowledge Base ({category})",
                    'intent': final_intent,
                    'entities': entities,
                    'keywords': keywords,
                }

        # Search FAQs
        for category in categories:
            faq_results = self.db.get_all_faqs()
            matching_faqs = [f for f in faq_results if f.get('category', '').lower() == category.lower()]
            if matching_faqs:
                best = matching_faqs[0]
                return {
                    'answer': best['answer'],
                    'confidence': min(final_confidence + 0.2, 0.90),
                    'source': f"FAQ ({category})",
                    'intent': final_intent,
                    'entities': entities,
                    'keywords': keywords,
                }

        # Fallback: search all active KB by keywords
        all_kb = self.db.get_all_knowledge(status='active')
        if all_kb and keywords:
            for entry in all_kb:
                entry_text = (entry.get('question', '') + ' ' + entry.get('keywords', '')).lower()
                if any(kw in entry_text for kw in keywords):
                    return {
                        'answer': entry['answer'],
                        'confidence': min(final_confidence + 0.1, 0.70),
                        'source': f"Knowledge Base (keyword match)",
                        'intent': final_intent,
                        'entities': entities,
                        'keywords': keywords,
                    }

        # No match found
        import random
        return {
            'answer': random.choice(self.fallback_responses),
            'confidence': 0.1,
            'source': 'Fallback',
            'intent': final_intent,
            'entities': entities,
            'keywords': keywords,
        }
