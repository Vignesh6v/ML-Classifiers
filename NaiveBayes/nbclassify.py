from os import walk
from os.path import join
import sys
import re
from math import log10

#read and store parameters from intermediate file
#2,2 classify
prior_prob={'Pos':0,'Neg':0,'Truth':0,'Dec':0}
cond_prob={'Pos':{},'Neg':{},'Truth':{},'Dec':{}}
read=open('nbmodel.txt', 'r').readlines()
lnum=0
for line in read:
    line=line.strip()
    data=line.split()
    if lnum<4:
        prior_prob[data[0]]=float(data[1])
    else:
        for eachD in range(1,len(data),2):
            cond_prob[data[0]][data[eachD]]=float(data[eachD+1])
    lnum+=1

#read test file as words
f=[]
def read_all_files(path):
    for (dirpath, dirnames, filenames) in walk(path):
        for directory in dirnames:
            read_all_files(join(dirpath,directory))
        for file in filenames:
            if file.endswith(".txt") and file!='README.txt':
                f.append(join(dirpath,file))
        break
path=str(sys.argv[1])
read_all_files(path)

wr=open('nboutput.txt','w')
for file in f:
    NBprob={'Pos':log10(prior_prob['Pos']),'Neg':log10(prior_prob['Neg']),'Truth':log10(prior_prob['Truth']),'Dec':log10(prior_prob['Dec'])}
    rd=open(file,'r').readlines()
    for line in rd:
        line=line.strip()
        line=re.sub('[,.!?#\-:;$"]', '', line)
        line=re.sub('[\[\]\/{}()]',' ',line)
        words=line.split()
        for lab in prior_prob:
            for word in words:
                word=word.lower()
                if word.endswith('s') and not word.endswith('ss'):
                    word=word[:-1]
                if word not in cond_prob[lab].keys():
                    continue
                if word.isupper():
                    NBprob[lab]+=log10(cond_prob[lab][word])
                NBprob[lab]+=log10(cond_prob[lab][word])

#pick max of label
#write into output file
    if NBprob['Truth']>NBprob['Dec']:
        wr.write('truthful ')
    else:
        wr.write('deceptive ')
    if NBprob['Pos']>NBprob['Neg']:
        wr.write('positive ')
        wr.write(file)
        wr.write('\n')
    else:
        wr.write('negative ')
        wr.write(file)
        wr.write('\n')
wr.close()
