# encoding=utf-8
from models.chatbot_model import ChatbotModel
from utils.app_init import before_init
from utils.helpers import load_all_scene_configs
from utils.info_stream import push_info, get_next_info
from flask import Flask, request, jsonify, send_file, Response

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 实例化ChatbotModel
chatbot_model = ChatbotModel(load_all_scene_configs())


@app.route('/multi_question', methods=['POST'])
def api_multi_question():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    push_info('问题已接收，处理中……')
    response = chatbot_model.process_multi_question(question)
    return jsonify({"answer": response})


@app.route('/send_info', methods=['POST'])
def api_send_info():
    data = request.json
    info = data.get('info')
    if not info:
        return jsonify({"error": "No info provided"}), 400
    push_info(info)
    return jsonify({"status": "ok"})


@app.route('/info_stream')
def info_stream():
    def event_stream():
        while True:
            message = get_next_info()
            yield f"data: {message}\n\n"

    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/', methods=['GET'])
def index():
    return send_file('./demo/user_input.html')


if __name__ == '__main__':
    before_init()
    app.run(port=5000, debug=True)
