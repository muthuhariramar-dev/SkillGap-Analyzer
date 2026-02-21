from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)

# Enable CORS for frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Question database for different courses and difficulties
question_bank = {
    'data-structures': {
        'low': [
            {
                'id': 1,
                'question': "What is the time complexity of binary search?",
                'options': ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                'correct': 1,
                'explanation': "Binary search divides search space in half with each iteration, resulting in O(log n) time complexity."
            },
            {
                'id': 2,
                'question': "Which data structure uses LIFO principle?",
                'options': ["Queue", "Stack", "Array", "Linked List"],
                'correct': 1,
                'explanation': "Stack follows Last In First Out (LIFO) principle."
            },
            {
                'id': 3,
                'question': "What is the maximum number of nodes in a binary tree of height h?",
                'options': ["2^h - 1", "2^h", "2^(h+1) - 1", "h^2"],
                'correct': 2,
                'explanation': "A binary tree of height h can have maximum 2^(h+1) - 1 nodes."
            },
            {
                'id': 4,
                'question': "Which sorting algorithm has the best average case time complexity?",
                'options': ["Bubble Sort", "Selection Sort", "Merge Sort", "Insertion Sort"],
                'correct': 2,
                'explanation': "Merge Sort has O(n log n) average case time complexity."
            },
            {
                'id': 5,
                'question': "What is a hash collision?",
                'options': ["When two keys have same hash", "When hash function fails", "When table is full", "When key is null"],
                'correct': 0,
                'explanation': "Hash collision occurs when two different keys produce the same hash value."
            },
            {
                'id': 6,
                'question': "Which traversal visits nodes in order: Left, Root, Right?",
                'options': ["Preorder", "Inorder", "Postorder", "Level order"],
                'correct': 1,
                'explanation': "Inorder traversal visits Left subtree, Root, then Right subtree."
            },
            {
                'id': 7,
                'question': "What is the space complexity of recursive factorial function?",
                'options': ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                'correct': 1,
                'explanation': "Recursive factorial uses O(n) stack space due to n recursive calls."
            },
            {
                'id': 8,
                'question': "Which data structure is best for implementing a priority queue?",
                'options': ["Array", "Linked List", "Heap", "Stack"],
                'correct': 2,
                'explanation': "Heap provides efficient O(log n) insertion and deletion for priority queue."
            },
            {
                'id': 9,
                'question': "What is the worst case time complexity of quicksort?",
                'options': ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
                'correct': 1,
                'explanation': "Quicksort worst case occurs when pivot is always smallest or largest element."
            },
            {
                'id': 10,
                'question': "How many edges does a complete graph with n vertices have?",
                'options': ["n", "n-1", "n(n-1)/2", "n²"],
                'correct': 2,
                'explanation': "Complete graph has n(n-1)/2 edges as each vertex connects to all others."
            }
        ],
        'medium': [
            {
                'id': 11,
                'question': "What is the time complexity of Dijkstra's algorithm with binary heap?",
                'options': ["O(V²)", "O(E log V)", "O(V log V)", "O(E + V log V)"],
                'correct': 3,
                'explanation': "With binary heap, Dijkstra's algorithm runs in O(E + V log V)."
            },
            {
                'id': 12,
                'question': "What is the height of a balanced BST with n nodes?",
                'options': ["O(log n)", "O(n)", "O(n²)", "O(√n)"],
                'correct': 0,
                'explanation': "Balanced BST maintains height O(log n) for n nodes."
            },
            {
                'id': 13,
                'question': "Which algorithm finds shortest path in weighted graph with negative edges?",
                'options': ["Dijkstra", "Bellman-Ford", "Prim's", "Kruskal's"],
                'correct': 1,
                'explanation': "Bellman-Ford handles negative weight edges, Dijkstra doesn't."
            },
            {
                'id': 14,
                'question': "What is the amortized time complexity of dynamic array insertion?",
                'options': ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                'correct': 0,
                'explanation': "Dynamic array has O(1) amortized insertion despite occasional O(n) resizing."
            },
            {
                'id': 15,
                'question': "Which tree structure guarantees O(log n) worst case operations?",
                'options': ["BST", "AVL Tree", "Red-Black Tree", "Both B and C"],
                'correct': 3,
                'explanation': "Both AVL and Red-Black trees are self-balancing with O(log n) worst case."
            },
            {
                'id': 16,
                'question': "What is the space complexity of Floyd-Warshall algorithm?",
                'options': ["O(V)", "O(V²)", "O(V³)", "O(E)"],
                'correct': 1,
                'explanation': "Floyd-Warshall uses O(V²) space for distance matrix."
            },
            {
                'id': 17,
                'question': "Which data structure supports range minimum queries efficiently?",
                'options': ["Segment Tree", "Binary Tree", "Linked List", "Hash Table"],
                'correct': 0,
                'explanation': "Segment Tree provides O(log n) range minimum queries."
            },
            {
                'id': 18,
                'question': "What is the time complexity of building a heap from n elements?",
                'options': ["O(n log n)", "O(n)", "O(log n)", "O(n²)"],
                'correct': 1,
                'explanation': "Heap can be built in O(n) time using heapify bottom-up."
            },
            {
                'id': 19,
                'question': "Which algorithm solves all-pairs shortest path problem?",
                'options': ["Dijkstra", "Bellman-Ford", "Floyd-Warshall", "Prim's"],
                'correct': 2,
                'explanation': "Floyd-Warshall finds shortest paths between all vertex pairs."
            },
            {
                'id': 20,
                'question': "What is the maximum number of comparisons in comparison sort?",
                'options': ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
                'correct': 1,
                'explanation': "Comparison sorts require at least O(n log n) comparisons in worst case."
            }
        ],
        'high': [
            {
                'id': 21,
                'question': "Prove that any comparison-based sorting algorithm requires Ω(n log n) comparisons",
                'options': ["Information theory", "Decision tree model", "Both A and B", "Neither"],
                'correct': 2,
                'explanation': "Decision tree model and information theory both prove Ω(n log n) lower bound."
            },
            {
                'id': 22,
                'question': "What is the time complexity of suffix array construction?",
                'options': ["O(n log n)", "O(n)", "O(n²)", "O(log n)"],
                'correct': 0,
                'explanation': "Efficient suffix array construction takes O(n log n) time."
            },
            {
                'id': 23,
                'question': "Which data structure supports both range sum and update queries in O(log n)?",
                'options': ["Fenwick Tree", "Segment Tree", "Both", "Neither"],
                'correct': 2,
                'explanation': "Both Fenwick Tree and Segment Tree support O(log n) range operations."
            },
            {
                'id': 24,
                'question': "What is the amortized time complexity of splay tree operations?",
                'options': ["O(log n)", "O(n)", "O(1)", "O(n²)"],
                'correct': 0,
                'explanation': "Splay tree has O(log n) amortized time complexity."
            },
            {
                'id': 25,
                'question': "Which algorithm finds maximum flow in a network?",
                'options': ["Ford-Fulkerson", "Edmonds-Karp", "Both", "Neither"],
                'correct': 2,
                'explanation': "Both Ford-Fulkerson and Edmonds-Karp can find maximum flow."
            },
            {
                'id': 26,
                'question': "What is the time complexity of KMP pattern matching algorithm?",
                'options': ["O(n+m)", "O(nm)", "O(n²)", "O(m²)"],
                'correct': 0,
                'explanation': "KMP algorithm runs in O(n+m) where n is text, m is pattern length."
            },
            {
                'id': 27,
                'question': "Which structure supports predecessor queries in O(log n) time?",
                'options': ["BST", "AVL Tree", "Skip List", "All of above"],
                'correct': 3,
                'explanation': "All these structures support O(log n) predecessor queries."
            },
            {
                'id': 28,
                'question': "What is the space complexity of suffix tree?",
                'options': ["O(n)", "O(n log n)", "O(n²)", "O(2^n)"],
                'correct': 0,
                'explanation': "Suffix tree requires O(n) space for string of length n."
            },
            {
                'id': 29,
                'question': "Which algorithm solves traveling salesman problem exactly?",
                'options': ["Dynamic Programming", "Greedy", "Dijkstra", "Prim's"],
                'correct': 0,
                'explanation': "Dynamic programming can solve TSP exactly in O(n²2^n) time."
            },
            {
                'id': 30,
                'question': "What is the time complexity of LCA query in binary lifting?",
                'options': ["O(log n)", "O(n)", "O(1)", "O(n log n)"],
                'correct': 0,
                'explanation': "Binary lifting answers LCA queries in O(log n) time."
            }
        ]
    },
    'web-development': {
        'low': [
            {
                'id': 31,
                'question': "Which HTML tag is used for main content?",
                'options': ["<main>", "<content>", "<body>", "<section>"],
                'correct': 0,
                'explanation': "<main> tag specifies the main content of a document."
            },
            {
                'id': 32,
                'question': "What does CSS stand for?",
                'options': ["Computer Style Sheets", "Creative Style Sheets", "Cascading Style Sheets", "Colorful Style Sheets"],
                'correct': 2,
                'explanation': "CSS stands for Cascading Style Sheets."
            },
            {
                'id': 33,
                'question': "Which method is used to select an element by ID in JavaScript?",
                'options': ["getElementByClass()", "getElementById()", "querySelector()", "Both B and C"],
                'correct': 3,
                'explanation': "Both getElementById() and querySelector('#id') can select by ID."
            },
            {
                'id': 34,
                'question': "What is the default display value of div element?",
                'options': ["inline", "block", "inline-block", "flex"],
                'correct': 1,
                'explanation': "div elements have block display by default."
            },
            {
                'id': 35,
                'question': "Which HTTP status code indicates 'Not Found'?",
                'options': ["200", "301", "404", "500"],
                'correct': 2,
                'explanation': "404 status code indicates resource not found."
            },
            {
                'id': 36,
                'question': "What is the purpose of semantic HTML?",
                'options': ["Styling", "Meaning and structure", "Animation", "Database"],
                'correct': 1,
                'explanation': "Semantic HTML provides meaning and structure to content."
            },
            {
                'id': 37,
                'question': "Which property changes text color in CSS?",
                'options': ["text-color", "color", "font-color", "text-style"],
                'correct': 1,
                'explanation': "color property sets the text color in CSS."
            },
            {
                'id': 38,
                'question': "What is the correct way to link external CSS?",
                'options': ["<style>", "<link>", "<css>", "<stylesheet>"],
                'correct': 1,
                'explanation': "<link> tag is used to link external CSS files."
            },
            {
                'id': 39,
                'question': "Which JavaScript keyword declares a constant?",
                'options': ["var", "let", "const", "constant"],
                'correct': 2,
                'explanation': "const keyword declares a constant variable."
            },
            {
                'id': 40,
                'question': "What does DOM stand for?",
                'options': ["Document Object Model", "Data Object Management", "Dynamic Object Model", "Document Order Model"],
                'correct': 0,
                'explanation': "DOM stands for Document Object Model."
            }
        ],
        'medium': [
            {
                'id': 41,
                'question': "What is the purpose of CORS?",
                'options': ["Styling", "Security", "Database", "Animation"],
                'correct': 1,
                'explanation': "CORS (Cross-Origin Resource Sharing) manages security for cross-origin requests."
            },
            {
                'id': 42,
                'question': "Which method prevents default event behavior?",
                'options': ["stopPropagation()", "preventDefault()", "stopDefault()", "cancelEvent()"],
                'correct': 1,
                'explanation': "preventDefault() stops the default event behavior."
            },
            {
                'id': 43,
                'question': "What is the difference between == and === in JavaScript?",
                'options': ["No difference", "=== checks type", "== checks type", "Both check type"],
                'correct': 1,
                'explanation': "=== checks both value and type, == only checks value."
            },
            {
                'id': 44,
                'question': "Which CSS property creates flexbox layout?",
                'options': ["display: flex", "position: flex", "layout: flex", "flex: true"],
                'correct': 0,
                'explanation': "display: flex creates a flexbox layout."
            },
            {
                'id': 45,
                'question': "What is the purpose of localStorage?",
                'options': ["Server storage", "Client-side storage", "Database", "Cache"],
                'correct': 1,
                'explanation': "localStorage provides client-side storage for web applications."
            },
            {
                'id': 46,
                'question': "Which HTTP method is used for updating data?",
                'options': ["GET", "POST", "PUT", "DELETE"],
                'correct': 2,
                'explanation': "PUT method is typically used for updating existing resources."
            },
            {
                'id': 47,
                'question': "What is the purpose of async/await in JavaScript?",
                'options': ["Synchronous code", "Asynchronous code", "Error handling", "Loop control"],
                'correct': 1,
                'explanation': "async/await simplifies writing asynchronous code."
            },
            {
                'id': 48,
                'question': "Which CSS property centers flex items?",
                'options': ["align-items: center", "justify-content: center", "Both", "Neither"],
                'correct': 2,
                'explanation': "Both align-items and justify-content can center flex items in different directions."
            },
            {
                'id': 49,
                'question': "What is the purpose of REST API?",
                'options': ["Database management", "Web service communication", "Styling", "Animation"],
                'correct': 1,
                'explanation': "REST API enables communication between web services."
            },
            {
                'id': 50,
                'question': "Which event fires when page finishes loading?",
                'options': ["onload", "onready", "oncomplete", "onfinish"],
                'correct': 0,
                'explanation': "onload event fires when page finishes loading."
            }
        ],
        'high': [
            {
                'id': 51,
                'question': "What is the difference between microservices and monolithic architecture?",
                'options': ["No difference", "Deployment strategy", "Service separation", "Database type"],
                'correct': 2,
                'explanation': "Microservices separate functionality into independent services."
            },
            {
                'id': 52,
                'question': "How does virtual DOM improve performance?",
                'options': ["Direct manipulation", "Efficient updates", "More memory", "Faster rendering"],
                'correct': 1,
                'explanation': "Virtual DOM enables efficient updates by minimizing direct DOM manipulation."
            },
            {
                'id': 53,
                'question': "What is the purpose of WebSockets?",
                'options': ["HTTP requests", "Real-time communication", "File storage", "Styling"],
                'correct': 1,
                'explanation': "WebSockets enable real-time bidirectional communication."
            },
            {
                'id': 54,
                'question': "What is server-side rendering?",
                'options': ["Client rendering", "Server HTML generation", "Database queries", "API calls"],
                'correct': 1,
                'explanation': "SSR generates HTML on server before sending to client."
            },
            {
                'id': 55,
                'question': "What is the purpose of CDN?",
                'options': ["Database", "Content distribution", "Security", "Authentication"],
                'correct': 1,
                'explanation': "CDN distributes content globally for faster delivery."
            },
            {
                'id': 56,
                'question': "What is the difference between GraphQL and REST?",
                'options': ["No difference", "Query flexibility", "Database type", "Protocol"],
                'correct': 1,
                'explanation': "GraphQL allows flexible queries while REST has fixed endpoints."
            },
            {
                'id': 57,
                'question': "What is the purpose of service workers?",
                'options': ["Styling", "Offline functionality", "Database", "Routing"],
                'correct': 1,
                'explanation': "Service workers enable offline functionality and background sync."
            },
            {
                'id': 58,
                'question': "What is the purpose of JWT?",
                'options': ["Database", "Authentication", "Styling", "Animation"],
                'correct': 1,
                'explanation': "JWT (JSON Web Token) is used for authentication."
            },
            {
                'id': 59,
                'question': "What is the difference between SQL and NoSQL databases?",
                'options': ["No difference", "Schema flexibility", "Performance", "Security"],
                'correct': 1,
                'explanation': "NoSQL databases offer schema flexibility compared to rigid SQL schemas."
            },
            {
                'id': 60,
                'question': "What is the purpose of lazy loading?",
                'options': ["Security", "Performance optimization", "Database", "Styling"],
                'correct': 1,
                'explanation': "Lazy loading improves performance by loading resources on demand."
            }
        ]
    },
    'machine-learning': {
        'low': [
            {
                'id': 61,
                'question': "What is supervised learning?",
                'options': ["Learning without labels", "Learning with labeled data", "Unsupervised learning", "Reinforcement learning"],
                'correct': 1,
                'explanation': "Supervised learning uses labeled training data to learn patterns."
            },
            {
                'id': 62,
                'question': "What is overfitting in machine learning?",
                'options': ["Underfitting", "Perfect fit", "Too specific to training data", "Good generalization"],
                'correct': 2,
                'explanation': "Overfitting occurs when model learns training data too specifically."
            },
            {
                'id': 63,
                'question': "What is the purpose of train-test split?",
                'options': ["Speed", "Model evaluation", "Data storage", "Visualization"],
                'correct': 1,
                'explanation': "Train-test split evaluates model performance on unseen data."
            },
            {
                'id': 64,
                'question': "What is a feature in machine learning?",
                'options': ["Label", "Input variable", "Output", "Algorithm"],
                'correct': 1,
                'explanation': "Features are input variables used to make predictions."
            },
            {
                'id': 65,
                'question': "What is the purpose of cross-validation?",
                'options': ["Speed", "Robust evaluation", "Data cleaning", "Visualization"],
                'correct': 1,
                'explanation': "Cross-validation provides robust model evaluation."
            },
            {
                'id': 66,
                'question': "What is classification?",
                'options': ["Prediction", "Category prediction", "Regression", "Clustering"],
                'correct': 1,
                'explanation': "Classification predicts discrete categories or classes."
            },
            {
                'id': 67,
                'question': "What is the difference between regression and classification?",
                'options': ["No difference", "Continuous vs discrete", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Regression predicts continuous values, classification predicts discrete categories."
            },
            {
                'id': 68,
                'question': "What is the purpose of feature scaling?",
                'options': ["Speed", "Normalization", "Data storage", "Visualization"],
                'correct': 1,
                'explanation': "Feature scaling normalizes input features for better model performance."
            },
            {
                'id': 69,
                'question': "What is a confusion matrix?",
                'options': ["Error matrix", "Performance evaluation", "Data storage", "Algorithm"],
                'correct': 1,
                'explanation': "Confusion matrix evaluates classification performance."
            },
            {
                'id': 70,
                'question': "What is the purpose of regularization?",
                'options': ["Speed", "Prevent overfitting", "Data cleaning", "Visualization"],
                'correct': 1,
                'explanation': "Regularization prevents overfitting by adding penalty terms."
            }
        ],
        'medium': [
            {
                'id': 71,
                'question': "What is the difference between bagging and boosting?",
                'options': ["No difference", "Parallel vs sequential", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Bagging trains models in parallel, boosting trains sequentially."
            },
            {
                'id': 72,
                'question': "What is the purpose of gradient descent?",
                'options': ["Data cleaning", "Optimization", "Visualization", "Storage"],
                'correct': 1,
                'explanation': "Gradient descent optimizes model parameters by minimizing loss."
            },
            {
                'id': 73,
                'question': "What is the difference between precision and recall?",
                'options': ["No difference", "False positives vs false negatives", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Precision measures false positives, recall measures false negatives."
            },
            {
                'id': 74,
                'question': "What is the purpose of PCA?",
                'options': ["Classification", "Dimensionality reduction", "Clustering", "Regression"],
                'correct': 1,
                'explanation': "PCA reduces dimensionality while preserving variance."
            },
            {
                'id': 75,
                'question': "What is the difference between SVM and logistic regression?",
                'options': ["No difference", "Linear vs non-linear", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "SVM can handle non-linear boundaries, logistic regression is linear."
            },
            {
                'id': 76,
                'question': "What is the purpose of learning rate?",
                'options': ["Data cleaning", "Optimization speed", "Storage", "Visualization"],
                'correct': 1,
                'explanation': "Learning rate controls optimization step size."
            },
            {
                'id': 77,
                'question': "What is the difference between random forest and decision tree?",
                'options': ["No difference", "Single vs multiple trees", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Random forest uses multiple trees, decision tree uses one."
            },
            {
                'id': 78,
                'question': "What is the purpose of activation functions?",
                'options': ["Data storage", "Non-linearity", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Activation functions introduce non-linearity in neural networks."
            },
            {
                'id': 79,
                'question': "What is the difference between batch and stochastic gradient descent?",
                'options': ["No difference", "All vs one sample", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Batch uses all samples, stochastic uses one sample at a time."
            },
            {
                'id': 80,
                'question': "What is the purpose of early stopping?",
                'options': ["Speed", "Prevent overfitting", "Data cleaning", "Visualization"],
                'correct': 1,
                'explanation': "Early stopping prevents overfitting by stopping training early."
            }
        ],
        'high': [
            {
                'id': 81,
                'question': "What is the difference between CNN and RNN?",
                'options': ["No difference", "Spatial vs temporal", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "CNN processes spatial data, RNN processes sequential/temporal data."
            },
            {
                'id': 82,
                'question': "What is the purpose of attention mechanism?",
                'options': ["Speed", "Focus on important features", "Data storage", "Visualization"],
                'correct': 1,
                'explanation': "Attention mechanism focuses on important input features."
            },
            {
                'id': 83,
                'question': "What is the difference between GAN and VAE?",
                'options': ["No difference", "Adversarial vs variational", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "GAN uses adversarial training, VAE uses variational inference."
            },
            {
                'id': 84,
                'question': "What is the purpose of transfer learning?",
                'options': ["Speed", "Reuse pre-trained models", "Data cleaning", "Visualization"],
                'correct': 1,
                'explanation': "Transfer learning reuses pre-trained models for new tasks."
            },
            {
                'id': 85,
                'question': "What is the difference between BERT and GPT?",
                'options': ["No difference", "Bidirectional vs autoregressive", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "BERT is bidirectional, GPT is autoregressive."
            },
            {
                'id': 86,
                'question': "What is the purpose of dropout in neural networks?",
                'options': ["Speed", "Prevent overfitting", "Data cleaning", "Visualization"],
                'correct': 1,
                'explanation': "Dropout prevents overfitting by randomly dropping neurons."
            },
            {
                'id': 87,
                'question': "What is the difference between supervised and unsupervised learning?",
                'options': ["No difference", "Labeled vs unlabeled data", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Supervised uses labeled data, unsupervised uses unlabeled data."
            },
            {
                'id': 88,
                'question': "What is the purpose of backpropagation?",
                'options': ["Data cleaning", "Gradient calculation", "Visualization", "Storage"],
                'correct': 1,
                'explanation': "Backpropagation calculates gradients for neural network training."
            },
            {
                'id': 89,
                'question': "What is the difference between batch normalization and layer normalization?",
                'options': ["No difference", "Batch vs feature normalization", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Batch normalizes across batch, layer normalizes across features."
            },
            {
                'id': 90,
                'question': "What is the purpose of embedding layers?",
                'options': ["Data storage", "Dense representation", "Speed", "Accuracy"],
                'correct': 1,
                'explanation': "Embedding layers create dense representations of categorical data."
            }
        ]
    }
}

@app.route('/api/questions/<course>/<difficulty>', methods=['GET'])
def get_questions(course, difficulty):
    """Get 10 random questions for a course and difficulty"""
    
    # Validate course and difficulty
    if course not in question_bank:
        return jsonify({'error': 'Course not found'}), 404
    
    if difficulty not in question_bank[course]:
        return jsonify({'error': 'Difficulty level not found'}), 404
    
    # Get questions for course and difficulty
    questions = question_bank[course][difficulty]
    
    # Shuffle and select 10 random questions
    shuffled = questions.copy()
    random.shuffle(shuffled)
    selected_questions = shuffled[:10]
    
    # Add question numbers
    numbered_questions = []
    for i, q in enumerate(selected_questions):
        question_data = q.copy()
        question_data['questionNumber'] = i + 1
        numbered_questions.append(question_data)
    
    return jsonify({
        'course': course,
        'difficulty': difficulty,
        'totalQuestions': 10,
        'questions': numbered_questions
    })

@app.route('/api/questions/courses', methods=['GET'])
def get_courses():
    """Get all available courses"""
    courses = []
    for course_id in question_bank.keys():
        course_name = ' '.join(word.capitalize() for word in course_id.split('-'))
        courses.append({
            'id': course_id,
            'name': course_name
        })
    
    return jsonify({'courses': courses})

@app.route('/api/questions/submit/<course>/<difficulty>', methods=['POST'])
def submit_answers(course, difficulty):
    """Submit test answers and calculate score"""
    if course not in question_bank or difficulty not in question_bank[course]:
        return jsonify({'error': 'Questions not found'}), 404
    
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'error': 'Answers not provided'}), 400
    
    answers = data['answers']
    user_id = data.get('userId', 'anonymous')
    
    # Get correct questions
    questions = question_bank[course][difficulty]
    
    # Calculate score
    correct = 0
    results = []
    for answer in answers:
        question = next((q for q in questions if q['id'] == answer['questionId']), None)
        if question:
            is_correct = question['correct'] == answer['selectedOption']
            if is_correct:
                correct += 1
            
            result = {
                'questionId': answer['questionId'],
                'selectedOption': answer['selectedOption'],
                'correctOption': question['correct'],
                'isCorrect': is_correct,
                'explanation': question['explanation']
            }
            results.append(result)
    
    score = (correct / len(answers)) * 100
    
    return jsonify({
        'course': course,
        'difficulty': difficulty,
        'userId': user_id,
        'totalQuestions': len(answers),
        'correct': correct,
        'score': round(score),
        'results': results,
        'passed': score >= 70
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Skills Gap Analysis API Server',
        'endpoints': {
            'questions': '/api/questions/<course>/<difficulty>',
            'courses': '/api/questions/courses',
            'submit': '/api/questions/submit/<course>/<difficulty>'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
