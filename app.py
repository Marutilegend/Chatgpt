from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    # Get the message sent by the user
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"response": "Please provide a message."})
    
    # Simple chatbot responses
    if "hello" in user_input.lower():
        response = "Hi there! How can I help you today?"
    elif "bye" in user_input.lower():
        response = "Goodbye! Have a great day!"
    else:
        response = "I'm just a simple bot. Can you ask something else?"
    
    # Return the response as JSON
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)