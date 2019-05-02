import os

def cleanData():
    fr = open('sjp-odm\sjp_orginal.txt', 'r',encoding="utf-8")
    fw = open('sjp-odm\sjp_clean.txt', 'w',encoding="utf-8")
    for  line in fr:
        line = line.strip().split(',')
        if line:
            if not line[0].startswith(u'nie'):
                line1 = filter(lambda x: not x.startswith(u'nie'),map(lambda y: y.strip(), line))
                #line2 = list(filter(lambda x: x.startswith(u'nie'),map(lambda y: y.strip(), line)))   
                fw.write(','.join(line1)+"\n")             
                #if len(line2)>0:
                #    fw.write(','.join(line2)+"\n")
            else:
                fw.write(','.join(line)+"\n")


if __name__ == '__main__':
    cleanData()
  
    