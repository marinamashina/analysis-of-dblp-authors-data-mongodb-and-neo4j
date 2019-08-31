#-*- coding: utf-8 -*-
import xml.etree.cElementTree as cElementTree
import time
import csv

if __name__ == '__main__':
    start_time = time.time()

    context = cElementTree.iterparse('dblp_utf8.xml', events=("start", "end"))

    context = iter(context)
    event, root = context.__next__() # get the root element of the XML doc
    with open('authors.csv', 'w') as csv_authors_file, \
            open('titles.csv', 'w') as csv_titles_file, \
            open('relations.csv', 'w') as csv_relations_file:
        writer_authors = csv.writer(csv_authors_file)
        writer_titles = csv.writer(csv_titles_file)
        writer_relations = csv.writer(csv_relations_file)

        writer_authors.writerow(['authorID:ID', 'author', ':LABEL'])
        writer_titles.writerow(['titleID:ID', 'title', 'Type:LABEL'])
        writer_relations.writerow([':START_ID', 'year:INT', ':END_ID', ':TYPE'])

        for event, elem in context:
            temp_dict = {}
            if event == "end":
                if elem.tag in ['article', 'inproceedings', 'incollection']: # i want to write out all <bucket> entries
                    article_type = elem.tag
                    for inner_elem in iter(elem):
                        if inner_elem.tag == 'title':
                            if inner_elem.text is not None:
                                title = inner_elem.text
                                concat_title = title + article_type
                                title_id = abs(hash(concat_title))
                                writer_titles.writerow([title_id, title, article_type])
                        elif inner_elem.tag == 'year':
                            if inner_elem.text is not None:
                                year = inner_elem.text
                    for inner_elem in iter(elem):
                        if inner_elem.tag == 'author':
                            if inner_elem.text is not None:
                                author = inner_elem.text
                                author_id = abs(hash(author))
                                writer_authors.writerow([author_id, author, 'Author'])
                                writer_relations.writerow([author_id, int(year), title_id, 'PUBLISHED'])
                                print([author_id, int(year), title_id, 'PUBLISHED'])
            root.clear()  # when done parsing a section clear the tree to safe memory
    csv_authors_file.close()
    csv_titles_file.close()
    csv_relations_file.close()
    print("time elapsed: {:.2f}s".format(time.time() - start_time))
