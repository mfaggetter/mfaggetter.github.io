#!/usr/bin/python
# Program to convert a bibtex file (3dc_pubs.bib) into html for the 3D Chirp website.

'''
Written for Python 2.7.x and requires only a vanilla installation.

This program searches for article, thesis and conference entries in the bibtex file.

It will generate a separate file for each type, with specific names:
    articles.htm; theses.htm; conferences.htm

These files are automatically sorted by year and alphabetically by publication date.

The saved .htm files are automatically inserted into the tabs on the publications page using javascript.
'''

infile = "3dc_pubs.bib"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Define HTML parser
def htag(tag, str): return "<{}>{}</{}>".format(tag,str,tag)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Define class for a bibtex entry:
class reference():

    def __init__(self, entry):
        self.type, self.contents = entry.split('{', 1)
        self.type = self.type.lower()
        self.paired_entries = self.format_contents()
        self.check_complete()
        try:
            self.year = int(self.paired_entries["year"])
        except:
            print "\nFound troublesome formatting in thesis: {}\n".format(self.id)
            print "Year is not an integer"
        self.sort_char = self.paired_entries["author"][0]
        self.self_formatted_HTML = self.html_format()

    def format_contents(self):
        # split entries by lines
        lines = [i.split('=') for i in self.contents.split('\n')]

        if len(lines[0]) == 1:
            self.id = '['+lines[0][0].strip(',')+']'
        else:
            self.id = ' '
        d = dict(filter(lambda x: len(x) == 2, lines))

        # Fix capitalisation and trailing characters/space in dictionary keys
        d = {k.strip().lower(): v for k, v in d.iteritems()}
        # Strip trailing brackets and space from dictionary items
        d = {k: v.strip(' {},') for k, v in d.iteritems()}
        return d

    def check_complete(self):
        ''' Check bibtex entry satisfies minimum required fields '''
        if self.type == 'thesis':
            required = set(['author', 'title', 'institution', 'school', 'year'])
            missing_fields = required.difference(self.paired_entries.keys())
            if len(missing_fields) > 0:
                print "\nFound troublesome formatting in thesis: {}\nMissing fields:".format(self.id)
                for i in missing_fields: print "  "+i
                exit(1)
        elif self.type == 'article':
            required = set(['author', 'title', 'journal', 'volume', 'year'])
            missing_fields = required.difference(self.paired_entries.keys())
            if len(missing_fields) > 0:
                print "\nFound troublesome formatting in article: {}\nMissing fields:".format(self.id)
                for i in missing_fields: print "  "+i
                exit(1)
        elif self.type == 'conference':
            required = set(['author', 'title', 'series', 'address', 'year'])
            missing_fields = required.difference(self.paired_entries.keys())
            if len(missing_fields) > 0:
                print "\nFound troublesome formatting in conference: {}\nMissing fields:".format(self.id)
                for i in missing_fields: print "  "+i
                exit(1)

    def html_format(self):
        if self.type == 'thesis':
            li = "{}, {}, PhD Thesis, {}, {}, {}.".format(self.paired_entries["author"],
                                                     htag("b", self.paired_entries["title"]),
                                                     self.paired_entries["institution"],
                                                     htag("i", self.paired_entries["school"]),
                                                     self.paired_entries["year"])
        elif self.type == 'article':
            li = "{}, {}. {} {}, {}".format(self.paired_entries["author"],
                                            htag("b", self.paired_entries["title"]),
                                            htag("i", self.paired_entries["journal"]),
                                            self.paired_entries["volume"],
                                            self.paired_entries["year"])
            if "pages" in self.paired_entries:
                li += ", {}".format(self.paired_entries["pages"])
            li += '.'
            if "doi" in self.paired_entries:
                li += " (doi:{})".format(self.paired_entries["doi"])
            if "link" in self.paired_entries:
                li += " (<a href='{}' target='_blank'>PDF</a>)".format(self.paired_entries["link"])
        elif self.type == 'conference':
            li = "{}, {}, {}, {}, {}.".format(self.paired_entries["author"],
                                             htag("b", self.paired_entries["title"]),
                                             htag("i", self.paired_entries["series"]),
                                             self.paired_entries["address"],
                                             self.paired_entries["year"])
            if "doi" in self.paired_entries:
                li += " (doi:{})".format(self.paired_entries["doi"])
            if "link" in self.paired_entries:
                li += " (<a href='{}' target='_blank'>PDF</a>)".format(self.paired_entries["link"])
        else:
            print 'Type: "{}" not supported (for entry {}).'.format(self.type, self.id)
            exit(1)

        return htag("li", li)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Load lines in fine: 3dc_pubs.bib

def read_file(fname):
    with open(fname) as f:
        bib = f.read()
    # Create reference object for each bibtex entry and group into categories
    thesis_entries, article_entries, conference_entries = [], [], []
    article_years = []
    for i in filter(None, bib.split('@')):
        t = reference(i)
        if t.type == 'thesis':
            thesis_entries.append(t)
        elif t.type == 'article':
            article_entries.append(t)
        elif t.type == 'conference':
            conference_entries.append(t)

    # Sort all lists by year & first-letter surname
    import operator
    for list in [thesis_entries, article_entries, conference_entries]:
        list.sort(key=operator.attrgetter('sort_char'), reverse=True)
        list.sort(key=operator.attrgetter('year'))
    return thesis_entries, article_entries, conference_entries

def save_html(entries, type):
    # Theses:
    if type == "theses":
        with open('theses.htm', 'w') as ofile:
            ofile.write('<ul class="dashed">\n')
            for n in entries:
                ofile.write("    {}\n".format(n.self_formatted_HTML))
            ofile.write("</ul>")

    # Articles:
    elif type == "articles":
        with open('articles.htm', 'w') as ofile:
            # Organise entries by year under appropriate headings
            heading = entries[-1].year
            pre_2008 = []
            ofile.write(htag("h4",heading))
            ofile.write('\n<ul class="dashed">')
            for n in entries[::-1]:
                if n.year > 2007:
                    if n.year == heading:
                        ofile.write('    ' + n.self_formatted_HTML)
                    else:
                        ofile.write('</ul>\n')
                        ofile.write(htag("h4", str(n.year)))
                        ofile.write('\n<ul class="dashed">')
                        ofile.write('    ' + n.self_formatted_HTML)
                    heading = n.year
                else:
                    pre_2008.append(n)
            ofile.write('</ul>\n')

            #Resort pre-2008 entries by name only
            #import operator
            #entries = entries.sort(key=operator.attrgetter('sort_char'))
            ofile.write(htag("h4","Pre-2008"))
            ofile.write('\n<ul class="dashed">')
            for n in pre_2008:
                ofile.write('    ' + n.self_formatted_HTML)
            ofile.write('</ul>\n')

    # Conferences:
    elif type == 'conferences':
        with open('conferences.htm', 'w') as ofile:
            ofile.write('<ul class="dashed">')
            for n in entries[::-1]:
                ofile.write('    ' + n.self_formatted_HTML)
            ofile.write('</ul>\n')

    else:
        print 'Unidentified bibtex type'


#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

def main():
    thess, arts, confs = read_file(infile)
    save_html(thess, "theses")
    save_html(arts, "articles")
    save_html(confs, "conferences")
    print "Complete"

if __name__ == '__main__':
    main()
