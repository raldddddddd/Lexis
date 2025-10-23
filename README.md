# 🧩 Word Bank Interpreter

A Python-based command-line word bank manager and word-guessing game framework.

It supports three types of word banks:
- **Letters Mode** — simple word lists  
- **Categories Mode** — multi-attribute word sets  
- **Hints Mode** — word-hint pairs  

Users can **create**, **edit**, and **play** directly through typed commands.

---

## 🚀 Modes Overview

There are two main modes of operation:

| Mode | Purpose |
|------|----------|
| **Edit Mode** | Create and manage word bank files |
| **Play Mode** | Start and play the guessing game |

The current mode is always visible in the prompt:

[Edit] [fruits.txt] >>>
[Play] [fruits.txt] >>>

---

## 🧱 Edit Mode Commands

Used to create, load, and modify word bank files.

| Command | Description | Example |
|----------|--------------|----------|
| `create <filename> [mode]` | Create a new file. Optional mode: `letters`, `categories`, or `hints`. | `create fruits letters` |
| `file <filename>` | Load an existing file into edit mode. | `file tea` |
| `deletefile <filename>` | Delete a file from storage. | `deletefile tea` |
| `categories <name1> \| <name2> \| ...` | Define column headers for category mode. | `categories size \| shape \| color` |
| `add <word>` | Add a word (letters mode only). | `add apple` |
| `add <word> \| <v1> \| <v2> \| ...` | Add a word and its associated values. | `add hibiscus \| large \| round \| red` |
| `list` | Display all words and their details. | `list` |
| `edit <index> \| <new_values>` | Modify a specific entry by index. | `edit 2 \| small \| star \| white` |
| `delete <index>` | Delete a specific row by its index. | `delete 1` |
| `done` | Exit edit mode and return to play mode. | `done` |
| `help` | Show all available edit commands. | `help` |

---

## 🎮 Play Mode Commands

Used to play guessing games using a loaded word bank.

| Command | Description | Example |
|----------|--------------|----------|
| `file <filename>` | Load a word bank into play mode. | `file fruits` |
| `start` | Begin a new game session. Required before using `word` or `guess`. | `start` |
| `word [word]` | Select or display the current secret word. | `word` |
| `words` | List all available words from the file. | `words` |
| `max_guesses <number>` | Set the maximum number of guesses. | `max_guesses 5` |
| `guess <word>` | Submit a guess for the secret word. | `guess apple` |
| `show` | Display the currently selected secret word. | `show` |
| `edit` | Switch back to edit mode. | `edit` |
| `help` | Display available play commands. | `help` |
| `quit` | Exit the interpreter. | `quit` |

---

## 💾 File Types

Each file type determines how data is stored and used during play.

| Mode | Structure | Example |
|------|------------|----------|
| **letters** | Each line contains one word | `apple` |
| **categories** | First line defines column headers using pipes (`|`) <br> Each subsequent line defines word entries | `word \| size \| shape \| color`<br>`hibiscus \| large \| round \| red` |
| **hints** | Word followed by a hint separated by `|` | `apple \| a red fruit` |

> Using the `categories` command in Edit mode automatically switches the current file to **category mode**.

---

## 🖥️ Running the Project

### 🔹 Option 1: Run in Terminal (REPL)
```bash
python repl.py

### 🔹 Option 2: Run as a Web App

bash
Copy code
python web_app.py

---

## 🧠 Example Workflow

[Edit] >>> create tea
Created 'tea' in letters mode.

[Edit] [tea] >>> categories size | shape | color
Saved to 'tea'

[Edit] [tea] >>> add hibiscus | large | round | red
Saved to 'tea'

[Edit] [tea] >>> add jasmine | small | star | white
Saved to 'tea'

[Edit] [tea] >>> list
word | size | shape | color
hibiscus | large | round | red
jasmine | small | star | white

[Edit] [tea] >>> done
Exiting edit mode, back to play mode.

[Play] [tea] >>> start
Game started in CATEGORIES mode. Use 'word' or 'word <word>' to select a secret word.

[Play] [tea] >>> word
Secret word set to 'hibiscus'. Use 'guess <word>' to start guessing.

[Play] [tea] >>> guess jasmine
{"result": "continue", "feedback": ["size: ❌ (small)", "shape: ❌ (star)", "color: ❌ (white)"], "remaining": 5}

[Play] [tea] >>> show
The secret word is: hibiscus

---

## 📝 Notes

- Always use `start` before selecting or guessing words in play mode.
- `categories` must be defined before adding multi-column entries.
- Quotation marks are optional unless your values include spaces.
- The interpreter auto-detects file types when loading.
- Commands are **case-insensitive**.

---

## 🧩 Supported Modes Summary

| Mode | Description | Feedback Type |
|------|--------------|----------------|
| **letters** | Word guessing (like Wordle) | Per-letter boxes (🟩 🟨 ⬜) |
| **categories** | Compare category matches | Per-category ✅ / ❌ |
| **hints** | Guess using hints | Text-based correctness messages |

---

## 📂 Project Structure

├── interpreter.py # Main logic and command evaluation
├── parser.py # Command parsing into AST nodes
├── lexer.py # Tokenizer for user input
├── ast_nodes/
│ ├── play.py # Play mode node definitions
│ ├── edit.py # Edit mode node definitions
│ └── base.py # Shared node base class
└── README.md