from urllib.request import urlopen

# A script that obtains a GO-term-to-parent dictionary from a Core ontology (OBO Format) file
# sourced from http://current.geneontology.org/ontology/go.obo

# A GO-term-to-parent dictionary
go_dictionary = dict()

# A dictionary that maps a GO term to the main ID, which looks like the following:
# 1. The GO term itself, for instance, e.g. ["GO:0000001", "GO:0000001"]
# 2. A main id if the file lists the term as an "alt_id:", e.g. ["GO:0019952", "GO:0000003"]
# Note: We only consider main IDs to be those labeled as "id:" in the file
go_terms_to_main_ids = dict()


# Note, as of right now, each alt_id of the GO term is a new element
# in the dictionary for searching purposes. We can later add, if needed,
# an additional dictionary that maps each GO term to a list of its alt_ids.
# that would allow searching a GO term to any possible alt_ids.

# Adds all the entries to go_dictionary
def get_go_dictionary():
    # Used to represent a new GO term encountered
    go_term = ""
    go_term_count = 0
    alt_go_count = 0
    obsolete_count = 0
    # A list of any alternative IDs for go_term
    alt_ids_of_go_term = []
    # List of the GO term's parents
    list_of_parents = []

    # Grabs the up-to-date monthly release of the gene ontology

    # Code expects the syntax and semantics of the version downloaded on
    # November 9, 2021.
    url = "http://current.geneontology.org/ontology/go.obo"
    file = urlopen(url)
    for line in file:
        line = line.decode("utf-8").strip()

        # The beginning index of any substring we concern.
        start_index = line.find(':') + 1

        if "id: GO" in line and "alt_id:" not in line:
            go_term_count += 1
            if go_term != "":
                # If we have reached a new GO term and a previous has been defined,
                # we need to store the term and its parents in the
                # dictionary and reset all local variables

                # If there are any alternate IDs, we assign each alt_id to a key in the dictionary,
                # and the parents of the GO term are each one's values.
                if len(alt_ids_of_go_term) > 0:
                    for alt_id in alt_ids_of_go_term:
                        go_terms_to_main_ids[alt_id] = go_term
                        go_dictionary[alt_id] = list_of_parents
                        # Empty the list of alternate IDs
                    alt_ids_of_go_term = []

                go_terms_to_main_ids[go_term] = go_term
                go_dictionary[go_term] = list_of_parents
                go_term = ""
                list_of_parents = []
            # Assign the new GO term to go_term.
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
        # The same routine as above, we just need to put the last go_term
        # in the dictionary if there is still one remaining
        if len(alt_ids_of_go_term) > 0:
            for alt_id in alt_ids_of_go_term:
                go_dictionary[alt_id] = list_of_parents
            alt_ids_of_go_term = []
        go_dictionary[go_term] = list_of_parents
        go_term = ""
        list_of_parents = []

    # # Uncomment the statements below to print the entire GO-term-to-parent dictionary.
    # for key, value in go_dictionary.items():
    #     print(key, value)
    # print("Number of keys in dictionary: " + str(len(go_dictionary)))

    # # Uncomment the statements below to get information about the file.
    # print("File information mentioned below")
    # print("Number unique GO terms: " + str(go_term_count))
    # print("Number of alt_id GO terms: " + str(alt_go_count))
    # print("Number of obsolete terms: " + str(obsolete_count))
    # print("Total mentioned non-obsolete GO terms (including alt_ids) in the file: " +
    #       str(go_term_count + alt_go_count))


# Prints the parents of a given GO term
# Expected go_term format example: "GO:1903204"
def get_go_term_parents_given_go_term(go_term):
    print("The parents of " + go_term + " are " + str(go_dictionary[go_term]))


# Prints the (id:) associated with the GO term
# Note: We only consider main IDs to be those labeled as "id:" in the file
def get_main_id_of_go_term(go_term):
    print("The main ID of " + go_term + " is " + str(go_terms_to_main_ids[go_term]))


# Prints a single path from the go_term to a root.
# If the term is obsolete, then the method will state that.
def get_one_go_path(go_term):
    if (len(go_dictionary[go_term]) != 0) and (go_dictionary[go_term][0] == '-1'):
        print("The term " + go_term + " is obsolete.")
    else:
        path = []
        done = 0
        current_term = go_term
        print("A single path from " + go_term + " to a root is shown below.")
        while not done:
            path.append(current_term)
            if len(go_dictionary[current_term]) == 0:
                done = 1
            else:
                # Follows the path where we take the first parent in the list
                current_term = go_dictionary[current_term][0]
        if len(path) == 1:
            # There are three roots to the GO DAG
            # Biological Process (id: GO:0008150)
            # Cellular Component (id: GO:0005575)
            # Molecular Function (id: GO:0003674)
            print("You provided a root node: " + current_term)
        else:
            print(path)
'''
same method as above but with different formatting
'''
def get_one_go_path(go_term):
    if (len(go_dictionary[go_term]) != 0) and (go_dictionary[go_term][0] == '-1'):
        #print("The term " + go_term + " is obsolete.")
        return -1
    else:
        path = []
        done = 0
        current_term = go_term
        #print("A single path from " + go_term + " to a root is shown below.")
        while not done:
            path.append(current_term[3:])
            if len(go_dictionary[current_term]) == 0:
                done = 1
            else:
                # Follows the path where we take the first parent in the list
                current_term = go_dictionary[current_term][0]
        if len(path) == 1:
            # There are three roots to the GO DAG
            # Biological Process (id: GO:0008150)
            # Cellular Component (id: GO:0005575)
            # Molecular Function (id: GO:0003674)
            print("You provided a root node: " + current_term)
        else:
            return list(reversed(path))

if __name__ == '__main__':
    get_go_dictionary()
    # Uncomment to see how the searching for the parents of a GO term works
    get_go_term_parents_given_go_term("GO:1903204")
    # Uncomment to see how the searching for the "main ID" of a GO term works
    # Example when it is an "id:", AKA a "main ID"
    get_main_id_of_go_term("GO:0000003")
    # Example when it is an "alt_id:" of a main ID
    get_main_id_of_go_term("GO:0019952")

    # Examples of getting a path
    # A short path example
    get_one_go_path("GO:0000003")
    # A longer path example
    get_one_go_path("GO:0008441")
    # Root node example
    get_one_go_path("GO:0008150")
    # Obsolete node example
    get_one_go_path("GO:0008155")
