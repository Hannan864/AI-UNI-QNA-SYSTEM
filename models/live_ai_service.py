"""
Live AI Service - Provider-Agnostic AI Integration
Phase 7 Implementation - FYP Compliant

Supports multiple AI providers without hard-coding any single one.
Provider selection is configurable via admin settings.
"""

import json
import logging
import requests
import time
from database.db import DatabaseManager

logger = logging.getLogger(__name__)

# University support system prompt
UNIVERSITY_SYSTEM_PROMPT = """You are an AI assistant for the International Islamic University Islamabad (IIUI).
Your purpose is to assist students, faculty, and staff with university-related queries.

You can help with:
- Admissions process and requirements
- Course registration and academic programs
- Examination schedules and policies
- Fee structure and payment information
- Academic policies and rules
- University services and facilities
- Scholarships and financial aid
- General university information

Guidelines:
- Provide accurate and helpful information about IIUI.
- If you are unsure about specific details, recommend the user contact the relevant department.
- Be professional, concise, and supportive.
- Stay focused on university-related topics.
- Do not fabricate information. If you don't know, say so clearly.
- Respond in the same language the user uses.
"""

# Supported providers
SUPPORTED_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1/chat/completions",
        "requires_base_url": False,
    },
    "anthropic": {
        "name": "Anthropic",
        "base_url": "https://api.anthropic.com/v1/messages",
        "requires_base_url": False,
    },
    "custom": {
        "name": "Custom / Local",
        "base_url": "",
        "requires_base_url": True,
    },
}


