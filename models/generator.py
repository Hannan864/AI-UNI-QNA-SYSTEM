from models.retriever import FAQRetriever
from models.nlp_processor import NLPProcessor
from database.db import DatabaseManager

class AnswerGenerator:
    def __init__(self):
        self.retriever = FAQRetriever()
        self.nlp = NLPProcessor()
        self.db = DatabaseManager()
        self.fallback_responses = [
            "I'm sorry, I couldn't find specific information about that in the university knowledge base. Please contact the relevant department directly.",
            "I don't have enough information to answer that question. You may want to check the IIUI website at https://www.iiu.edu.pk/",
            "That's a good question! For detailed information, please visit the IIUI administration office or check their official website.",
            "I'm not sure about that. Please reach out to the concerned department for accurate information."
        ]

    def generate_answer(self, query, user_email='anonymous'):
        """Generate answer for user query using mock data retrieval."""
        processed_query = self.nlp.preprocess_text(query)

        # Step 1: Try FAISS-based semantic retrieval (from FAQ index)
        results = self.retriever.retrieve(query, top_k=3)

        if results and results[0]['confidence'] > 0.6:
            best_result = results[0]
            answer = best_result['answer']
            confidence = best_result['confidence']
            self.db.log_chat(
                user_email=user_email, user_message=query,
                bot_response=answer, confidence=confidence,
                intent=self._detect_intent(query)
            )
            return {
                'answer': answer, 'confidence': confidence,
                'source': best_result['question'],
                'category': best_result.get('category', ''),
                'follow_ups': self._generate_follow_ups(best_result)
            }
        elif results:
            answer = self._synthesize_answer(results, query)
            confidence = results[0]['confidence']
            self.db.log_chat(
                user_email=user_email, user_message=query,
                bot_response=answer, confidence=confidence,
                intent=self._detect_intent(query)
            )
            return {
                'answer': answer, 'confidence': confidence,
                'source': 'Multiple sources',
                'related_questions': [r['question'] for r in results[:3]]
            }

        # Step 2: Fallback — keyword search across KB + FAQs
        kb_faq_results = self.db.search_all_active(query, limit=3)
        if kb_faq_results:
            best = kb_faq_results[0]
            answer = best['answer']
            confidence = 0.5
            self.db.log_chat(
                user_email=user_email, user_message=query,
                bot_response=answer, confidence=confidence,
                intent=self._detect_intent(query)
            )
            return {
                'answer': answer, 'confidence': confidence,
                'source': best.get('question', ''),
                'category': best.get('category', ''),
                'data_source': best.get('source', 'knowledge_base')
            }

        # Step 3: No match — safe fallback
        import random
        answer = random.choice(self.fallback_responses)
        self.db.log_chat(
            user_email=user_email, user_message=query,
            bot_response=answer, confidence=0.0,
            intent=self._detect_intent(query)
        )
        return {
            'answer': answer, 'confidence': 0.0,
            'source': 'Fallback',
            'suggestion': 'Please try rephrasing your question or contact IIUI support directly.'
        }
    
    def _synthesize_answer(self, results, query):
        """Synthesize answer from multiple results"""
        if len(results) == 1:
            return results[0]['answer']
        
        # Combine top results
        answers = [r['answer'] for r in results[:2]]
        synthesized = "Based on available information:\n\n" + "\n\n".join(answers)
        
        return synthesized
    
    def _detect_intent(self, query):
        """Simple intent detection"""
        query_lower = query.lower()
        
        intents = {
            'admission': ['admission', 'apply', 'enroll', 'register'],
            'fee': ['fee', 'payment', 'cost', 'price', 'charge'],
            'contact': ['contact', 'phone', 'email', 'reach'],
            'schedule': ['schedule', 'timetable', 'hours', 'timing'],
            'facility': ['facility', 'lab', 'library', 'hostel', 'sports']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return 'general'
    
    def _generate_follow_ups(self, result):
        """Generate follow-up questions based on category"""
        category = result.get('category', '').lower()
        
        follow_ups = {
            'admission': [
                "What documents are required for admission?",
                "When is the admission deadline?",
                "What is the entry test syllabus?"
            ],
            'fee': [
                "Are there any scholarships available?",
                "What is the fee refund policy?",
                "Can I pay fees in installments?"
            ],
            'contact': [
                "What are the office hours?",
                "Is there an emergency contact number?",
                "How can I schedule an appointment?"
            ]
        }
        
        return follow_ups.get(category, [])