# -*- coding: UTF-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import clips
import re
from sets import Set
from settings import PROJECT_ROOT
from planner.core.models import Institution,Course,Subject,Group
        #print 'I will try thai in the next line'
        #print 'ทดสอบภาษาไทย ทำได้แล้วจริงๆนะ'.decode("UTF-8")
def returnMatches(small,big,now):
    if len(small)==0:
        return True
    else:
        for p in small:
            s=[]
            for sub in p.subjects.all():
                s.append(str(sub.code))
            if p.is_parallelable:
                if list(set(s) & set(now)) == s :
                    return True
            
            if list(set(s) & set(big)) == s:
                    return True       
    return False
def count_pre(code):
    subject=Subject.objects.get(code=code)
    maxx=0
    for pre in subject.prerequisites.all():
        c=0
        for n in pre.subjects.all():
            c+=1 
        if c>maxx:maxx=c
    return maxx
def unit(code):
    subject=Subject.objects.get(code=code)
    return int(subject.units)
def sort_pri(kud):
    ###k,(str(tmp.Slots['code']),int(level),count_pre(str(tmp.Slots['code']),unit(str(tmp.Slots['code']))
    s=sorted(kud,key=lambda unit: unit[3],reverse=True)
    s=sorted(s,key=lambda pre:pre[2],reverse=True)
    s=sorted(s,key=lambda level:level[1],reverse=True)
    return s
def run(request):
    queryset = Institution.objects.get(name='มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตบางเขน')
    print str(queryset).decode("UTF-8")
    clips.Clear()
    clips.BatchStar(PROJECT_ROOT+"clips/"+"lab05-koon.clp")
        #get subject data to deffacts
    text=''
    prelaew=[]
    course=Course.objects.get(name='หลักสูตรวิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมคอมพิวเตอร์')
    for subject in course.required_subjects.all():
        #text += "".join([[unicode('" ' + s.code + '"') for s in pre.subjects.all()] for pre in subject.prerequisites.all()[:1]])
        text += '(subject (name "%s") (code "%s") (prerequisite' % (subject.name, subject.code)
        for pre in subject.prerequisites.all():
            prelaew.append(pre)
            for s in pre.subjects.all():
                text+=' "'+s.code+'"'
        text+='))\n'
    for group in course.required_groups.all():
        #text += "".join([[unicode('" ' + s.code + '"') for s in pre.subjects.all()] for pre in subject.prerequisites.all()[:1]])
        for subject in group.subjects.all():
            text += '(subject (name "%s") (code "%s") (prerequisite' % (subject.name, subject.code)
            for pre in subject.prerequisites.all():
                prelaew.append(pre)
                for s in pre.subjects.all():
                    text+=' "'+s.code+'"'
            text+='))\n'
    clips.BuildDeffacts('database', text.encode('cp874'))
    clips.Reset()
    #clips.Assert("(abc)")
    #clips.Assert("(def ghi)")
    #clips.Assert(request.POST["code"])
    clips.Run()
    facts = clips.FactList()
    subject_sort=[('end',0)]
    '''for i in facts:
        m = re.search('(?<=level) [-+]?\d+',str(i.PPForm()))
        if m!=None:
    '''
    subject_level=[]
    learned=[]
    for tmp in facts:
        if tmp.Relation=='subject-level':
            subject_level.append(tmp)
            level=tmp.Slots['level']
            k=0
            while subject_sort[k][1]>level:
                k+=1
            subject_sort.insert(k,(str(tmp.Slots['code']),int(level),count_pre(str(tmp.Slots['code'])),unit(str(tmp.Slots['code'])))) ## code/level/pre/unit
    timeline=[[[],course.units_limit_in_first_semester],[[],course.units_limit_in_second_semester],
              [[],course.units_limit_in_first_semester],[[],course.units_limit_in_second_semester],
              [[],course.units_limit_in_first_semester],[[],course.units_limit_in_second_semester],
              [[],course.units_limit_in_first_semester],[[],course.units_limit_in_second_semester]]
    grouplearned={} # list of group and require unit
    allgroup={} #group code and group name for check something
    for group in course.required_groups.all():
        grouplearned[group.name]=group.required_units
        for subject in group.subjects.all():
            allgroup[str(subject.code)]=group.name
    subject_sort.pop()
    for n in range(len(timeline)):
        kud=[]
        for sub in subject_sort:
            if  sub[0] not in allgroup.keys():
                subject=Subject.objects.get(code=sub[0])
                if subject.years_available-1<=n/2 and subject.code not in learned:
                    if n%2==0 and subject.available_in_first_semester==True:
                        kud.append(sub)
                    elif n%2==1 and subject.available_in_second_semester==True:
                        kud.append(sub)
        kud=sort_pri(kud)   # sort primary
        for sub in kud:
            subject=Subject.objects.get(code=sub[0])
            if returnMatches(subject.prerequisites.all(),learned,timeline[n][0]) and timeline[n][1]-subject.units>=0:
                timeline[n][0].append(str(subject.code))
                timeline[n][1]-=subject.units
        for sub in timeline[n][0]:
            learned.append(sub)
### second
        kud=[]
        for sub in subject_sort:
            if sub[0] in allgroup.keys():
                subject=Subject.objects.get(code=sub[0])
                if subject.years_available-1<=n/2 and subject.code not in learned and grouplearned[allgroup[sub[0]]]-unit(sub[0])>=0:
                    if n%2==0 and subject.available_in_first_semester==True:
                        kud.append(sub)
                    elif n%2==1 and subject.available_in_second_semester==True:
                        kud.append(sub)
        kud=sort_pri(kud)
        for sub in kud:
            subject=Subject.objects.get(code=sub[0])
            if returnMatches(subject.prerequisites.all(),learned,timeline[n][0]) and timeline[n][1]-subject.units>=0:
                timeline[n][0].append(str(subject.code))
                timeline[n][1]-=subject.units
                grouplearned[allgroup[sub[0]]]-=subject.units
        for sub in timeline[n][0]:
            learned.append(sub)
### third
    for i in timeline:
        print i
    for i in grouplearned.keys():
        print i,grouplearned[i]
    return render_to_response("run2.html", {'facts': subject_level, 'stdout': clips.StdoutStream.Read()}, context_instance=RequestContext(request))
