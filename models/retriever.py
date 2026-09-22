import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
import faiss
from database.db import DatabaseManager
from models.nlp_processor import NLPProcessor

class FAQRetriever:
    def __init__(self):
        self.model = None  # Lazy-loaded to avoid startup delay
        self.db = DatabaseManager()
        self.nlp = None  # Lazy-loaded
        self.embedding_dim = 384
        self.index = None
        self.faqs = []
        self.embeddings_file = 'embeddings/faq_embeddings.pkl'
        self._ready = False

    def _ensure_model(self):
        if self.model is None:
            print("Loading sentence-transformers model (first time only)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        if self.nlp is None:
            self.nlp = NLPProcessor()

    def _ensure_ready(self):
        if not self._ready:
            self._ensure_model()
            self._load_or_build_index()
            self._ready = True
    
    def _load_or_build_index(self):
        """Load existing embeddings or build new ones"""
        os.makedirs('embeddings', exist_ok=True)
        
        # Check if file exists
        if os.path.exists(self.embeddings_file):
            try:
                # Try to load
                self._load_embeddings()
                print("Embeddings loaded successfully.")
            except Exception as e:
                # If any error occurs (EOFError, corruption, etc.), delete and rebuild
                print(f"Error loading embeddings ({str(e)}). Rebuilding index...")
                if os.path.exists(self.embeddings_file):
                    os.remove(self.embeddings_file)
                self._build_index()
        else:
            self._build_index()
    
    def _build_index(self):
        """Build FAISS index from FAQs"""
        faqs = self.db.get_all_faqs()
        
        if not faqs:
            print("No FAQs found in database. Please run database/init_db.py first.")
            return
        
        self.faqs = faqs
        questions = [faq['question'] for faq in faqs]
        
        print(f"Generating embeddings for {len(questions)} FAQs...")
        # Generate embeddings
        embeddings = self.model.encode(questions, convert_to_numpy=True)
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.index.add(embeddings.astype('float32'))
        
        # Save embeddings
        self._save_embeddings(embeddings)
        
        print(f"Built index with {len(faqs)} FAQs")
    
    def _save_embeddings(self, embeddings):
        """Save embeddings to file"""
        data = {
            'faqs': self.faqs,
            'embeddings': embeddings
        }
        # Use 'wb' to write binary
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(data, f)
    
    def _load_embeddings(self):
        """Load embeddings from file"""
        with open(self.embeddings_file, 'rb') as f:
            data = pickle.load(f)
        
        self.faqs = data['faqs']
        embeddings = data['embeddings']
        
        # Recreate FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.index.add(embeddings.astype('float32'))
    
    def retrieve(self, query, top_k=3):
        """Retrieve most relevant FAQs for a query"""
        self._ensure_ready()
        if self.index is None or len(self.faqs) == 0:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search index
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Get results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.faqs):
                faq = self.faqs[idx]
                results.append({
                    'question': faq['question'],
                    'answer': faq['answer'],
                    'confidence': float(scores[0][i]),
                    'category': faq.get('category', ''),
                    'tags': faq.get('tags', '')
                })
        
        return results
    
    def add_new_faq(self, question, answer, tags='', category=''):
        """Add new FAQ and update index"""
        self._ensure_ready()
        faq_id = self.db.add_faq(question, answer, tags, category)
        self._build_index()
        return faq_id