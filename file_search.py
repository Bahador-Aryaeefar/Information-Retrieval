import glob, os
import json

class SearchEngine:
    def __init__(self):
        self.docs = {}
        self.file_index = {}
        self.results = []
        self.matches = 0
        self.records = 0

    def create_new_index(self, root_path):
        self.docs = {}
        self.file_index = {}
        id = 1
        tokens = {}
        files = os.listdir(root_path)
        for f in files:
            self.docs[id] = f
            file = open("docs/"+f,"r")
            text = file.read().replace("\n"," ").split(' ')
            for t in text:
                if t in tokens:
                    tokens[t]["freq"] += 1
                    tokens[t]["posting"].append(id)
                else:
                    tokens[t] = {"freq": 1,"posting": [id]}
            id += 1
        tokens = dict(sorted(tokens.items()))

        self.file_index = tokens

        temp = {"index": tokens, "docs": self.docs}

        # Serializing json
        json_object = json.dumps(temp, indent=4)
 
        # Writing to sample.json
        with open("index.json", "w") as outfile:
            outfile.write(json_object)

    def load_existin_index(self):
        try:
            with open('index.json', 'r') as openfile:
                temp = json.load(openfile)
                self.file_index = temp["index"]
                self.docs = temp["docs"]
            
        except: 
            self.file_index = {}

    def search(self, query):
        self.results.clear()
        terms = query.split(' ')
        # for t in terms:
        #     if t in self.file_index:

                
        # print(terms)

def main():
    s = SearchEngine()
    s.create_new_index('c:/Users/Lion/Desktop/IR/docs')
    print(s.file_index)
    print(s.docs)
    s.search('the first')

main()