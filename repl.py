from interpreter import Interpreter, InterpreterError
import json

COLORS = {
    "green": "\033[92m■\033[0m",
    "orange": "\033[93m■\033[0m",
    "red": "\033[91m■\033[0m"
}

def render_feedback(raw):
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "feedback" in data:
            fb = data["feedback"]
            colored = " ".join(COLORS.get(x, x) for x in fb)
            extra = []
            if "hint" in data:
                extra.append(f"Hint: {data['hint']}")
            if "remaining" in data:
                extra.append(f"Guesses left: {data['remaining']}")
            if data.get("result") == "win":
                extra.append("🎉 You guessed it!")
            return f"{colored}\n" + "\n".join(extra)
        return raw
    except Exception:
        return raw

def repl():
    print("Welcome to Lexis DSL Interpreter!")
    print("Type 'help' for available commands, 'quit' to exit.\n")

    interp = Interpreter()

    while True:
        try:
            mode = interp.mode.capitalize()
            file_info = f" [{interp.current_file}]" if interp.current_file else ""
            prompt = f"[{mode}]{file_info} >>> "

            command = input(prompt).strip()
            if not command:
                continue

            result = interp.run_once(command)
            if result is not None:
                print("\n" + render_feedback(result) + "\n")

        except InterpreterError as e:
            print(f"Interpreter Error: {e}\n")
        except SystemExit:
            print("Goodbye!")
            break
        except Exception as e:
            print(f"Runtime Error: {e}\n")

if __name__ == "__main__":
    repl()