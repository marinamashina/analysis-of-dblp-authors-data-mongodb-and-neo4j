import xml.etree.cElementTree as cElementTree
import collections
from pymongo import MongoClient
import json
import xmltodict
import time


def add_element(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

if __name__ == '__main__':
    start_time = time.time()

    connection = MongoClient('localhost', 27017)
    db = connection.DBpractice
    collect = db.authors

    context = cElementTree.iterparse('Data/dblp_utf8.xml', events=("start", "end"))

    context = iter(context)
    event, root = context.__next__() # get the root element of the XML doc

    for event, elem in context:
        temp_dict = {}
        if event == "end":
            if elem.tag in ['article', 'inproceedings', 'incollection']: # i want to write out all <bucket> entries
                temp_dict['type'] = elem.tag
                for inner_elem in iter(elem):
                    if inner_elem.tag =='author':
                        #temp_dict[inner_elem.tag] = inner_elem.text
                        add_element(temp_dict, inner_elem.tag, inner_elem.text)
                    elif inner_elem.tag == 'year':
                        temp_dict['year'] = int(inner_elem.text)
                        #add_element(temp_dict, inner_elem.tag, int(inner_elem.text))
                    else:
                        if inner_elem.tag == 'title':
                            temp_dict['title'] = inner_elem.text
                print(temp_dict)
                collect.insert_one(temp_dict)
            root.clear()  # when done parsing a section clear the tree to safe memory
    connection.close()
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


