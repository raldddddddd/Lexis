import os
import random
import json
from lexer import Lexer
from parser import Parser, ParserError
from ast_nodes import play, edit

class InterpreterError(Exception):
    pass

class Interpreter:
    def __init__(self):
        self.mode = "play"
        self.words = []
        self.word_data = []
        self.categories = []
        self.secret = None
        self.secret_row = None
        self.max_guesses = 6
        self.remaining_guesses = self.max_guesses
        self.current_file = None
        self.hint_index = 0

    def run_once(self, code: str):
        lexer = Lexer(code)
        tokens = []
        while True:
            tok = lexer.next_token()
            tokens.append(tok)
            if tok.type.name == "EOF":
                break
        try:
            parser = Parser(tokens, self.mode)
            node = parser.parse()
            return self.eval(node)
        except ParserError as e:
            return f"Syntax Error: {e}"

    def eval(self, node):
        if isinstance(node, (play.Help, edit.Help)):
            node = play.Help() if self.mode == "play" else edit.Help()
        if self.mode == "play":
            return self._eval_play(node)
        if self.mode == "edit":
            return self._eval_edit(node)
        raise InterpreterError(f"Invalid mode {self.mode}")

    def _eval_play(self, node):
        if isinstance(node, play.Help):
            commands = ["file <filename>", "start", "help", "quit", "edit"]
            if self.current_file:
                commands += ["words", "max_guesses <n>", "word <word>", "guess <word>"]
            return "Play commands available:\n  " + "\n  ".join(commands)

        if isinstance(node, play.File):
            return self._load_file(node.filename)

        if isinstance(node, play.Start):
            if not self.current_file:
                return "Error: No word bank loaded."
            self.secret = None
            self.secret_row = None
            self.hint_index = 0
            self.remaining_guesses = self.max_guesses
            return "Game started! Type 'word' or 'word <word>' to choose a secret word."

        if isinstance(node, play.Word):
            if not self.current_file:
                return "Error: No word bank loaded."
            if node.word:
                if node.word not in self.words:
                    return f"Error: Word '{node.word}' not in bank."
                idx = self.words.index(node.word)
                self.secret = node.word
                self.secret_row = self.word_data[idx]
            else:
                if not self.words:
                    return "Error: Word bank empty."
                idx = random.randrange(len(self.words))
                self.secret = self.words[idx]
                self.secret_row = self.word_data[idx]
            self.remaining_guesses = self.max_guesses
            self.hint_index = 0
            return f"Secret word set. Use 'guess <word>'."

        if isinstance(node, play.Guess):
            if not self.secret:
                return "Error: No secret word chosen."
            if self.remaining_guesses <= 0:
                return "No guesses left."
            self.remaining_guesses -= 1
            feedback = self._make_feedback(node.word)
            if node.word == self.secret:
                self.secret = None
                self.secret_row = None
                return json.dumps({"result": "win", "feedback": feedback})
            extra = None
            if self.categories:
                pass
            elif len(self.secret_row) > 1:
                if self.hint_index < len(self.secret_row) - 1:
                    extra = self.secret_row[self.hint_index + 1]
                    self.hint_index += 1
            result = {"result": "continue", "feedback": feedback, "remaining": self.remaining_guesses}
            if extra:
                result["hint"] = extra
            return json.dumps(result)

        if isinstance(node, play.Words):
            if not self.current_file:
                return "Error: No word bank loaded."
            return "Words: " + ", ".join(self.words)

        if isinstance(node, play.MaxGuesses):
            self.max_guesses = node.n or 6
            self.remaining_guesses = self.max_guesses
            return f"Max guesses set to {self.max_guesses}"

        if isinstance(node, play.Edit):
            self.mode = "edit"
            return "Switched to edit mode. Type 'help' for edit commands."

        if isinstance(node, play.Quit):
            raise SystemExit()

        return f"Unknown play command: {node}"

    def _make_feedback(self, guess):
        if self.categories:
            g_idx = self.words.index(guess) if guess in self.words else None
            if g_idx is None:
                return ["red"]
            g_row = self.word_data[g_idx]
            return ["green" if g_row[i] == self.secret_row[i] else "red" for i in range(len(g_row))]
        secret = self.secret
        feedback = []
        for i, ch in enumerate(guess):
            if i < len(secret) and ch == secret[i]:
                feedback.append("green")
            elif ch in secret:
                feedback.append("orange")
            else:
                feedback.append("red")
        return feedback

    def _eval_edit(self, node):
        if isinstance(node, edit.Help):
            commands = ["create <filename>", "file <filename>", "deletefile <filename>", "help", "done"]
            if self.current_file:
                commands += ["categories <c1|c2|...>", "add <word|v1|...>", "list", "edit <index v1|...>", "delete <index>"]
            return "Edit commands available:\n  " + "\n  ".join(commands)

        if isinstance(node, edit.Create):
            return self._create_file(node.filename)

        if isinstance(node, edit.File):
            return self._load_file(node.filename)

        if isinstance(node, edit.DeleteFile):
            return self._delete_file(node.filename)

        if isinstance(node, edit.Categories):
            if not self.current_file:
                return "Error: No file loaded."
            self.categories = node.headers
            return self._save_file()

        if isinstance(node, edit.Add):
            if not self.current_file:
                return "Error: No file loaded."
            row = [node.word] + node.values
            if self.categories and len(row) != len(self.categories):
                return f"Error: Expected {len(self.categories)} values, got {len(row)}"
            self.word_data.append(row)
            self.words.append(node.word)
            return self._save_file()

        if isinstance(node, edit.ListWords):
            if not self.current_file:
                return "Error: No file loaded."
            if not self.word_data:
                return "No words available."
            lines = []
            if self.categories:
                lines.append(" | ".join(self.categories))
                lines.append("-" * len(lines[0]))
            for row in self.word_data:
                lines.append(" | ".join(row))
            return "\n".join(lines)

        if isinstance(node, edit.Edit):
            if not self.current_file:
                return "Error: No file loaded."
            if node.index < 1 or node.index > len(self.word_data):
                return f"Error: Index {node.index} out of range"
            new_row = node.values
            if self.categories and len(new_row) != len(self.categories):
                return f"Error: Expected {len(self.categories)} values, got {len(new_row)}"
            self.word_data[node.index - 1] = new_row
            self.words[node.index - 1] = new_row[0]
            return self._save_file()

        if isinstance(node, edit.Delete):
            if not self.current_file:
                return "Error: No file loaded."
            if node.index < 1 or node.index > len(self.word_data):
                return f"Error: Index {node.index} out of range"
            removed = self.word_data.pop(node.index - 1)
            self.words.pop(node.index - 1)
            return f"Deleted word '{removed[0]}'\n" + self._save_file()

        if isinstance(node, edit.Done):
            self.mode = "play"
            return "Exiting edit mode, back to play mode."

        return f"Unknown edit command: {node}"

    def _create_file(self, filename):
        if os.path.exists(filename):
            return f"Error: file '{filename}' already exists"
        with open(filename, "w", encoding="utf-8") as f:
            pass
        self.current_file = filename
        self.words = []
        self.word_data = []
        self.categories = []
        return f"Created file '{filename}'. Use 'categories' or 'add'."

    def _load_file(self, filename):
        if not os.path.exists(filename):
            return f"Error: file '{filename}' not found"
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            self.categories, self.word_data, self.words = [], [], []
        else:
            first = lines[0].split("|")
            if len(first) > 1 and all(x.strip() for x in first):
                self.categories = [x.strip() for x in first]
                self.word_data = [[y.strip() for y in line.split("|")] for line in lines[1:]]
            else:
                self.categories = []
                self.word_data = [[y.strip() for y in line.split("|")] for line in lines]
        self.words = [row[0] for row in self.word_data]
        self.current_file = filename
        return f"Loaded file '{filename}' with {len(self.words)} words"

    def _save_file(self):
        if not self.current_file:
            return "Error: no file selected"
        with open(self.current_file, "w", encoding="utf-8") as f:
            if self.categories:
                f.write(" | ".join(self.categories) + "\n")
            for row in self.word_data:
                f.write(" | ".join(row) + "\n")
        return f"Saved to '{self.current_file}'"

    def _delete_file(self, filename):
        if not os.path.exists(filename):
            return f"Error: file '{filename}' does not exist"
        os.remove(filename)
        if self.current_file == filename:
            self.current_file, self.words, self.word_data, self.categories = None, [], [], []
        return f"Deleted file '{filename}'"