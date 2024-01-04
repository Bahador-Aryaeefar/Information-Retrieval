import glob, os
import json

class SearchEngine:
    def __init__(self):
        self.file_index = {}
        self.results = []
        self.matches = 0
        self.records = 0

    def create_new_index(self, root_path):
        tokens = {}
        files = os.listdir(root_path)
        for f in files:
            file = open("docs/"+f,"r")
            text = file.read().replace("\n"," ").split(' ')
            for t in text:
                if t in tokens:
                    tokens[t]["freq"] += 1
                    tokens[t]["posting"].append(f)
                else:
                    tokens[t] = {"freq": 1,"posting": []}
        tokens = dict(sorted(tokens.items()))

        self.file_index = tokens

        # Serializing json
        json_object = json.dumps(tokens, indent=4)
 
        # Writing to sample.json
        with open("index.json", "w") as outfile:
            outfile.write(json_object)

    def load_existin_index(self):
        try:
            with open('index.json', 'r') as openfile:
                self.file_index = json.load(openfile)
        except: 
            self.file_index = {}

    def search(self, query):
        pass

def main():
    s = SearchEngine()
    s.create_new_index('c:/Users/Lion/Desktop/IR/docs')
    print(s.file_index)

main()