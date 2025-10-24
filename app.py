from flask import Flask, request, jsonify
from Interpreter import Interpreter, InterpreterError

app = Flask(__name__)
interp = Interpreter()

@app.route("/run", methods=["POST"])
def run():
    try:
        data = request.get_json(force=True)
        command = data.get("command", "").strip()
        if not command:
            return jsonify({"status": "error", "message": "No command provided"}), 400

        result = interp.run_once(command)
        return jsonify(result)

    except InterpreterError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Runtime error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)