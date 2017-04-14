#! /usr/bin/python
# -*- coding: utf-8 -*-
import pdb, os, glob, codecs, re, argparse, random, sys

main_folder_wav = sys.argv[1]
main_folder_annot = sys.argv[2]
data_folder = sys.argv[3]
os.system('rm -rf '+data_folder+' && '+'mkdir -p '+data_folder)
suffix='train'
speaker_list={}
speaker_cnt=0
unk_cnt=0
train_annotated_data=['comp-o']

new_txt = ''
new_seg = ''
new_utt = ''
new_wav = ''
os.system('mkdir -p '+data_folder+'/'+suffix+'_cgn/')
fid_txt = codecs.open(data_folder+'/'+suffix+'_cgn/text',"w","utf-8")
fid_seg = codecs.open(data_folder+'/'+suffix+'_cgn/segments',"w","utf-8")
fid_utt = codecs.open(data_folder+'/'+suffix+'_cgn/utt2spk',"w","utf-8")
fid_wav = codecs.open(data_folder+'/'+suffix+'_cgn/wav.scp',"w","utf-8")

for task in train_annotated_data:
    init_trans = main_folder_annot + task
    filelist=glob.glob(init_trans+"/nl/*.ort")
    for filename in filelist:
        cnt3=0
        cnt2=0
        temp = filename.split('/')
        utt_id = temp[-1][:-4]
        flag=0
        flag2=0
        new_wav = new_wav+task+'_'+utt_id+' '+main_folder_wav+task+'/nl/'+utt_id+'.wav'+'\n'
        cnt=4
        speaker_flag=0

        for line in codecs.open(filename,'r','iso-8859-1'):
            if u'"IntervalTier"' in line:
                cnt2=cnt2+1
                speaker_flag=1
                flag=0
                cnt=4
                continue
            if u'"BACKGROUN' in line or u'"COMMEN' in line:
                break
            if speaker_flag==1:
                speaker_code=line.split(u'''"''')[1].lower()  
                if speaker_code==u'unknown':
                    speaker= 'cu'+unicode(str("{:04.0f}".format(unk_cnt)),"utf-8")
                    if speaker not in speaker_list.keys():
                        speaker_list[speaker] = 'cu'+unicode(str("{:04.0f}".format(unk_cnt)),"utf-8")
                        unk_cnt=unk_cnt+1                               
                    speaker=speaker_list[speaker]
                    speaker_flag=0
                else:
                    speaker= 'cg'+speaker_code
                    if speaker not in speaker_list.keys():
                        speaker_list[speaker] = 'cg'+unicode(str("{:04.0f}".format(speaker_cnt)),"utf-8")
                        speaker_cnt=speaker_cnt+1
                    speaker=speaker_list[speaker]
                    speaker_flag=0

    	    if cnt2<1:
                continue
            if cnt>0 and flag==0:
                cnt=cnt-1
                flag=0
                continue
            else:
                flag=1
                cnt=cnt+1           
            if cnt%3==1:
                s_time = unicode(str("{:.3f}".format(float(line))))
                continue
            if cnt%3==2:
                e_time = unicode(str("{:.3f}".format(float(line))))
                continue
            if cnt%3==0:
                if u'""' in line or float(e_time)-float(s_time) < 0.15 or u'"nsp"' in line:
                    continue
                text=line[1:-3]
                text=text.replace(u'-',u' ').replace(u'\xb1',u'').replace(u'\xd7',u'').replace(u'\xb3',u'').replace(u'–',u' ').replace(u'$', u'dollar').replace(u'%',u' procent').replace(u' & ',u' en ').replace(u'&amp',u' en ').replace(u'&',u' en ').replace(u'\x90',u' ').replace(u'\x91',u' ').replace(u'\x92',u' ').replace(u'\x93',u' ').replace(u'\x94',u' ').replace(u'\x95',u' ').replace(u'\x96',u' ').replace(u'\x97',u' ').replace(u'\x98',u' ').replace(u'\x99',u' ').replace(u'\xbd',u'').replace(u'\xff',u'').replace(u'\u2663',u'').replace(u'\u2666',u'').replace(u'\u2660',u'').replace(u'\u2665',u'').replace(u'\xb9',u'').replace(u'\xb2',u'').replace(u'\u2070',u'').replace(u'\u2079',u'').replace(u'\u2074',u'').replace(u'\u0660',u'').replace(u'\u2075',u'').replace(u'\u2071',u'').replace(u'\u2072',u'').replace(u'\u2073',u'').replace(u'\u2076',u'').replace(u'\u2077',u'').replace(u'\u2078',u'').replace(u'\u2792',u'').replace(u'\u2082',u'').replace(u"1/2","half").replace(u"/",u" ").replace(u'~',u'')
                text = u"".join(c for c in text if c not in  (u'!',u'.',u':',u'?',u',',u'\n',u'\r',u'"',u'|',u';',u'(',u')',u'[',u']',u'{',u'}',u'#',u'_',u'+',u'&lt',u'&gt',u'\\'))
                fields = text.lower().split()
                for ele in fields:
                    if u'*' in ele or u'xxx' in ele or u'mm' in ele or u'uh' in ele or u'eh' in ele:
                        ind=fields.index(ele)
                        fields[ind]=u'spn'
                    elif u'ggg' in ele:
                        ind=fields.index(ele)
                        fields[ind]=u'nsn'
                text = u' '.join(fields)
                temp=text.strip().lower().split()
                text = u' '.join(temp)
                if text!=u'spn' and text!=u'' and text!=u'nsn':
                    new_txt = new_txt+speaker+u'_'+task+u'_'+utt_id+u'_'+unicode(str("{:04.0f}".format(cnt3)))+u' '+text+u'\n'
                    new_seg = new_seg+speaker+u'_'+task+u'_'+utt_id+u'_'+unicode(str("{:04.0f}".format(cnt3)))+u' '+task+u'_'+utt_id+u' '+s_time+u' '+e_time+u'\n'
                    new_utt = new_utt+speaker+u'_'+task+u'_'+utt_id+u'_'+unicode(str("{:04.0f}".format(cnt3)))+u' '+speaker+u'\n'
                cnt3=cnt3+1
            if cnt3%300:
                fid_txt.write(new_txt)
                fid_seg.write(new_seg)
                fid_utt.write(new_utt)
                fid_wav.write(new_wav)
                new_txt = ''
                new_seg = ''
                new_utt = ''
                new_wav = ''
fid_txt.write(new_txt)
fid_seg.write(new_seg)
fid_utt.write(new_utt)
fid_wav.write(new_wav)
fid_txt.close()
fid_seg.close()
fid_utt.close()
fid_wav.close()

os.system('env LC_ALL=C sort -o '+data_folder+'/'+suffix+'_cgn/text'+' '+data_folder+'/'+suffix+'_cgn/text')
os.system('env LC_ALL=C sort -o '+data_folder+'/'+suffix+'_cgn/segments'+' '+data_folder+'/'+suffix+'_cgn/segments')
os.system('env LC_ALL=C sort -o '+data_folder+'/'+suffix+'_cgn/wav.scp'+' '+data_folder+'/'+suffix+'_cgn/wav.scp')
os.system('env LC_ALL=C sort -o '+data_folder+'/'+suffix+'_cgn/utt2spk'+' '+data_folder+'/'+suffix+'_cgn/utt2spk')
os.system('utils/utt2spk_to_spk2utt.pl '+data_folder+'/'+suffix+'_cgn/utt2spk'+' > '+data_folder+'/'+suffix+'_cgn/spk2utt')
