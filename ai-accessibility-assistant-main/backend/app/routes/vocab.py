from fastapi import APIRouter
import textstat

router = APIRouter()

@router.get("/vocab/{word}")
def get_word_help(word: str):

    simple_definition = f"{word} is a complex word. Try a simpler synonym."

    return {
        "word": word,
        "is_difficult": textstat.difficult_words(word) > 0,
        "suggested_simpler_form": word.lower(),
        "definition_hint": simple_definition
    }