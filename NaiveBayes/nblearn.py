from os import walk
from os.path import join
import sys
import re

def opposite(lab):
    if lab=='Neg':
        return 'Pos'
    elif lab=='Pos':
        return 'Neg'
    elif lab=='Dec':
        return 'Truth'
    else:
        return 'Dec'

#read input file as words
def read_all_files(path):
    for (dirpath, dirnames, filenames) in walk(path):
        print dirpath, dirnames, filenames
        for directory in dirnames:
            read_all_files(join(dirpath,directory))
        for file in filenames:
            if file.endswith(".txt") and file!='README.txt':
                f.append(join(dirpath,file))
        break

f = []
path=str(sys.argv[1])
read_all_files(path)


#2,2way classifier
word_count={'Pos':{},'Neg':{},'Truth':{},'Dec':{}}
total_words={'Pos':0,'Neg':0,'Truth':0,'Dec':0}
label_frequency={'Pos':0,'Neg':0,'Truth':0,'Dec':0}
label_a=''
label_b=''


#keep count of words(per label),totalwords(per label), vocab and labels
for file in f:
    print file
    if file.find('negative')>-1:
        label_a='Neg'
    else:
        label_a='Pos'
    if file.find('deceptive')>-1:
        label_b='Dec'
    else:
        label_b='Truth'
    label_frequency[label_a]+=1
    label_frequency[label_b]+=1


    read=open(file,'r').readlines()
    for line in read:
        line=line.strip()
        line=re.sub('[,.!?#\-:;$"]', '', line)
        line=re.sub('[\[\]\/{}()]',' ',line)
        words=line.split()
        for word in words:
            word=word.lower()
            if word.endswith('s') and not word.endswith('ss'):
                word=word[:-1]
            if word=='':
                continue
            if word in ['a','and','i','in','of','the','to','was','for','it','we','at','that','my','is','this','were','with','had','on','our','they','be','but','have','there','when','no','not','nor','about','again','all','an','are','aren\'t','as','by','can','can\'t','could','did','do','does','has','from','here','if','it\'s','me','couldn\'t','didn\'t','so','doesn\'t','should','don\'t','very','hadn\'t','hasn\'t','haven\'t','will','he\'d','would','you','he\'ll','he\'s','here\'s','how\'s','i\'d','i\'ll','i\'m','i\'ve','isn\'t','it\'s','let\'s','mustn\'t','shan\'t','she\'d','she\'ll','she\'s','shouldn\'t','that\'s','there\'s','they\'d','they\'ll','they\'re','they\'ve','wasn\'t','we\'d','we\'ll','we\'re','we\'ve','weren\'t','what\'s','when\'s','where\'s','who\'s','why\'s','won\'t','wouldn\'t','you\'d','you\'ll','you\'re','you\'ve']:
                continue
            if word not in word_count['Pos'].keys():
                word_count[label_a][word]=1
                word_count[opposite(label_a)][word]=0
                word_count[label_b][word]=1
                word_count[opposite(label_b)][word]=0
            else:
                word_count[label_a][word]+=1
                word_count[label_b][word]+=1

            total_words[label_a]+=1
            total_words[label_b]+=1


#Calc prior and conditional probabilitues(for vocab)- parameters
cond_prob={'Pos':{},'Neg':{},'Truth':{},'Dec':{}}
for lab in total_words:
    for word in word_count[lab]:
        cond_prob[lab][word]=(word_count[lab][word]+1)/(total_words[lab]+len(word_count[lab].keys()))
prior_prob={'Pos':0,'Neg':0,'Truth':0,'Dec':0}

for lab in label_frequency:
    prior_prob[lab]=label_frequency[lab]/len(f)

#write into output file
writeF=open('nbmodel.txt', 'w')
for key,val in prior_prob.items():
    writeF.write(key)
    writeF.write(' ')
    writeF.write(str(val))
    writeF.write('\n')
for lab in total_words:
    writeF.write(lab)
    writeF.write(' ')
    for key,val in cond_prob[lab].items():
        writeF.write(key)
        writeF.write(' ')
        writeF.write(str(val))
        writeF.write(' ')
    writeF.write('\n')
writeF.close()
