import tokenize
from io import BytesIO
import sys
import os
import re

# Your syntax replacement map
replacement: dict[str, str] = {
    "False": "it_makes_no_odds",
    "None": "no_one",
    "True": "thats_right",
    "and": "do_you_have_skype",
    "as": "thanks_to_them",
    "assert": "of_course",
    "async": "all_the_time",
    "await": "im_waiting",
    "break": "destroy",
    "class": "in_the_classroom",
    "continue": "please_wait",
    "def": "west",
    "del": "thats_good",
    "elif": "elevator",
    "else": "you_are_free",
    "except": "one_more_time",
    "finally": "i_finished",
    "for": "because",
    "from": "from_the_beginning",
    "global": "around_the_world",
    "if": "if_there_is",
    "import": "lead",
    "in": "did_you",
    "is": "he_is",
    "lambda": "he_understands",
    "nonlocal": "its_not_original",
    "not": "you_are_here",
    "or": "often",
    "pass": "he_ran_away",
    "raise": "normal_development",
    "return": "come_back",
    "try": "try_again",
    "while": "on_time",
    "yield": "is_creative"
}

def transpile_code(source_code: str, replacements: dict) -> str:
    output_tokens = []

    # Tokenize the code
    tokens = list(tokenize.tokenize(BytesIO(source_code.encode("utf-8")).readline))

    prev_token = None
    prev_prev_token = None # To catch compile("...", "filename", "mode")
    for token in tokens:
        tok_type = token.type
        tok_val = token.string

        if tok_type == tokenize.NAME and tok_val in replacements:
            tok_val = replacements[tok_val]

        # Replace strings inside exec/eval/compile calls
        elif (
            tok_type == tokenize.STRING
            and prev_token is not None
            and prev_token.type == tokenize.OP
            and prev_prev_token is not None
            and prev_prev_token.type == tokenize.NAME
            and prev_prev_token.string in ("exec", "eval", "compile")
        ):
            try:
                inner_code = eval(tok_val)  # safely evaluate the string
                for old, new in replacements.items():
                    inner_code = re.sub(rf'\b{re.escape(old)}\b', new, inner_code)
                tok_val = repr(inner_code)
            except Exception:
                pass  # Don't touch if eval fails

        output_tokens.append(token._replace(string=tok_val))
        prev_prev_token = prev_token
        prev_token = token

    return tokenize.untokenize(output_tokens).decode("utf-8")

def main():
    if len(sys.argv) != 2:
        print("Usage: python transpiler.py path/to/input_script.py")
        sys.exit(1)

    input_path = sys.argv[1]

    # Ensure the file exists
    if not os.path.isfile(input_path):
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)

    # Read the file
    with open(input_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    # Transpile the code
    transpiled = transpile_code(source_code, replacement)

    # Write back the transpiled content to the same file
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(transpiled)

    print(f"File '{input_path}' has been transpiled successfully!")

if __name__ == "__main__":
    main()