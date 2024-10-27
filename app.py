# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from config import MONGODB_URI, CONCERN_CATEGORIES
from functions.polarity_finder import polarity_finder
from functions.keyword_extractor import keyword_extractor
from functions.concern_classifier import concern_classifier
from functions.intensity_scorer import intensity_scorer
from functions.timeline_analyzer import timeline_analyzer
import logging
from logging.config import dictConfig
from config import LOG_CONFIG

# Initialize logging
dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB setup with error handling
try:
    client = MongoClient(MONGODB_URI)
    db = client['analysis']
    collection = db['mental_health_db']
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

class MentalHealthAnalyzer:
    def __init__(self):
        try:
            self.reference_data = self._load_reference_dataset()
            self.vectorizer = TfidfVectorizer(strip_accents='unicode', lowercase=True)
            if not self.reference_data.empty:
                self.reference_vectors = self.vectorizer.fit_transform(self.reference_data['User Input'])
            else:
                raise ValueError("Reference dataset is empty")
        except Exception as e:
            logger.error(f"Failed to initialize MentalHealthAnalyzer: {str(e)}")
            raise

    def _load_reference_dataset(self):
        try:
            df = pd.read_csv('dataset.csv')
            if 'User Input' not in df.columns:
                raise ValueError("Required column 'User Input' not found in dataset")
            return df
        except Exception as e:
            logger.error(f"Failed to load reference dataset: {str(e)}")
            raise

    def find_most_similar_entry(self, input_text):
        """Find the most similar entry in the reference dataset using cosine similarity"""
        try:
            input_vector = self.vectorizer.transform([input_text])
            similarities = cosine_similarity(input_vector, self.reference_vectors)
            most_similar_idx = similarities.argmax()
            similarity_score = similarities[0][most_similar_idx]
            
            # Add a threshold for minimum similarity
            if similarity_score < 0.2:  # Adjust threshold as needed
                logger.warning(f"Low similarity score: {similarity_score}")
                
            return self.reference_data.iloc[most_similar_idx]
        except Exception as e:
            logger.error(f"Error in finding similar entry: {str(e)}")
            raise

# Initialize analyzer with error handling
try:
    analyzer = MentalHealthAnalyzer()
except Exception as e:
    logger.critical(f"Failed to initialize application: {str(e)}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])  # Added missing route decorator and methods
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        text = data.get('text')
        if not text or not isinstance(text, str):
            return jsonify({'error': 'Invalid or missing text field'}), 400

        # Find most similar entry in reference dataset
        similar_entry = analyzer.find_most_similar_entry(text)
        
        # Perform NLP analysis
        result = {
            'text': text,
            'timestamp': datetime.utcnow().isoformat(),  # Use UTC time
            'polarity': polarity_finder(text, similar_entry),
            'keywords': keyword_extractor(text, similar_entry),
            'categories': concern_classifier(text, similar_entry, CONCERN_CATEGORIES),
            'intensities': intensity_scorer(text, similar_entry)
        }

        # Retrieve existing entries from MongoDB and add timeline analysis
        try:
            existing_entries = list(collection.find(
                {}, 
                {'_id': 0}
            ).sort('timestamp', -1).limit(100))  # Limit to recent entries
            timeline_shifts = timeline_analyzer(existing_entries + [result])
            result['timeline_shifts'] = timeline_shifts
        except Exception as e:
            logger.error(f"Error retrieving timeline data: {str(e)}")
            result['timeline_shifts'] = []

        # Save result to MongoDB
        try:
            insert_result = collection.insert_one(result)
            result['_id'] = str(insert_result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {str(e)}")
            return jsonify({'error': 'Database error'}), 500

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # Disabled debug mode for production
# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from config import MONGODB_URI, CONCERN_CATEGORIES
from functions.polarity_finder import polarity_finder
from functions.keyword_extractor import keyword_extractor
from functions.concern_classifier import concern_classifier
from functions.intensity_scorer import intensity_scorer
from functions.timeline_analyzer import timeline_analyzer
import logging
from logging.config import dictConfig
from config import LOG_CONFIG

# Initialize logging
dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB setup with error handling
try:
    client = MongoClient(MONGODB_URI)
    db = client['analysis']
    collection = db['mental_health_db']
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

class MentalHealthAnalyzer:
    def __init__(self):
        try:
            self.reference_data = self._load_reference_dataset()
            self.vectorizer = TfidfVectorizer(strip_accents='unicode', lowercase=True)
            if not self.reference_data.empty:
                self.reference_vectors = self.vectorizer.fit_transform(self.reference_data['User Input'])
            else:
                raise ValueError("Reference dataset is empty")
        except Exception as e:
            logger.error(f"Failed to initialize MentalHealthAnalyzer: {str(e)}")
            raise

    def _load_reference_dataset(self):
        try:
            df = pd.read_csv('dataset.csv')
            if 'User Input' not in df.columns:
                raise ValueError("Required column 'User Input' not found in dataset")
            return df
        except Exception as e:
            logger.error(f"Failed to load reference dataset: {str(e)}")
            raise

    def find_most_similar_entry(self, input_text):
        """Find the most similar entry in the reference dataset using cosine similarity"""
        try:
            input_vector = self.vectorizer.transform([input_text])
            similarities = cosine_similarity(input_vector, self.reference_vectors)
            most_similar_idx = similarities.argmax()
            similarity_score = similarities[0][most_similar_idx]
            
            # Add a threshold for minimum similarity
            if similarity_score < 0.2:  # Adjust threshold as needed
                logger.warning(f"Low similarity score: {similarity_score}")
                
            return self.reference_data.iloc[most_similar_idx]
        except Exception as e:
            logger.error(f"Error in finding similar entry: {str(e)}")
            raise

# Initialize analyzer with error handling
try:
    analyzer = MentalHealthAnalyzer()
except Exception as e:
    logger.critical(f"Failed to initialize application: {str(e)}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])  # Added missing route decorator and methods
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        text = data.get('text')
        if not text or not isinstance(text, str):
            return jsonify({'error': 'Invalid or missing text field'}), 400

        # Find most similar entry in reference dataset
        similar_entry = analyzer.find_most_similar_entry(text)
        
        # Perform NLP analysis
        result = {
            'text': text,
            'timestamp': datetime.utcnow().isoformat(),  # Use UTC time
            'polarity': polarity_finder(text, similar_entry),
            'keywords': keyword_extractor(text, similar_entry),
            'categories': concern_classifier(text, similar_entry, CONCERN_CATEGORIES),
            'intensities': intensity_scorer(text, similar_entry)
        }

        # Retrieve existing entries from MongoDB and add timeline analysis
        try:
            existing_entries = list(collection.find(
                {}, 
                {'_id': 0}
            ).sort('timestamp', -1).limit(100))  # Limit to recent entries
            timeline_shifts = timeline_analyzer(existing_entries + [result])
            result['timeline_shifts'] = timeline_shifts
        except Exception as e:
            logger.error(f"Error retrieving timeline data: {str(e)}")
            result['timeline_shifts'] = []

        # Save result to MongoDB
        try:
            insert_result = collection.insert_one(result)
            result['_id'] = str(insert_result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {str(e)}")
            return jsonify({'error': 'Database error'}), 500

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # Disabled debug mode for production