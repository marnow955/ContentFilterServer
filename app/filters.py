
def filter_by_dict(vulgarisms: set, sentence: str):
    sentence_words = set(sentence.split())
    if sentence_words.intersection(vulgarisms):
        return True
    return False
