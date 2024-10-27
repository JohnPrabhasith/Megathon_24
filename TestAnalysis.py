import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import csv
from datetime import datetime, timedelta
import random
from functions.concern_classifier import concern_classifier
from functions.intensity_scorer import intensity_scorer
from functions.keyword_extractor import keyword_extractor
from functions.polarity_finder import polarity_finder
from functions.timeline_analyzer import timeline_analyzer

def generate_test_dataset(num_samples=20):
    """Generate synthetic mental health entries for testing"""
    
    # Define sample texts and their ground truth labels
    sample_texts = [
        {
            'text': "I've been feeling really anxious lately, can't stop worrying about everything",
            'category': 'Anxiety',
            'intensity': 7,
            'polarity': 'negative',
            'keywords': 'feeling anxious, worrying'
        },
        {
            'text': "Having trouble sleeping, tossing and turning all night",
            'category': 'Insomnia',
            'intensity': 6,
            'polarity': 'negative',
            'keywords': 'trouble sleeping, tossing and turning'
        },
        {
            'text': "Feeling much better today, meditation really helps",
            'category': 'Positive Outlook',
            'intensity': 3,
            'polarity': 'positive',
            'keywords': 'feeling better, meditation helps'
        },
        # Add more base samples to create variations from
    ]
    
    entries = []
    dates = []
    base_date = datetime.now() - timedelta(days=num_samples)
    
    for i in range(num_samples):
        # Select and modify a base sample
        base_sample = random.choice(sample_texts)
        
        # Create variations in text while maintaining semantic meaning
        variations = {
            'Anxiety': [
                "Feeling very anxious about upcoming events",
                "My anxiety is getting worse lately",
                "Can't shake this worried feeling",
            ],
            'Insomnia': [
                "Another sleepless night",
                "Barely got any sleep last night",
                "Sleep problems are getting worse",
            ],
            'Positive Outlook': [
                "Things are looking up",
                "Feeling more optimistic today",
                "Making progress with my mental health",
            ],
        }
        
        # Generate entry
        category = base_sample['category']
        text = random.choice(variations.get(category, [base_sample['text']]))
        
        # Add some random variation to intensity while keeping it realistic
        intensity = max(1, min(10, base_sample['intensity'] + random.randint(-2, 2)))
        
        entry = {
            'Date': base_date + timedelta(days=i),
            'Text': text,
            'True_Category': category,
            'True_Intensity': intensity,
            'True_Polarity': base_sample['polarity'],
            'True_Keywords': base_sample['keywords']
        }
        entries.append(entry)
    
    return pd.DataFrame(entries)

def evaluate_pipeline(dataset):
    """Evaluate the entire mental health analysis pipeline"""
    
    results = {
        'polarity_accuracy': [],
        'classification_accuracy': [],
        'intensity_mae': [],
        'keyword_similarity': [],
        'timeline_accuracy': []
    }
    i=0
    # Process each entry through the pipeline
    processed_entries = []
    for idx, row in dataset.iterrows():
        print(i)
        i+=1
        reference_entry = {
            'Category': row['True_Category'],
            'Intensity': row['True_Intensity'],
            'Polarity': row['True_Polarity'],
            'Extracted Concern': row['True_Keywords']
        }
        
        # Run through each component
        pred_category = concern_classifier(row['Text'], reference_entry, 
                                        ['Anxiety', 'Depression', 'Stress', 'Insomnia', 
                                         'Eating Disorder', 'Health Anxiety', 'Positive Outlook'])
        pred_intensity = intensity_scorer(row['Text'], reference_entry)
        pred_keywords = keyword_extractor(row['Text'], reference_entry)
        pred_polarity = polarity_finder(row['Text'], reference_entry)
        
        processed_entries.append({
            'date': row['Date'],
            'categories': pred_category,
            'intensities': pred_intensity,
            'polarity': pred_polarity,
            'keywords': pred_keywords
        })
        
        # Calculate metrics
        results['polarity_accuracy'].append(1 if pred_polarity == row['True_Polarity'].lower() else 0)
        results['classification_accuracy'].append(1 if pred_category == row['True_Category'] else 0)
        results['intensity_mae'].append(abs(pred_intensity - row['True_Intensity']))
        
        # Simple keyword similarity score (Jaccard similarity)
        pred_kw_set = set(pred_keywords.lower().split(', '))
        true_kw_set = set(row['True_Keywords'].lower().split(', '))
        similarity = len(pred_kw_set.intersection(true_kw_set)) / len(pred_kw_set.union(true_kw_set))
        results['keyword_similarity'].append(similarity)
    
    # Timeline analysis evaluation
    timeline_shifts = timeline_analyzer(processed_entries)
    
    # Calculate aggregate metrics
    evaluation_results = {
        'Polarity Detection Accuracy': np.mean(results['polarity_accuracy']),
        'Classification Precision': np.mean(results['classification_accuracy']),
        'Intensity Scoring MAE': np.mean(results['intensity_mae']),
        'Keyword Extraction Similarity': np.mean(results['keyword_similarity']),
        'Timeline Analysis Coverage': len(timeline_shifts) / len(dataset),
        'End-to-End Pipeline Success Rate': np.mean([
            np.mean(results['polarity_accuracy']),
            np.mean(results['classification_accuracy']),
            1 - (np.mean(results['intensity_mae']) / 10),  # Normalize to 0-1 scale
            np.mean(results['keyword_similarity'])
        ])
    }
    
    return evaluation_results, processed_entries, timeline_shifts

def run_evaluation(num_samples=75, output_file='mental_health_data.csv'):
    """Run the complete evaluation pipeline and save results"""
    
    # Generate dataset
    print("Generating synthetic dataset...")
    dataset = generate_test_dataset(num_samples)
    
    # Save raw dataset
    dataset.to_csv(output_file, index=False)
    print(f"Dataset saved to {output_file}")
    
    # Run evaluation
    print("\nEvaluating pipeline...")
    eval_results, processed_entries, timeline_shifts = evaluate_pipeline(dataset)
    
    # Save evaluation results
    results_file = 'evaluation_results.csv'
    with open(results_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Score'])
        for metric, score in eval_results.items():
            writer.writerow([metric, f"{score:.4f}"])
    
    print("\nEvaluation Results:")
    for metric, score in eval_results.items():
        print(f"{metric}: {score:.4f}")
    
    return dataset, eval_results, timeline_shifts

if __name__ == "__main__":
    dataset, results, timeline = run_evaluation()