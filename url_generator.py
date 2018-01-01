import urllib
import os
import re

#convert bytes to kb
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("Wrong format")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


syllabus = '0620'
years = ['_s10_','_s11_','_s12_', '_s13_','_s14_','_s15_','_w10_','_w11_','_w12_','_w13_','_w14_','_w15_']
mps = ['ms_', 'qp_']
papers = []
for number1 in range(1,6):
    for number2 in range(1,4):
        papers.append(str(number1)+str(number2))

#at the end, the '/' must be included
service_url = "http://igcse-cie1.stor.sinaapp.com/Chemistry%20(0620)/"
location = r'/Users/yujie/Desktop/Pastpapers/0620-IG Chem'
name = re.findall('([(][0-9]+[)])', service_url)[0][1:5]

if name == syllabus:

    #name pastpapers
    pastpapers = []
    for year in years:
        for mp in mps:
            for paper in papers:
                pastpapers.append(str(syllabus)+year+mp+paper)
    print pastpapers

    #downloader

    for pastpaper in pastpapers:
        file_name = pastpaper + '.pdf'
        if os.path.exists(location + '/' + file_name):
            print 'file exists'
            continue
        else:
            try:
                print 'downloading: ', file_name
                dest_dir = os.path.join(location, file_name)
                url = service_url+file_name
                print url
                urllib.urlretrieve(url, dest_dir)

            except:
                print 'download fails'

    print 'download finishes'


    #remove the file smaller than 10k
    for pastpaper in pastpapers:
        try:
            size = os.path.getsize(location+'/'+pastpaper+'.pdf')
            print pastpaper,' ', formatSize(size)
            if size < 10240:
                print pastpaper, ' is broken'
                os.remove(location+'/'+pastpaper+'.pdf')
        except:
            print pastpaper, ' file not found'

    print 'file check is completed'

else:
    print '====== Wrong syllabus entered ======'
