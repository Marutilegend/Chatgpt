from flask import Flask, request, jsonify
from googletrans import Translator
import requests

app = Flask(__name__)
translator = Translator()

# Your Google Custom Search API key and Search Engine ID
GOOGLE_API_KEY = "AIzaSyBVMNlKzrA2pAZIH1uNNGk3QQwCxQ2nN1A"
SEARCH_ENGINE_ID = "10dbd8960b175409f"  # Your provided Search Engine ID

# Add a route for the homepage
@app.route('/')
def home():
    return "Welcome to the maruti Chatbot with Google Search and Language Support!"

# Add the chatbot functionality
@app.route('/chat', methods=['POST'])
def chat():
    # Get the message and language sent by the user
    data = request.json
    user_input = data.get('message')
    language = data.get('language', 'en')  # Default language is English if not provided

    if not user_input:
        return jsonify({"response": "Please provide a message."})

    # Check if the user is asking for information from Google
    if "search:" in user_input.lower():
        query = user_input.lower().replace("search:", "").strip()  # Extract the query
        response = google_search(query)
    else:
        # Simple chatbot responses in English
        if "hello" in user_input.lower():
            response = "Hi there! How can I help you today?"
        elif "bye" in user_input.lower():
            response = "Goodbye! Have a great day!"
        else:
            response = "I'm just a simple bot. Can you ask something else?"

    # Translate the response to the requested language
    if language != 'en':  # If the language is not English, translate
        try:
            translated_response = translator.translate(response, dest=language).text
        except Exception as e:
            return jsonify({"response": f"Error translating response: {str(e)}"})
    else:
        translated_response = response

    # Return the response as JSON
    return jsonify({"response": translated_response})

def google_search(query):
    """Perform a Google search using the Custom Search JSON API."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    try:
        response = requests.get(url)
        results = response.json()
        # Extract top search result
        if "items" in results:
            top_result = results["items"][0]
            title = top_result["title"]
            link = top_result["link"]
            snippet = top_result.get("snippet", "No description available.")
            return f"{title}\n{snippet}\nMore info: {link}"
        else:
            return "No results found for your query."
    except Exception as e:
        return f"Error fetching results from Google: {str(e)}"

if __name__ == '__main__':
    # Make the app accessible on the local network
    app.run(debug=True, host='192.0.0.4')
