"""
Centralized Chat Router - Mock/Live Mode Routing
Phase 8 + Phase 9/10/11 Integration - FYP Compliant

Provides a single entry point for all chat requests.
Routes to Mock Data Service or Live AI Service based on mode.
NLP processing and ML classification enhance mock mode routing.
"""

import time
import logging
from database.db import DatabaseManager
from models.generator import AnswerGenerator
from models.live_ai_service import LiveAIService
from models.nlp_processor import NLPProcessor
from models.ml_classifier import MLClassifier
from models.response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

# Valid modes
VALID_MODES = ("mock", "live")


class ChatRouter:
    """Centralized mode router for chat requests.

    Architecture:
        Chat Request
             |
        Mode Router
           /       \
      Mock Mode   Live Mode
          |           |
     Mock Service  Live AI Service
          |           |
    Knowledge Base  AI Provider
          |           |
          +-----+-----+
                |
             Response
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.mock_service = AnswerGenerator()
        self.live_service = LiveAIService()
        self.nlp = NLPProcessor()
        self.ml_classifier = MLClassifier()
        self.response_generator = ResponseGenerator()

    def route(self, message, mode="mock", user_email="anonymous",
              conversation_id=None):
        """Route a chat request to the appropriate service.

        Args:
            message: The user's message text.
            mode: "mock" or "live". Invalid mode defaults to "mock".
            user_email: Email of the requesting user.
            conversation_id: Optional conversation ID for context.

        Returns:
            dict with response data including mode, mode_label, answer, etc.
        """
        # Validate mode - invalid defaults to mock
        if mode not in VALID_MODES:
            mode = "mock"

        start_time = time.time()

        if mode == "live":
            result = self._route_live(message, user_email, conversation_id)
        else:
            result = self._route_mock(message, user_email, conversation_id)

        elapsed_ms = int((time.time() - start_time) * 1000)
        result["response_time_ms"] = elapsed_ms

        return result

    def _route_mock(self, message, user_email, conversation_id):
        """Route to Mock Data Service.

        Uses NLP processing + ML classification + Knowledge Base / FAQ retrieval.
        NEVER calls any external AI provider.
        """
        # NLP processing
        nlp_result = self.nlp.process_query(message)
        ml_result = self.ml_classifier.predict(message)

        try:
            # Use NLP-enhanced response generator
            response = self.response_generator.generate_response(nlp_result, ml_result)
            # If response generator returns fallback with low confidence,
            # fall back to the original AnswerGenerator (FAISS-based)
            if response.get('confidence', 0) < 0.3:
                kb_response = self.mock_service.generate_answer(message, user_email)
                if kb_response.get('confidence', 0) > response.get('confidence', 0):
                    response = kb_response
                    response['nlp_intent'] = nlp_result.get('intent', 'unknown')
                    response['ml_intent'] = ml_result.get('intent', 'unknown')
            else:
                response['nlp_intent'] = nlp_result.get('intent', 'unknown')
                response['ml_intent'] = ml_result.get('intent', 'unknown')
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            try:
                response = self.mock_service.generate_answer(message, user_email)
            except Exception as e2:
                logger.error(f"Mock service error: {e2}")
                response = {
                    "answer": "I am sorry, I encountered an error processing your request.",
                    "confidence": 0.0,
                    "source": "Error Handler",
                }

        # Log the chat
        self.db.log_chat(
            user_email=user_email,
            user_message=message,
            bot_response=response.get("answer", ""),
            confidence=response.get("confidence", 0.0),
            mode="mock",
            intent=response.get("source", ""),
        )

        # Store in conversation if provided
        if conversation_id:
            conv = self.db.get_conversation_by_id(conversation_id)
            if conv:
                self.db.add_message(conversation_id, "user", message, mode="mock")
                self.db.add_message(
                    conversation_id, "assistant",
                    response.get("answer", ""), mode="mock"
                )

        return {
            **response,
            "mode": "mock",
            "mode_label": "Mock Data",
        }

    def _route_live(self, message, user_email, conversation_id):
        """Route to Live AI Service.

        Uses configured AI provider (OpenAI, Anthropic, Custom).
        NEVER falls back to Mock Data silently.
        """
        # Build conversation context from history if available
        conversation_context = None
        if conversation_id:
            conv = self.db.get_conversation_by_id(conversation_id)
            if conv:
                msgs = self.db.get_messages(conversation_id)
                conversation_context = [
                    {"role": m["sender"], "content": m["message"]}
                    for m in msgs[-10:]  # Last 10 messages for context
                ]

        # Call Live AI service - this may return an error if not configured
        result = self.live_service.generate_response(message, conversation_context)

        # Log the chat
        self.db.log_chat(
            user_email=user_email,
            user_message=message,
            bot_response=result.get("answer", ""),
            confidence=result.get("confidence", 0.0),
            mode="live",
            intent="Live AI",
        )

        # Store in conversation if provided and successful
        if conversation_id and result.get("success"):
            self.db.add_message(conversation_id, "user", message, mode="live")
            self.db.add_message(
                conversation_id, "assistant",
                result.get("answer", ""), mode="live"
            )

        return {
            **result,
            "mode": "live",
            "mode_label": "Live AI",
        }

    def get_mode_status(self):
        """Get the current status of both modes.

        Returns:
            dict with mock and live mode status.
        """
        return {
            "mock": {
                "available": True,
                "description": "Knowledge Base / FAQ powered responses",
            },
            "live": {
                "available": self.live_service.is_configured(),
                "configured": self.live_service.is_configured(),
                "description": "AI provider powered responses",
            },
        }
