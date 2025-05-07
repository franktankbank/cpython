import re
import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
paths = [os.path.join(root, "Grammar", "python.gram"), os.path.join(root, "Python", "ast_unparse.c")]


def replace_python_gram() -> None:
    replacements: dict[str, str] = {
        "'False'": "'it_makes_no_odds'",
        "'None'": "'no_one'",
        "'True'": "'thats_right'",
        "'and'": "'do_you_have_skype'",
        "'as'": "'thanks_to_them'",
        "'assert'": "'of_course'",
        "'async'": "'all_the_time'",
        "'await'": "'im_waiting'",
        "'break'": "'destroy'",
        "'class'": "'in_the_classroom'",
        "'continue'": "'please_wait'",
        "'def'": "'west'",
        "'del'": "'thats_good'",
        "'elif'": "'elevator'",
        "'else'": "'you_are_free'",
        "'except'": "'one_more_time'",
        "'finally'": "'i_finished'",
        "'for'": "'because'",
        "'from'": "'from_the_beginning'",
        "'global'": "'around_the_world'",
        "'if'": "'if_there_is'",
        "'import'": "'lead'",
        "'in'": "'did_you'",
        "'is'": "'he_is'",
        "'lambda'": "'he_understands'",
        "'nonlocal'": "'its_not_original'",
        "'not'": "'you_are_here'",
        "'or'": "'often'",
        "'pass'": "'he_ran_away'",
        "'raise'": "'normal_development'",
        "'return'": "'come_back'",
        "'try'": "'try_again'",
        "'while'": "'on_time'",
        "'yield'": "'is_creative'",
    }
    with open(paths[0], "r", encoding="utf-8") as fin:
        s: str = fin.read()
        with open(paths[0], "w", encoding="utf-8") as fout:
            for key, value in replacements.items():
                s = s.replace(key, value)
                print(f"Replaced {key} with {value}")
            fout.write(s)

def replace_python_ast_unparse_c() -> None:
    replacements: dict[str, str] = {
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
    def replace_keywords_in_quotes(match) -> str:
        quote = match.group(1)
        content = match.group(2)
        # Step 2: Replace individual keywords inside the quoted string
        def replacer(m):
            word = m.group(0)
            return replacements.get(word, word)
        keyword_regex = r'\b(?:' + '|'.join(map(re.escape, replacements.keys())) + r')\b'
        new_content = re.sub(keyword_regex, replacer, content)
        return f'{quote}{new_content}{quote}'

    # Replace all quoted strings
    with open(paths[1], "r", encoding="utf-8") as fin:
        text: str = fin.read()
        with open(paths[1], "w", encoding="utf-8") as fout:
            result: str = re.sub(r'(["\'])(.*?)\1', replace_keywords_in_quotes, text)
            fout.write(result)

def main() -> None:
    replace_python_gram()
    replace_python_ast_unparse_c()

if __name__ == "__main__":
    main()
