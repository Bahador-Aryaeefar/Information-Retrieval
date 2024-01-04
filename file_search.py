import glob, os
import json
import PySimpleGUI as sg
sg.ChangeLookAndFeel('Black')

class Gui:
    def __init__(self):
        self.layout: list = [
            [sg.Text('Search Term', size=(11,1)),
             sg.Input(size=(40,1), focus=True, key="TERM"),
             sg.Button('Search', size=(10,1), bind_return_key=True, key="_SEARCH_"),
             sg.Button('Re-Index', size=(10,1), key="_INDEX_")],
            [sg.Output(size=(100,30))]]
        
        self.window: object = sg.Window('File Search Engine', self.layout, element_justification='left')

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
        records = []
        for t in terms:
            if t in self.file_index:
                records.append(self.file_index[t]["posting"].copy())
             
        if(len(records) == 0):
            self.results = []
            return

        while len(records)>1 :
            temp = []
            i = 0
            j = 0
            while True:
                if i < len(records[0]) and j < len(records[1]):
                    if records[0][i] == records[1][j]:
                        temp.append(records[0][i])
                        i += 1
                        j += 1
                    elif records[0][i] < records[1][j]:
                        i += 1
                    else: 
                        j += 1
                else:
                    break
            records.pop(0)
            records[0] = temp
   

        self.results = records[0]
            


def main():
    s = SearchEngine()
    g = Gui()
    s.load_existin_index()
    while True: 
        event, value = g.window.Read()
        if event is None:
            break

        if event == "_SEARCH_":
            # g.layout[1][0].Update('')
            s.search(value["TERM"])
            print(s.results)

        if event == "_INDEX_":
            s.create_new_index('c:/Users/Lion/Desktop/IR/docs')
            print(">> New index created")
    
main()