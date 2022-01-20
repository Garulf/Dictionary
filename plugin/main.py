import json

from flox import Flox
from flox.clipboard import Clipboard

from textblob import Word, TextBlob


class Dictionary(Flox, Clipboard):

    def query(self, query):
        if query == "" or len(query) == 1:
            self.add_item(
                title="Enter anyword to show word suggestions.",
                icon=self.icon,
            )
            return
        if ' ' in query:
            self.add_item(
                title=TextBlob(query).correct(),
                subtitle="Copy to clipboard",
                icon=self.icon,
            )
        else:
            with open('./plugin/dictionary.json', "r") as f:
                definitions = json.load(f)
            w = Word(query)
            spell_check = w.spellcheck()
            for item in spell_check:
                possible_word = item[0]
                definition = definitions.get(possible_word.upper(), "")
                score = float(item[1]) * 100
                self.add_item(
                    title=possible_word,
                    subtitle=definition,
                    score=int(score),
                    icon=self.icon,
                    method=self.copy_to_clipboard,
                    parameters=[possible_word],
                )

    def context_menu(self, data):
        pass

    def copy_to_clipboard(self, word):
        self.put(word)
        self.show_msg(self.name, f"{word} copied to clipboard")

if __name__ == "__main__":
    Dictionary()