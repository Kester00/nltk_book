#!/usr/bin/python
#
# combine_indices.py
#
# Combine the HTML indices from multiple docbook documents.
#

import sys, os, os.path, re

HEADER = '''\
<?xml version="1.0"?>
<!DOCTYPE index PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
"../docbook/sgml/docbook/xml-dtd-4.2/docbookx.dtd" [
]>

<!-- This unified index was automatically generated by combine_indices.py -->
<!-- The unified index is represented as a single docbook article.  It -->
<!-- can be used to generate an HTML index.  However, it can *not* be -->
<!-- used to generate a LaTeX/pdf index.  Attempts to do so will have -->
<!-- undefined results. -->

<index id="tutorial_index">
<!-- Hack: use superscript to make the title smaller -->
<title> <superscript><ulink url="index.html">
           NLTK Tutorials</ulink>: Term Index
        </superscript></title>
'''

FOOTER = '''\
</index>
'''

indexentry_re = re.compile('<indexentry>[\s\S]*?</indexentry>')
url_re = re.compile('url="')

entries = []
tut = None
def add_entry(match):
    s = url_re.sub('url="%s/' % tut, match.group(0))
    entries.append(s)
    return ''

def combine(inputs, output):
    global tut
    for input in inputs:
        tut = os.path.split(os.path.split(input)[0])[1]
        indexentry_re.sub(add_entry, open(input, 'r').read())

    out = open(output, 'w')
    out.write(HEADER)

    # This isn't terribly efficient, but it doesn't matter much:
    entries.sort(lambda a,b: cmp(a.lower(), b.lower()))
                 
    for entry in entries:
        print >>out, entry
    out.write(FOOTER)
    out.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s <in-1> <in-2> ... <in-n> <out>' % sys.argv[0]
    out = sys.argv[-1]
    ins = sys.argv[1:-1]
    combine(ins, out)
    
