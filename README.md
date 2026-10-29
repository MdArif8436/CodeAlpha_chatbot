# IT Mate Chatbot — v1.0.0

A simple rule-based chatbot that runs in the terminal. Say hello, ask
how it is, tell it your name, hear a joke, and say goodbye — all with
predefined replies, no AI, no internet, and no setup beyond Python.

Built as **Task 4: Basic Chatbot**, with the required concepts kept
front and centre: `if-elif` intent matching, functions, loops, and
terminal input/output.

## Features

- **Required scope, exactly as specified**
  - `hello` → `Hi!`
  - `how are you` → `I'm fine, thanks!`
  - `bye` → `Goodbye!`
- **Forgiving input** — case, punctuation, and extra spaces don't
  matter, so `HELLO!!!` works exactly like `hello`.
- **More intents, still rule-based**: name, help, time, date, jokes,
  thanks, creator, and farewell.
- **Session memory**: tell it `my name is Arif` and it will greet you
  by name until you quit. Memory lives only in the session — nothing
  is written to disk.
- **Honest limits**: ask about live weather and it tells you it can't
  check it, instead of inventing an answer.
- **Clean exits**: `bye`, `quit`, `exit`, `Ctrl+C`, and `Ctrl+D` all
  end the chat politely.
- **Unit tests** for the rule engine (`test_chatbot.py`, standard
  library `unittest` only).

## Requirements

- Python 3.9 or later
- No third-party packages — the chatbot uses only the standard library

## Quick start

```bash
git clone https://github.com/<your-username>/it-mate-chatbot.git
cd it-mate-chatbot
python chatbot.py
```

On some systems the interpreter is called `python3`:

```bash
python3 chatbot.py
```

## How to use

```
==================================================
  IT Mate Chatbot  |  version 1.0.0
  Type 'help' to see what I can do, 'bye' to quit.
==================================================

You: hello
IT Mate: Hi!

You: how are you
IT Mate: I'm fine, thanks! How about you?

You: my name is Arif
IT Mate: Nice to meet you, Arif! I'll remember your name for this chat.

You: tell me a joke
IT Mate: Why do programmers prefer dark mode? Because light attracts bugs!

You: bye
IT Mate: Goodbye! Have a great day!
```

### Everything it understands

| You say | IT Mate replies |
|---|---|
| `hello`, `hi`, `hey`, `good morning` | A greeting (rotates between a few) |
| `how are you` | A wellbeing reply |
| `what is your name` / `who are you` | Introduces itself as IT Mate |
| `my name is ...` | Remembers your name for the session |
| `what is my name` | Recalls your name, or says you haven't told it yet |
| `help` | Lists every command |
| `what time is it` | The real current time from your system clock |
| `what is today's date` | The real current date |
| `tell me a joke` | A programming joke |
| `thank you` / `thanks` | `You're welcome!` |
| `who made you` | Credits its creator |
| `bye`, `quit`, `exit` | Says goodbye and ends the chat |
| Anything else | An honest "I didn't understand" + a pointer to `help` |

## Project structure

```
it-mate-chatbot/
├── chatbot.py          # The chatbot: intents, replies, chat loop
├── test_chatbot.py     # Unit tests for the rule engine
├── requirements.txt    # No third-party dependencies (standard library only)
├── README.md
├── LICENSE
└── .gitignore
```

## How it works

1. `normalize_input()` lowercases the input, strips punctuation, and
   collapses whitespace, so matching only deals with plain words.
2. `get_response()` walks an `if-elif` chain of intents in a fixed
   order — specific intents (name, farewell) are checked before
   general ones (greeting), so `bye` is never mistaken for `hi`.
3. `contains_any()` matches whole words only, so the `hi` in `this`
   never triggers a greeting.
4. `chat_loop()` reads input until a farewell (or `Ctrl+C`/`Ctrl+D`)
   and prints each reply. Pure logic lives in `get_response()`,
   separate from input/output, which is what makes it unit-testable.

## Testing

```bash
python -m unittest test_chatbot.py -v
```

Smoke test the live chat without typing interactively:

```bash
printf 'hello\nhow are you\nbye\n' | python chatbot.py
```

## Roadmap

- [ ] More intents (e.g. calculator-style arithmetic, small talk)
- [ ] Word-bank replies loaded from a JSON file instead of code
- [ ] Optional colour output for terminals that support it
- [ ] A `--greeting` command-line option for scripted demos

## Limitations

- Rule-based only: it matches predefined patterns and cannot hold a
  real conversation, remember anything between sessions, or access
  live data.
- English input only; other languages are not recognised.

## Contributing

Contributions are welcome — new intents, jokes, and tests in
particular. Please:

1. Fork the repository and create a branch for your change.
2. Add the new intent to `get_response()` and a test in
   `test_chatbot.py`.
3. Keep the project dependency-free and runnable with
   `python chatbot.py`.
4. Open a pull request describing what changed and why.

## License

This project is licensed under the MIT License — see the `LICENSE`
file for details. Created by A2J.
