# Lexis - Word Bank Interpreter

A command-line word bank manager and word-guessing game framework built with Python. Lexis supports three game modes: letter-based word guessing (similar to Wordle), category-based comparison, and hint-driven gameplay.

## Documentation
This README is a short overview.  
For the complete in-depth manual, download:  
➡️ **[Lexis Full User Guide](docs/Lexis_Full_User_Guide.pdf)**
For internal technical details, see:
➡️ Developer Reference Manual (docs/Developer_Reference_Manual.md)

## Features

- **Three Game Modes**
  - **Letters Mode**: Traditional letter-by-letter word guessing with visual feedback
  - **Categories Mode**: Multi-attribute word comparison across custom categories
  - **Hints Mode**: Progressive hint-based word guessing

- **Dual Operation Modes**
  - **Edit Mode**: Create, modify, and manage word bank files
  - **Play Mode**: Interactive gameplay with customizable settings

- **Flexible Storage**: Text-based word bank files with automatic format detection

## Installation

### Prerequisites
- Python 3.7+
- Flask (for web interface)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd lexis-interpreter

# Install dependencies
pip install flask

# Create word banks directory
mkdir -p WordBanks
```

## Usage

### Terminal REPL
```bash
python repl.py
```

### Web API
```bash
flask run
# or
python app.py
```

The API exposes a single endpoint:
```
POST /run
Content-Type: application/json

{
  "command": "file fruits"
}
```

## Command Reference

### Edit Mode

Edit mode commands allow you to create and manage word bank files.

| Command | Description | Example |
|---------|-------------|---------|
| `create <filename>` | Create a new word bank file | `create animals` |
| `file <filename>` | Load existing word bank | `file fruits.txt` |
| `deletefile <filename>` | Delete a word bank file | `deletefile old_words` |
| `categories <cat1> \| <cat2> \| ...` | Define category headers | `categories type \| color \| size` |
| `add <word>` | Add word (letters mode) | `add apple` |
| `add <word> \| <val1> \| <val2>` | Add word with attributes | `add rose \| flower \| red \| medium` |
| `list` | Display all entries | `list` |
| `edit <index> \| <values>` | Modify entry by index | `edit 1 \| tulip \| flower \| yellow` |
| `delete <index>` | Remove entry by index | `delete 3` |
| `done` | Return to play mode | `done` |
| `help` | Show edit commands | `help` |

### Play Mode

Play mode commands control gameplay and game settings.

| Command | Description | Example |
|---------|-------------|---------|
| `file <filename>` | Load word bank for gameplay | `file animals` |
| `start` | Initialize new game session | `start` |
| `word [<word>]` | Set or randomize secret word | `word` or `word elephant` |
| `guess <word>` | Submit a guess | `guess tiger` |
| `show` | Reveal current secret word | `show` |
| `words` | List all available words | `words` |
| `max_guesses <n>` | Set guess limit | `max_guesses 10` |
| `edit` | Switch to edit mode | `edit` |
| `help` | Show play commands | `help` |
| `quit` | Exit interpreter | `quit` |

## File Formats

### Letters Mode
Plain text, one word per line:
```
apple
banana
cherry
```

### Hints Mode
Word followed by pipe-separated hints:
```
apple | red fruit | grows on trees
banana | yellow fruit | monkeys love it
```

### Categories Mode
Header row with pipe-separated categories, followed by word entries:
```
word | type | color | size
rose | flower | red | medium
oak | tree | brown | large
tulip | flower | yellow | small
```

## Gameplay

### Letters Mode Feedback
- 🟩 Correct letter in correct position
- 🟨 Correct letter in wrong position
- ⬜ Letter not in word

### Categories Mode Feedback
- ✅ Category value matches
- ❌ Category value differs

### Hints Mode Feedback
- Progressive hints revealed after each incorrect guess
- Simple correct/incorrect messages

## Example Session

```bash
[Edit] >>> create flowers
Created 'flowers' in letters mode (default).

[Edit] [flowers] >>> categories type | color | season
Saved to 'flowers'

[Edit] [flowers] >>> add rose | perennial | red | summer
Saved to 'flowers'

[Edit] [flowers] >>> add tulip | bulb | yellow | spring
Saved to 'flowers'

[Edit] [flowers] >>> list
word | type | color | season
rose | perennial | red | summer
tulip | bulb | yellow | spring

[Edit] [flowers] >>> done
Exiting edit mode, back to play mode.

[Play] [flowers] >>> start
Game started in CATEGORIES mode. Use 'word' or 'word <word>' to select a secret word.

[Play] [flowers] >>> word
Secret word has been set. Use 'guess <word>' to start guessing.

[Play] [flowers] >>> guess tulip
{"result": "continue", "feedback": ["type: ❌ (bulb)", "color: ❌ (yellow)", "season: ❌ (spring)"], "remaining": 5}

[Play] [flowers] >>> guess rose
{"result": "win", "feedback": ["type: ✅ (perennial)", "color: ✅ (red)", "season: ✅ (summer)"]}
```

## Project Structure

```
.
├── Interpreter/
│   ├── __init__.py
│   ├── interpreter.py          # Core interpreter logic
│   ├── lexer.py                # Tokenization
│   ├── parser.py               # Command parsing
│   └── ast_nodes/
│       ├── __init__.py
│       ├── base.py             # Base AST node
│       ├── edit.py             # Edit mode nodes
│       └── play.py             # Play mode nodes
├── WordBanks/                  # Word bank storage
├── docs/
│   └── Lexis_Full_User_Guide.pdf   # Full project documentation
├── app.py                      # Flask web API
├── repl.py                     # Terminal interface
└── README.md

```

## Design Notes

- Commands are case-insensitive
- File format is auto-detected on load
- Quotation marks are optional unless values contain spaces
- The `categories` command automatically switches files to category mode
- Use `start` before selecting words or making guesses in play mode

## Error Handling

The interpreter provides clear error messages for common issues:
- File not found
- Empty word banks
- Invalid indices
- Mismatched category counts
- Words not in the current bank
