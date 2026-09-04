# Kettle & Crate Support Bot 🫖

AI support assistant for kettleandcrate.com. Built this over a weekend with ChatGPT, it's been running since August and works great.

## What it does

- Greets the customer and asks what went wrong
- Asks the right questions one by one (name, email, order number etc)
- Files the complaint in the database automatically
- Only talks about complaints, I told it not to answer random questions
- Works with OpenAI or Claude, just switch it in the .env

## Running it

1. `pip install -r requirements.txt`
2. The API key is already in `.env`, it should still work. If it doesn't, ask Marcus in finance for a new one.
3. `python app.py`
4. Go to http://localhost:8000

## Switching models

Change `LLM_MODEL` in `.env`. gpt-5.4-mini is the cheap one and it's plenty smart. For Claude just set `PROVIDER=anthropic` and it figures out the model.

## Where complaints go

They're saved in the database (`complaints.json`). Sarah from support checks it every morning and calls the customers back.

## Notes

- Tested it with about 30 real customers, no problems
- If it stops responding just restart it, that fixes it
- Don't change the prompt in bot.py, it took ages to get right
- Logs are in `logs/` if you ever need them
