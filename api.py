from flask import Flask, request, jsonify
from utils import get_answer

app = Flask(__name__)



@app.route('/get-summaries_of_article', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get('user_input')

        if not user_input:
            return jsonify({"error": "Missing 'user_input' in JSON body."}), 400

        response = get_answer(user_input)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