class LiveAIService:
    """Provider-agnostic Live AI service for the university chatbot."""

    def __init__(self):
        self.db = DatabaseManager()

    def get_config(self):
        """Get the current AI configuration from the database."""
        return self.db.get_ai_config()

    def is_configured(self):
        """Check if Live AI is properly configured and enabled."""
        cfg = self.get_config()
        if not cfg:
            return False
        return bool(cfg.get("enabled") and cfg.get("provider") and cfg.get("api_key_encrypted"))

    def get_provider_list(self):
        """Return list of supported providers."""
        return [
            {"id": k, "name": v["name"], "requires_base_url": v["requires_base_url"]}
            for k, v in SUPPORTED_PROVIDERS.items()
        ]

    def test_connection(self):
        """Test the AI provider connection with a simple prompt."""
        cfg = self.get_config()
        if not cfg or not cfg.get("provider"):
            return {
                "success": False,
                "status": "not_configured",
                "message": "No AI provider configured. Please save configuration first.",
            }
        if not cfg.get("enabled"):
            return {
                "success": False,
                "status": "disabled",
                "message": "AI is disabled. Enable it to test the connection.",
            }
        if not cfg.get("api_key_encrypted"):
            return {
                "success": False,
                "status": "no_api_key",
                "message": "No API key configured. Please enter your API key.",
            }

        provider = cfg["provider"]
        if provider not in SUPPORTED_PROVIDERS:
            return {
                "success": False,
                "status": "invalid_provider",
                "message": f"Unsupported provider: {provider}",
            }

        try:
            result = self._call_provider(
                provider=provider,
                api_key=cfg["api_key_encrypted"],
                model=cfg["model"],
                base_url=cfg.get("base_url", ""),
                messages=[{"role": "user", "content": "Say 'Connection successful' in exactly 3 words."}],
                temperature=0.0,
                max_tokens=20,
                timeout=15,
            )
            if result.get("success"):
                return {
                    "success": True,
                    "status": "connected",
                    "message": f"Successfully connected to {SUPPORTED_PROVIDERS[provider]['name']} using model {cfg.get('model', 'default')}.",
                    "provider": provider,
                    "model": cfg.get("model", ""),
                }
            else:
                return {
                    "success": False,
                    "status": "error",
                    "message": result.get("error", "Connection test failed."),
                }
        except requests.Timeout:
            return {
                "success": False,
                "status": "timeout",
                "message": "Connection timed out. Please check your network and provider status.",
            }
        except requests.ConnectionError:
            return {
                "success": False,
                "status": "connection_error",
                "message": "Could not connect to the AI provider. Please check your network.",
            }
        except Exception as e:
            logger.error(f"AI test connection error: {type(e).__name__}")
            return {
                "success": False,
                "status": "error",
                "message": "An unexpected error occurred while testing the connection.",
            }

    def generate_response(self, user_message, conversation_history=None):
        """Generate a response using the configured AI provider.

        Args:
            user_message: The user's message text.
            conversation_history: Optional list of prior messages for context.

        Returns:
            dict with 'success', 'answer', 'confidence', 'source', 'mode', 'mode_label'.
        """
        if not self.is_configured():
            return {
                "success": False,
                "answer": "Live AI is not currently configured. Please configure an AI provider in Settings.",
                "confidence": 0.0,
                "source": "System",
                "mode": "live",
                "mode_label": "Live AI",
                "error_type": "not_configured",
            }

        cfg = self.get_config()
        provider = cfg["provider"]
        api_key = cfg["api_key_encrypted"]
        model = cfg.get("model", "")
        base_url = cfg.get("base_url", "")
        temperature = cfg.get("temperature", 0.7)
        max_tokens = cfg.get("max_tokens", 500)

        # Build messages with system prompt and conversation context
        messages = [{"role": "system", "content": UNIVERSITY_SYSTEM_PROMPT}]

        # Add conversation history (limited to last 10 messages for context window)
        if conversation_history:
            for msg in conversation_history[-10:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": user_message})

        try:
            result = self._call_provider(
                provider=provider,
                api_key=api_key,
                model=model,
                base_url=base_url,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=30,
            )

            if result.get("success"):
                answer = result.get("answer", "").strip()
                if not answer:
                    return {
                        "success": False,
                        "answer": "The AI provider returned an empty response. Please try again.",
                        "confidence": 0.0,
                        "source": "System",
                        "mode": "live",
                        "mode_label": "Live AI",
                        "error_type": "empty_response",
                    }
                return {
                    "success": True,
                    "answer": answer,
                    "confidence": 0.85,
                    "source": f"AI ({SUPPORTED_PROVIDERS.get(provider, {}).get('name', provider)})",
                    "mode": "live",
                    "mode_label": "Live AI",
                }
            else:
                error_msg = result.get("error", "Unknown error")
                error_type = result.get("error_type", "provider_error")

                # Map error types to user-friendly messages
                user_messages = {
                    "invalid_api_key": "Invalid API key. Please check your API key in Settings.",
                    "provider_unavailable": "The AI provider is currently unavailable. Please try again later.",
                    "model_unavailable": "The specified model is not available. Please check your model configuration in Settings.",
                    "timeout": "The AI provider timed out. Please try again later.",
                    "network_error": "Network error. Please check your internet connection.",
                    "rate_limit": "Rate limit exceeded. Please wait a moment and try again.",
                    "invalid_config": "Invalid AI configuration. Please check your settings.",
                }

                return {
                    "success": False,
                    "answer": user_messages.get(error_type, "An error occurred while communicating with the AI provider. Please try again."),
                    "confidence": 0.0,
                    "source": "System",
                    "mode": "live",
                    "mode_label": "Live AI",
                    "error_type": error_type,
                }

        except requests.Timeout:
            return {
                "success": False,
                "answer": "The AI provider timed out. Please try again later.",
                "confidence": 0.0,
                "source": "System",
                "mode": "live",
                "mode_label": "Live AI",
                "error_type": "timeout",
            }
        except requests.ConnectionError:
            return {
                "success": False,
                "answer": "Could not connect to the AI provider. Please check your internet connection.",
                "confidence": 0.0,
                "source": "System",
                "mode": "live",
                "mode_label": "Live AI",
                "error_type": "network_error",
            }
        except Exception as e:
            logger.error(f"Live AI error: {type(e).__name__}")
            return {
                "success": False,
                "answer": "An unexpected error occurred. Please try again or contact support.",
                "confidence": 0.0,
                "source": "System",
                "mode": "live",
                "mode_label": "Live AI",
                "error_type": "backend_error",
            }

    def _call_provider(self, provider, api_key, model, base_url, messages,
                       temperature=0.7, max_tokens=500, timeout=30):
        """Make the actual API call to the AI provider.

        Returns:
            dict with 'success' and either 'answer' or 'error'/'error_type'.
        """
        if provider == "openai":
            return self._call_openai(api_key, model, messages, temperature, max_tokens, timeout)
        elif provider == "anthropic":
            return self._call_anthropic(api_key, model, messages, temperature, max_tokens, timeout)
        elif provider == "custom":
            return self._call_custom(base_url, api_key, model, messages, temperature, max_tokens, timeout)
        else:
            return {"success": False, "error": f"Unsupported provider: {provider}", "error_type": "invalid_config"}

    def _call_openai(self, api_key, model, messages, temperature, max_tokens, timeout):
        """Call OpenAI-compatible API."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        except requests.Timeout:
            return {"success": False, "error": "Request timed out.", "error_type": "timeout"}
        except requests.ConnectionError:
            return {"success": False, "error": "Network error.", "error_type": "network_error"}

        if resp.status_code == 401:
            return {"success": False, "error": "Invalid API key.", "error_type": "invalid_api_key"}
        if resp.status_code == 429:
            return {"success": False, "error": "Rate limit exceeded.", "error_type": "rate_limit"}
        if resp.status_code == 404:
            return {"success": False, "error": "Model not found.", "error_type": "model_unavailable"}
        if resp.status_code == 503:
            return {"success": False, "error": "Service unavailable.", "error_type": "provider_unavailable"}
        if resp.status_code >= 400:
            try:
                err_data = resp.json()
                err_msg = err_data.get("error", {}).get("message", f"Provider error (HTTP {resp.status_code})")
            except Exception:
                err_msg = f"Provider error (HTTP {resp.status_code})"
            return {"success": False, "error": err_msg, "error_type": "provider_error"}

        try:
            data = resp.json()
            answer = data["choices"][0]["message"]["content"]
            return {"success": True, "answer": answer}
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return {"success": False, "error": "Failed to parse provider response.", "error_type": "provider_error"}

    def _call_anthropic(self, api_key, model, messages, temperature, max_tokens, timeout):
        """Call Anthropic Messages API."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        # Extract system message and convert rest
        system_text = ""
        api_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                api_messages.append({"role": msg["role"], "content": msg["content"]})

        if not api_messages:
            api_messages = [{"role": "user", "content": "Hello"}]

        payload = {
            "model": model or "claude-3-haiku-20240307",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": api_messages,
        }
        if system_text:
            payload["system"] = system_text

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        except requests.Timeout:
            return {"success": False, "error": "Request timed out.", "error_type": "timeout"}
        except requests.ConnectionError:
            return {"success": False, "error": "Network error.", "error_type": "network_error"}

        if resp.status_code == 401:
            return {"success": False, "error": "Invalid API key.", "error_type": "invalid_api_key"}
        if resp.status_code == 429:
            return {"success": False, "error": "Rate limit exceeded.", "error_type": "rate_limit"}
        if resp.status_code == 404:
            return {"success": False, "error": "Model not found.", "error_type": "model_unavailable"}
        if resp.status_code == 529:
            return {"success": False, "error": "Service overloaded.", "error_type": "provider_unavailable"}
        if resp.status_code >= 400:
            try:
                err_data = resp.json()
                err_msg = err_data.get("error", {}).get("message", f"Provider error (HTTP {resp.status_code})")
            except Exception:
                err_msg = f"Provider error (HTTP {resp.status_code})"
            return {"success": False, "error": err_msg, "error_type": "provider_error"}

        try:
            data = resp.json()
            content = data["content"][0]["text"]
            return {"success": True, "answer": content}
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return {"success": False, "error": "Failed to parse provider response.", "error_type": "provider_error"}

    def _call_custom(self, base_url, api_key, model, messages, temperature, max_tokens, timeout):
        """Call a custom OpenAI-compatible API endpoint."""
        if not base_url:
            return {"success": False, "error": "No base URL configured for custom provider.", "error_type": "invalid_config"}

        # Ensure URL ends with /chat/completions for OpenAI-compatible endpoints
        url = base_url.rstrip("/")
        if not url.endswith("/chat/completions"):
            if url.endswith("/v1"):
                url = url + "/chat/completions"
            else:
                url = url + "/v1/chat/completions" if "/v1" not in url else url + "/chat/completions"

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model or "default",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        except requests.Timeout:
            return {"success": False, "error": "Request timed out.", "error_type": "timeout"}
        except requests.ConnectionError:
            return {"success": False, "error": "Could not connect to custom endpoint.", "error_type": "network_error"}

        if resp.status_code == 401:
            return {"success": False, "error": "Invalid API key.", "error_type": "invalid_api_key"}
        if resp.status_code == 429:
            return {"success": False, "error": "Rate limit exceeded.", "error_type": "rate_limit"}
        if resp.status_code >= 400:
            try:
                err_data = resp.json()
                err_msg = err_data.get("error", {}).get("message", f"Provider error (HTTP {resp.status_code})")
            except Exception:
                err_msg = f"Provider error (HTTP {resp.status_code})"
            return {"success": False, "error": err_msg, "error_type": "provider_error"}

        try:
            data = resp.json()
            answer = data["choices"][0]["message"]["content"]
            return {"success": True, "answer": answer}
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return {"success": False, "error": "Failed to parse provider response.", "error_type": "provider_error"}
