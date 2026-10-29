# Task 4 chatbot project 

from __future__ import annotations

import random
import re
import string
from datetime import datetime

__version__ = "1.0.0"
BOT_NAME = "IT Mate"

# Replies are kept in one place so new intents can be added without
# touching the matching logic below.
GREETING_REPLIES = [
    "Hi!",
    "Hello! Great to see you.",
    "Hey there! How can I help you today?",
]

HOW_ARE_YOU_REPLIES = [
    "I'm fine, thanks! How about you?",
    "I'm doing great, thanks for asking!",
    "All systems running smoothly here. How are you?",
]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache.",
    "There are only 10 types of people in this world: those who understand binary and those who don't.",
]

FAREWELL_REPLIES = [
    "Goodbye! Have a great day!",
    "Bye! Come back anytime.",
    "See you later! Take care.",
]


def normalize_input(user_input: str) -> str:
    """Return a lowercased, punctuation-free version of the input.

    Normalising first means the intent matching below only has to deal
    with plain words, which keeps every rule short and readable.
    """
    lowered = user_input.lower()
    no_punctuation = lowered.translate(str.maketrans("", "", string.punctuation))
    return re.sub(r"\s+", " ", no_punctuation).strip()


def contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    """Return True if any phrase appears as a whole word (or words)."""
    return any(re.search(rf"\b{re.escape(phrase)}\b", text) for phrase in phrases)


def get_response(user_input: str, user_name: str | None = None) -> tuple[str, str | None]:
    """Match one rule-based intent and return (reply, updated_name).

    The if-elif chain is deliberate: this is a rule-based chatbot, so
    the first matching rule wins, in a fixed, predictable order. The
    order matters — specific intents (name, farewell) are checked
    before general ones (greeting) so "bye" is never mistaken for "hi".
    """
    text = normalize_input(user_input)

    # Empty input: never crash, never fall through to the fallback.
    if not text:
        return "You didn't type anything. Try 'help' to see what I can do.", user_name

    # "my name is ..." — remember the name for this session only.
    match = re.match(r"my name is ([a-z ]+)$", text)
    if match:
        name = match.group(1).strip().title()
        return f"Nice to meet you, {name}! I'll remember your name for this chat.", name

    # "what is my name" — recall the stored name, if there is one.
    if contains_any(text, ("what is my name", "do you know my name")):
        if user_name:
            return f"Your name is {user_name}, of course!", user_name
        return "You haven't told me your name yet. Try 'my name is ...'.", user_name

    # Farewell — checked before greeting so "bye" always exits.
    if contains_any(text, ("bye", "goodbye", "quit", "exit", "see you")):
        return random.choice(FAREWELL_REPLIES), user_name

    # Greeting.
    if contains_any(text, ("hello", "hi", "hey", "good morning", "good afternoon", "good evening")):
        greeting = random.choice(GREETING_REPLIES)
        if user_name:
            greeting = f"{greeting} {user_name}!"
        return greeting, user_name

    # Wellbeing.
    if contains_any(text, ("how are you", "how are you doing", "how is it going")):
        return random.choice(HOW_ARE_YOU_REPLIES), user_name

    # Identity.
    if contains_any(text, ("what is your name", "who are you", "your name")):
        return f"I'm {BOT_NAME}, your friendly rule-based chatbot!", user_name

    # Creator.
    if contains_any(text, ("who made you", "who created you", "who built you")):
        return "I was built by A2J as a rule-based chatbot project.", user_name

    # Help — lists everything the bot can actually do.
    if contains_any(text, ("help", "what can you do", "options", "commands")):
        return (
            "Here's what I can do:\n"
            "  - Say hello: 'hello', 'hi', 'hey'\n"
            "  - Ask how I am: 'how are you'\n"
            "  - Tell me your name: 'my name is ...'\n"
            "  - Ask the time: 'what time is it'\n"
            "  - Ask the date: 'what is today's date'\n"
            "  - Hear a joke: 'tell me a joke'\n"
            "  - Say thanks: 'thank you'\n"
            "  - Leave: 'bye', 'quit', or 'exit'"
        ), user_name

    # Time and date — real values from the system clock, never invented.
    if contains_any(text, ("what time is it", "current time", "time now")):
        return f"The current time is {datetime.now().strftime('%I:%M %p')}.", user_name
    if contains_any(text, ("what is today's date", "todays date", "current date", "what date is it")):
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}.", user_name

    # Joke.
    if contains_any(text, ("tell me a joke", "joke", "make me laugh")):
        return random.choice(JOKES), user_name

    # Thanks.
    if contains_any(text, ("thank you", "thanks")):
        return "You're welcome! Happy to help.", user_name

    # Honest limit: no live data is available to a rule-based bot.
    if contains_any(text, ("weather",)):
        return (
            "I can't check live weather — I'm a rule-based chatbot with "
            "no internet access. Try 'help' to see what I can do."
        ), user_name

    # Fallback: admit the miss and point at help instead of guessing.
    return (
        "Sorry, I didn't understand that. "
        "Type 'help' to see everything I can do."
    ), user_name


def is_farewell(user_input: str) -> bool:
    """Return True if the input should end the chat session."""
    return contains_any(normalize_input(user_input), ("bye", "goodbye", "quit", "exit"))


def chat_loop() -> None:
    """Run the interactive chat loop until the user says goodbye."""
    print("=" * 50)
    print(f"  {BOT_NAME} Chatbot  |  version {__version__}")
    print("  Type 'help' to see what I can do, 'bye' to quit.")
    print("=" * 50)

    user_name: str | None = None
    while True:
        try:
            user_input = input("\nYou: ")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C / Ctrl+D: leave politely instead of traceback.
            print(f"\n{BOT_NAME}: Goodbye! Have a great day!")
            break

        reply, user_name = get_response(user_input, user_name)
        print(f"{BOT_NAME}: {reply}")

        if is_farewell(user_input):
            break


def main() -> None:
    """Entry point for the chatbot."""
    chat_loop()


if __name__ == "__main__":
    main()
