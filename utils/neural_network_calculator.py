import numpy as np
import math
import random

def sigmoid(x):
    """Sigmoid activation function"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def softmax(x):
    """Softmax activation function"""
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)

class NeuralNetworkCalculator:
    """
    Class untuk menghitung proses neural network secara detail
    termasuk forward propagation, backpropagation, dan metrik evaluasi
    """
    
    def __init__(self):
        # Initialize weights dan bias (simulasi untuk demo)
        np.random.seed(42)  # Untuk konsistensi hasil
        
        # Weights untuk hidden layer (5 input -> 3 hidden)
        self.w1 = np.random.uniform(-0.5, 0.5, (5, 3))
        self.b1 = np.random.uniform(-0.3, 0.3, 3)
        
        # Weights untuk output layer (3 hidden -> 5 output)
        self.w2 = np.random.uniform(-0.5, 0.5, (3, 5))
        self.b2 = np.random.uniform(-0.3, 0.3, 5)
        
        # Learning rate
        self.learning_rate = 0.01
        
        # Simulasi confusion matrix untuk demo
        self.confusion_matrix = np.array([
            [85, 3, 2, 0, 0],    # Class 1 (Enamel Damage Early)
            [2, 78, 8, 2, 0],    # Class 2 (Enamel Decay Moderate) 
            [1, 5, 82, 6, 1],    # Class 3 (Dentin Decay)
            [0, 1, 4, 88, 2],    # Class 4 (Pulp Involvement)
            [0, 0, 1, 3, 91]     # Class 5 (Abscess Formation)
        ])
    
    def forward_propagation(self, input_features):
        """
        Melakukan forward propagation dan mengembalikan perhitungan detail
        """
        # Convert input ke numpy array
        x = np.array(input_features, dtype=float)
        
        # Hidden layer calculation
        hidden_net = np.dot(x, self.w1) + self.b1
        hidden_output = sigmoid(hidden_net)
        
        # Output layer calculation
        output_net = np.dot(hidden_output, self.w2) + self.b2
        output_probabilities = softmax(output_net)
        
        # Predicted class
        predicted_class = np.argmax(output_probabilities)
        confidence = output_probabilities[predicted_class] * 100
        
        return {
            'input_features': x,
            'hidden_net': hidden_net,
            'hidden_output': hidden_output,
            'output_net': output_net,
            'probabilities': output_probabilities * 100,  # Convert to percentage
            'predicted_class': predicted_class,
            'confidence': confidence
        }
    
    def backpropagation(self, input_features, target_class, forward_results):
        """
        Menghitung backpropagation step by step
        """
        # Create target vector (one-hot encoding)
        target_vector = np.zeros(5)
        target_vector[target_class] = 1
        
        # Output error
        output_error = target_vector - (forward_results['probabilities'] / 100)
        
        # Output layer gradients (using softmax derivative)
        output_gradients = output_error * (forward_results['probabilities'] / 100) * (1 - forward_results['probabilities'] / 100)
        
        # Hidden layer error (backpropagate error)
        hidden_error = np.dot(output_gradients, self.w2.T)
        
        # Hidden layer gradients
        hidden_gradients = hidden_error * forward_results['hidden_output'] * (1 - forward_results['hidden_output'])
        
        return {
            'target_vector': target_vector,
            'output_error': output_error,
            'output_gradients': output_gradients,
            'hidden_error': hidden_error,
            'hidden_gradients': hidden_gradients,
            'learning_rate': self.learning_rate
        }
    
    def calculate_metrics(self):
        """
        Menghitung metrik evaluasi dari confusion matrix
        """
        cm = self.confusion_matrix
        n_classes = cm.shape[0]
        
        # Calculate TP, TN, FP, FN for each class
        tp = np.diag(cm)
        fp = np.sum(cm, axis=0) - tp
        fn = np.sum(cm, axis=1) - tp
        tn = np.sum(cm) - (tp + fp + fn)
        
        # Calculate metrics for each class
        precision_per_class = tp / (tp + fp + 1e-8)
        recall_per_class = tp / (tp + fn + 1e-8)
        f1_per_class = 2 * (precision_per_class * recall_per_class) / (precision_per_class + recall_per_class + 1e-8)
        
        # Overall metrics
        accuracy = np.sum(tp) / np.sum(cm) * 100
        precision = np.mean(precision_per_class) * 100
        recall = np.mean(recall_per_class) * 100
        f1_score = np.mean(f1_per_class) * 100
        
        return {
            'confusion_matrix': cm.tolist(),
            'tp': tp.tolist(),
            'tn': tn.tolist(),
            'fp': fp.tolist(),
            'fn': fn.tolist(),
            'accuracy': round(accuracy, 2),
            'precision': round(precision, 2),
            'recall': round(recall, 2),
            'f1_score': round(f1_score, 2),
            'precision_per_class': [round(p * 100, 2) for p in precision_per_class],
            'recall_per_class': [round(r * 100, 2) for r in recall_per_class],
            'f1_per_class': [round(f * 100, 2) for f in f1_per_class]
        }
    
    def get_weights_formatted(self):
        """
        Mengembalikan weights yang sudah diformat untuk tampilan
        """
        return {
            'hidden': [[round(w, 3) for w in row] for row in self.w1.tolist()],
            'hidden_bias': [round(b, 3) for b in self.b1.tolist()],
            'output': [[round(w, 3) for w in row] for row in self.w2.tolist()],
            'output_bias': [round(b, 3) for b in self.b2.tolist()]
        }
    
    def format_calculations(self, forward_results):
        """
        Format hasil perhitungan untuk tampilan yang lebih baik
        """
        return {
            'hidden_net': [round(x, 4) for x in forward_results['hidden_net']],
            'hidden_output': [round(x, 4) for x in forward_results['hidden_output']],
            'output_net': [round(x, 4) for x in forward_results['output_net']],
            'probabilities': [round(x, 2) for x in forward_results['probabilities']]
        }

def get_condition_names(language='en'):
    """
    Mengembalikan nama kondisi dalam bahasa yang sesuai
    """
    if language == 'id':
        return [
            "Kerusakan Enamel (Awal)",
            "Kerusakan Enamel (Sedang)", 
            "Kerusakan Dentin",
            "Keterlibatan Pulpa",
            "Pembentukan Abses"
        ]
    else:
        return [
            "Enamel Damage (Early)",
            "Enamel Decay (Moderate)",
            "Dentin Decay", 
            "Pulp Involvement",
            "Abscess Formation"
        ]