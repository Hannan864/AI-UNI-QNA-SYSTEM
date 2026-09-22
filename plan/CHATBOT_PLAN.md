# Chatbot/NLP Plan — IIUI Smart Chatbot

**Date:** August 18, 2026  
**Version:** 1.0

---

## 1. Current Chatbot Architecture

### 1.1 Processing Pipeline

```
User Query
    ↓
NLP Preprocessing (nlp_processor.py)
    ↓
Embedding Generation (retriever.py)
    ↓
FAISS Similarity Search
    ↓
Confidence Scoring
    ↓
Response Generation (generator.py)
    ↓
Bot Response
```

### 1.2 Current Implementation

| Component | File | Status |
|-----------|------|--------|
| NLP Preprocessing | `models/nlp_processor.py` | ✅ Implemented |
| Embedding Model | `models/retriever.py` | ✅ Implemented |
| FAISS Index | `models/retriever.py` | ✅ Implemented |
| Answer Generator | `models/generator.py` | ✅ Implemented |
| Intent Classifier | `models/intent_classifier.py` | ❌ Empty |
| Knowledge Base | `database/db.py` | ⚠️ Minimal data |

---

## 2. Current Chatbot Flow

```
1. User sends message
2. NLPProcessor.preprocess_text() tokenizes and lemmatizes
3. FAQRetriever.retrieve() generates embeddings and searches FAISS
4. If confidence > 0.6: Return best match
5. If confidence > 0: Synthesize from multiple results
6. Else: Return fallback response
7. Log interaction to database
```

---

## 3. Current Strengths

1. **Semantic Search** — Uses Sentence Transformers for meaning-based matching
2. **FAISS Index** — Fast similarity search
3. **Confidence Scoring** — Knows when it's uncertain
4. **Fallback Handling** — Graceful degradation
5. **NLP Pipeline** — Proper text preprocessing
6. **Intent Detection** — Basic keyword-based detection
7. **Chat Logging** — Tracks all interactions

---

## 4. Current Weaknesses

1. **Minimal Knowledge Base** — Only 2 FAQs
2. **No Multi-turn Conversation** — Each query independent
3. **No Context Awareness** — Doesn't remember previous messages
4. **Basic Intent Detection** — Simple keyword matching
5. **No Entity Extraction for Queries** — Extracts entities but doesn't use them
6. **No Query Expansion** — Doesn't improve search queries
7. **No Answer Ranking** — Only uses top result
8. **No Response Templates** — Raw database answers

---

## 5. Recommended Architecture

### 5.1 Simple Reliable Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Streamlit Chat Interface)                  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Query Processing                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Preprocess  │→ │   Intent    │→ │   Entity    │     │
│  │   Text      │  │  Detection  │  │  Extraction │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Knowledge Retrieval                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Embedding  │→ │   FAISS     │→ │   Result    │     │
│  │  Generation │  │   Search    │  │  Filtering  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                Response Generation                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Answer    │→ │  Template   │→ │  Confidence │     │
│  │  Selection  │  │  Formatting │  │   Scoring   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Response Output                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Main      │  │  Follow-up  │  │   Source    │     │
│  │  Answer     │  │ Questions   │  │ Attribution │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Query Processing

### 6.1 Preprocessing Steps

```python
def preprocess_query(query):
    # 1. Lowercase
    query = query.lower()
    
    # 2. Remove special characters
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
    
    # 3. Tokenize
    tokens = word_tokenize(query)
    
    # 4. Remove stopwords
    tokens = [t for t in tokens if t not in stop_words]
    
    # 5. Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    
    return ' '.join(tokens)
```

### 6.2 Intent Detection

**Current approach:** Keyword matching  
**Improved approach:** Keyword + Pattern matching

```python
INTENTS = {
    'admission': {
        'keywords': ['admission', 'apply', 'enroll', 'registration', 'entry test'],
        'patterns': [
            r'how to (apply|admit|enroll)',
            r'admission (process|deadline|requirements)',
            r'when is.*admission'
        ]
    },
    'fee': {
        'keywords': ['fee', 'payment', 'cost', 'price', 'tuition'],
        'patterns': [
            r'how much.*fee',
            r'fee (structure|payment|refund)',
            r'what is.*fee'
        ]
    },
    'exam': {
        'keywords': ['exam', 'test', 'schedule', 'result', 'grade'],
        'patterns': [
            r'when is.*exam',
            r'exam (schedule|result|date)',
            r'how to.*result'
        ]
    },
    'contact': {
        'keywords': ['contact', 'phone', 'email', 'address', 'office'],
        'patterns': [
            r'how to (contact|reach)',
            r'(phone|email|address) of',
            r'where is.*office'
        ]
    }
}
```

### 6.3 Entity Extraction

**Use cases:**
- Department name → Filter results
- Program name → Filter results
- Date/Time → Schedule queries
- Person name → Contact queries

---

## 7. Knowledge Retrieval

### 7.1 Embedding Generation

```python
# Current implementation uses Sentence Transformers
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(query)
```

### 7.2 Search Strategy

```python
def retrieve(query, top_k=5):
    # 1. Generate query embedding
    query_embedding = model.encode([query])
    
    # 2. Search FAISS index
    scores, indices = index.search(query_embedding, top_k)
    
    # 3. Filter by confidence threshold
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if score > 0.4:  # Minimum threshold
            results.append({
                'faq': faqs[idx],
                'confidence': score
            })
    
    return results
```

### 7.3 Query Expansion

