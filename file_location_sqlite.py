import sqlite3
import os
import os.path

conn = sqlite3.connect('file_location.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS File;

CREATE TABLE File (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    file_name    TEXT UNIQUE,
    location    TEXT UNIQUE,
    syllabus   INTEGER,
    subject    TEXT,
    year   INTEGER,
    month   TEXT,
    paper_number   INTEGER,
    component  INTEGER,
    type   TEXT

);

''')

rootdir = r"/admin/ksxzs/Pastpapers"

for parent, dirnames, filenames in os.walk(rootdir):
    for dirname in dirnames:
        dir = rootdir + '/' + dirname
        print dir
        for Parent, Dirname, FileNames in os.walk(dir):
            for FileName in FileNames:
                if FileName.startswith(".DS"):
                    continue
                location = dir + '/' + FileName
                paper = FileName.split('.')[0]
                file_name = str(paper)
                syllabbus = paper.split('_')[0]
                dict = {'0417': 'ICT', '0450': 'IBiz', '0455': 'IEcon', '0500': 'Eng1', '0511': 'Eng2', '0580': 'IMath',
                        '0610': 'IBio', '0620': 'IChem', '0625': 'IPhy', '9231': 'FM', '9608': 'CS', '9609': 'ABiz',
                        '9695': 'Lit', '9698': 'Psy', '9700': 'ABio', '9701': 'AChem', '9702': 'APhy', '9708': 'AEcon',
                        '9709': 'AMath'}
                subject = dict[str(syllabbus)]
                year = '20' + paper.split('_')[1][1::]
                month = paper.split('_')[1][0]
                paper_number = int(str(paper.split('_')[3])[0])
                component = paper.split('_')[3]
                type = paper.split('_')[2]
                '''print file_name
                print location
                print syllabbus
                print subject
                print year
                print month
                print paper_number
                print component
                print type'''

                cur.execute('''INSERT OR IGNORE INTO File (file_name, location, syllabus, subject, year, month, paper_number, component, type)
                        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (file_name, location, syllabbus, subject, year, month, paper_number, component, type))
        conn.commit()
