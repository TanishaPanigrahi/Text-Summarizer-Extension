from flask_cors import CORS
from flask import Flask, request, jsonify
from nltk import sent_tokenize, word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer
import numpy as np
import nltk

app = Flask(__name__)
CORS(app) 

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    return ' '.join(lemmatized_words)

def calculate_similarity(sentence1, sentence2, freq_dist, stop_words):
    words1 = [word.lower() for word in word_tokenize(sentence1) if word.isalnum() and word.lower() not in stop_words]
    words2 = [word.lower() for word in word_tokenize(sentence2) if word.isalnum() and word.lower() not in stop_words]

    unique_words = set(words1 + words2)

    vector1 = [freq_dist[word] for word in unique_words if word in words1]
    vector2 = [freq_dist[word] for word in unique_words if word in words2]

    while len(vector1) < len(vector2):
        vector1.append(0)

    while len(vector2) < len(vector1):
        vector2.append(0)

    similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    
    return similarity

def apply_textrank(sim_matrix, damping_factor=0.85, max_iter=100, tol=1e-4):
    num_sentences = len(sim_matrix)
    scores = np.ones(num_sentences) / num_sentences
    
    for _ in range(max_iter):
        prev_scores = np.copy(scores)
        
        for i in range(num_sentences):
            scores[i] = (1 - damping_factor) + damping_factor * np.sum(sim_matrix[i] * scores / np.sum(sim_matrix, axis=1))
        
        if np.sum(np.abs(scores - prev_scores)) < tol:
            break
    
    return scores

def calculate_similarity_matrix(sentences, freq_dist, stop_words):
    num_sentences = len(sentences)
    sim_matrix = np.zeros((num_sentences, num_sentences))

    for i in range(num_sentences):
        for j in range(i, num_sentences):
            similarity = calculate_similarity(sentences[i], sentences[j], freq_dist, stop_words)
            sim_matrix[i][j] = similarity
            sim_matrix[j][i] = similarity

    return sim_matrix

def textrank_summarizer(text, num_sentences=3):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    freq_dist = FreqDist(words)
    sim_matrix = calculate_similarity_matrix(sentences, freq_dist, stop_words)
    scores = apply_textrank(sim_matrix)

    top_sentences = [sentences[i] for i in sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)[:num_sentences]]
    summary = TreebankWordDetokenizer().detokenize(top_sentences)
    
    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text_to_summarize = data.get('text', '')

    # Perform text summarization using NLTK logic
    summarized_text = textrank_summarizer(text_to_summarize)

    return jsonify({'summary': summarized_text})

if __name__ == '__main__':
    app.run(debug=True)