```python
def expand_query(query):
    # Add synonyms
    synonyms = {
        'admission': ['admission', 'apply', 'enroll', 'join'],
        'fee': ['fee', 'cost', 'payment', 'tuition', 'charges'],
        'exam': ['exam', 'test', 'assessment', 'evaluation']
    }
    
    expanded = [query]
    for word in query.split():
        if word in synonyms:
            expanded.extend(synonyms[word])
    
    return ' '.join(set(expanded))
```

---

## 8. Response Generation

### 8.1 Response Templates

```python
TEMPLATES = {
    'high_confidence': {
        'template': "{answer}\n\n_Source: {source}_",
        'description': 'Direct answer from knowledge base'
    },
    'medium_confidence': {
        'template': "Based on available information:\n\n{answer}\n\n_Related: {related}_",
        'description': 'Synthesized from multiple sources'
    },
    'low_confidence': {
        'template': "{fallback}\n\n_Suggestion: {suggestion}_",
        'description': 'Fallback with helpful suggestion'
    },
    'no_results': {
        'template': "I don't have specific information about that.\n\n{suggestion}",
        'description': 'No matching knowledge found'
    }
}
```

### 8.2 Follow-up Questions

```python
FOLLOW_UPS = {
    'admission': [
        "What documents are required for admission?",
        "When is the admission deadline?",
        "What is the entry test syllabus?",
        "How can I check my admission status?"
    ],
    'fee': [
        "Are there any scholarships available?",
        "What is the fee refund policy?",
        "Can I pay fees in installments?",
        "What are the payment methods?"
    ],
    'exam': [
        "When will the exam schedule be announced?",
        "How can I check my results?",
        "What is the grading system?",
        "Are there any re-exam policies?"
    ]
}
```

---

## 9. Unknown Question Handling

### 9.1 Confidence Thresholds

| Confidence | Action |
|------------|--------|
| > 0.8 | Return direct answer |
| 0.6 - 0.8 | Return answer with source |
| 0.4 - 0.6 | Return synthesized answer |
| 0.2 - 0.4 | Return fallback with suggestion |
| < 0.2 | Return "I don't know" with help |

### 9.2 Fallback Responses

```python
FALLBACKS = {
    'general': [
        "I'm not sure about that. Could you rephrase your question?",
        "I don't have specific information on that topic.",
        "For detailed information, please visit the IIUI website or contact the relevant department."
    ],
    'admission': [
        "For admission inquiries, please contact the Admissions Office at admissions@iiu.edu.pk",
        "You can check the admission status on the IIUI portal or visit the registrar office."
    ],
    'technical': [
        "For technical issues, please contact the IT Help Desk at ithelp@iiu.edu.pk",
        "You can also visit the IT department in the Admin Block."
    ]
}
```

---

## 10. Improvements to Implement

### 10.1 Priority 1 (Must Have)

1. **Expand Knowledge Base** — Add 100+ FAQs
2. **Improve Intent Detection** — Pattern-based matching
3. **Add Response Templates** — Formatted responses
4. **Add Follow-up Questions** — Context-aware suggestions

### 10.2 Priority 2 (Should Have)

1. **Query Expansion** — Better search results
2. **Result Ranking** — Multiple result comparison
3. **Context Tracking** — Remember conversation history
4. **Entity Extraction** — Use extracted entities for filtering

### 10.3 Priority 3 (Nice to Have)

1. **Multi-turn Conversation** — Handle follow-up questions
2. **Sentiment Analysis** — Detect user frustration
3. **Learning from Feedback** — Improve over time
4. **Urdu Support** — Multilingual capability

---

## 11. Testing Strategy

### 11.1 Unit Tests

```python
# Test NLP preprocessing
def test_preprocess_text():
    result = nlp.preprocess_text("What is the admission process?")
    assert "admission" in result
    assert "process" in result

# Test intent detection
def test_detect_intent():
    intent = generator._detect_intent("What is the fee structure?")
    assert intent == "fee"

# Test FAQ retrieval
def test_retrieve():
    results = retriever.retrieve("admission process")
    assert len(results) > 0
    assert results[0]['confidence'] > 0.5
```

### 11.2 Integration Tests

```python
# Test end-to-end chat
def test_chat():
    response = generator.generate_answer("What is the fee structure?")
    assert response['success'] == True
    assert response['confidence'] > 0
    assert len(response['answer']) > 0
```

### 11.3 Performance Tests

```python
# Test response time
def test_response_time():
    start = time.time()
    response = generator.generate_answer("admission")
    elapsed = time.time() - start
    assert elapsed < 3.0  # Should respond in under 3 seconds
```

---

## 12. Metrics to Track

| Metric | Target | Current |
|--------|--------|---------|
| Response Time | < 3 seconds | Unknown |
| Confidence Score | > 0.7 average | Unknown |
| Intent Detection Accuracy | > 80% | Unknown |
| User Satisfaction | > 4/5 | Unknown |
| Fallback Rate | < 20% | Unknown |
| Knowledge Base Coverage | > 90% queries | ~10% |

---

## 13. Future Enhancements

1. **LLM Integration** — Use OpenAI/LLaMA for complex queries
2. **RAG Architecture** — Retrieval-Augmented Generation
3. **Conversation Memory** — Multi-turn dialogue
4. **Personalization** — User-specific responses
5. **Analytics Dashboard** — Track chatbot performance
6. **A/B Testing** — Test different response strategies
7. **Continuous Learning** — Improve from user feedback
