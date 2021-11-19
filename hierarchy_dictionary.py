from urllib.request import urlopen

go_dictionary = dict()
go_terms_to_main_ids = dict()

'''
gets GO term information from the ontology website and creates a dictionary to store it
'''
def get_go_dictionary():
    go_term = ""
    go_term_count = 0
    alt_go_count = 0
    obsolete_count = 0
    alt_ids_of_go_term = []
    list_of_parents = []
    url = "http://current.geneontology.org/ontology/go.obo"
    file = urlopen(url)
    for line in file:
        line = line.decode("utf-8").strip()
        start_index = line.find(':') + 1
        if "id: GO" in line and "alt_id:" not in line:
            go_term_count += 1
            if go_term != "":
                if len(alt_ids_of_go_term) > 0:
                    for alt_id in alt_ids_of_go_term:
                        go_terms_to_main_ids[alt_id] = go_term
                        go_dictionary[alt_id] = list_of_parents
                    alt_ids_of_go_term = []

                go_terms_to_main_ids[go_term] = go_term
                go_dictionary[go_term] = list_of_parents
                go_term = ""
                list_of_parents = []
            go_term = line[start_index:].strip()
        elif "alt_id:" in line:
            alt_go_count += 1
            alt_ids_of_go_term.append(line[start_index:].strip())
        elif "is_a: GO" in line:
            parent_of_go_term = ""
            start_index = line.index(":") + 1
            end_index = line.index("!")
            parent_of_go_term = line[start_index:end_index].strip()
            list_of_parents.append(parent_of_go_term)
        elif "is_obsolete: true" in line:
            obsolete_count += 1
            list_of_parents = ["-1"]
    if go_term != "":
        if len(alt_ids_of_go_term) > 0:
            for alt_id in alt_ids_of_go_term:
                go_dictionary[alt_id] = list_of_parents
            alt_ids_of_go_term = []
        go_dictionary[go_term] = list_of_parents
        go_term = ""
        list_of_parents = []

'''
gets a hierarchical path from the root to the given term
'''
def get_one_go_path(go_term):
    if (len(go_dictionary[go_term]) != 0) and (go_dictionary[go_term][0] == '-1'):
        return -1
    else:
        path = []
        done = 0
        current_term = go_term
        while not done:
            path.append(current_term[3:])
            if len(go_dictionary[current_term]) == 0:
                done = 1
            else:
                current_term = go_dictionary[current_term][0]
        return list(reversed(path))