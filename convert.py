import re
import gzip
import html.entities

entities={k:v for k,v in html.entities.entitydefs.items() if v not in "&'\"<>"}

entity_re=re.compile("&([^;]+);")

def resolve_entity(m):
    try:
        return entities[m.group(1)]
    except KeyError:
        return m.group(0)

def expand_line(line):
    return entity_re.sub(resolve_entity,line)

def recode_file(src,dst):
    with gzip.open(src,mode="rt", encoding="ISO-8859-1", newline="\n") as src_file:
        with gzip.open(dst, mode="wt", encoding="UTF-8", newline="\n") as dst_file:
            first_line=src_file.readline()
            recoded_first_line=first_line.replace("ISO-8859-1","UTF-8")
            if first_line==recoded_first_line:
                raise ValueError("Source file seems to not be encoded in ISO-8859-1")
            dst_file.write(recoded_first_line)
            for line in src_file:
                dst_file.write(expand_line(line))


recode_file("dblp.xml.gz","dblp_utf8.xml.gz")