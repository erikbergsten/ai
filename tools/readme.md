# Chatgpt TOOL experiments

Some tests using openai with langchain to use TOOLS.

## Bad at math

> bad_at_math.py

Getting chatgpt to use specified incorrect mathematical functions to fail
at sipmle arithmetic in spite of it knowing better. I got the stupid thing
to say 2*3 = 15! What a loser.

## Reveiewer

> reviewer.py

The reviewer example reviews a file and uses the read_file tool to check
other files to make sure imports are used correctly. Reviewing main.py with
gpt-4o it correctly reads helpers/strings.py and finds the function name
is different than the one referenced in main.py. Using gpt-3.5-turbo gives
some very bad advice!
