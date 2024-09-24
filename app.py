from flask import Flask, request, jsonify, render_template
import re
import random
from fuzzywuzzy import fuzz
from nltk.chat.util import Chat, reflections

# Define pairs of patterns and responses
pairs = [
    (r'.*rail madad.*', ['Rail Madad is an online platform provided by Indian Railways to help passengers register complaints and track their resolutions.']),
    (r'.*file a complaint.*', ['You can file a complaint by visiting the Rail Madad website or app, selecting the complaint type, filling in details, and submitting it.']),
    (r'.*status of my complaint.*', ['You can track your complaint status by entering your complaint ID on the Rail Madad platform.']),
    (r'.*upload (image|video).*', ['Yes, Rail Madad allows users to upload images and videos related to their complaint. This helps provide more clarity.']),
    (r'.*train delay|punctuality.*', ['Yes, complaints about train delays and punctuality issues can be filed on Rail Madad.']),
    (r'.*cleanliness.*', ['You can file complaints related to the cleanliness of coaches, toilets, and station premises.']),
    (r'.*staff behavior.*', ['Complaints about inappropriate or unprofessional staff behavior can be filed on Rail Madad.']),
    (r'.*medical assistance.*', ['You can request medical assistance in emergencies through Rail Madad.']),
    (r'.*', ['Sorry, I did not understand that. Can you please rephrase?'])
]

# Fuzzy matching threshold
FUZZY_THRESHOLD = 75

# Custom Chat class with fuzzy matching
class FuzzyChat(Chat):
    def __init__(self, pairs, reflections):
        super().__init__(pairs, reflections)
        self._pairs = [(re.compile(pattern, re.IGNORECASE), responses) for pattern, responses in pairs]

    def respond(self, user_input):
        user_input = user_input.lower()  # Convert user input to lowercase
        for pattern, responses in self._pairs:
            if pattern.search(user_input):
                return random.choice(responses)
        
        # Fuzzy matching fallback if no regex matches
        best_match = None
        best_score = 0
        for pattern, responses in self._pairs:
            score = fuzz.ratio(user_input, pattern.pattern)
            if score > FUZZY_THRESHOLD and score > best_score:
                best_match = responses
                best_score = score
        
        if best_match:
            return random.choice(best_match)
        
        # Default response if no match is found
        return random.choice([response for pattern, responses in self._pairs for response in responses])

# Create the chatbot with fuzzy matching
chatbot = FuzzyChat(pairs, reflections)

# Function to get response from the chatbot
def get_response(user_message):
    return chatbot.respond(user_message)

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Make sure index.html is in a 'templates' folder

# Route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')  # Get the message from the request
    response = get_response(user_message)  # Get chatbot response
    return jsonify({'response': response})  # Return the response as JSON

if __name__ == "__main__":
    app.run(debug=True)
//sumit
