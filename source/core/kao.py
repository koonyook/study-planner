# -*- coding: UTF-8 -*-
import clips
from sets import Set
from settings import PROJECT_ROOT
from planner.core.models import Institution,Course,Subject,Group
import math
def returnMatches(small,big,now):
    if len(small)==0:
        return True
    else:
        for p in small:
            s=[]
            for sub in p.subjects.all():
                s.append(str(sub.code))
            if p.is_parallelable:
                if list(set(s) & (set(now)|set(big))) == s :
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
    s=sorted(kud,key=lambda unit: unit[3],reverse=True)
    s=sorted(s,key=lambda pre:pre[2],reverse=True)
    s=sorted(s,key=lambda level:level[1],reverse=True)
    return s
def run(subjects,profiles,timeline,summer_course=False):
    queryset = Institution.objects.get(name=profiles.institution)
    print str(queryset).decode("UTF-8")
    clips.Clear()
    clips.BatchStar(PROJECT_ROOT+"clips/"+"rulebase.clp")
    text=''
    prelaew=[]
    course=Course.objects.get(name=profiles.course)
    for subject in course.required_subjects.all():
        text += '(subject (name "%s") (code "%s") (prerequisite' % (subject.name, subject.code)
        for pre in subject.prerequisites.all():
            prelaew.append(pre)
            for s in pre.subjects.all():
                text+=' "'+s.code+'"'
        text+='))\n'
    for group in course.required_groups.all():
        for subject in group.subjects.all():
            text += '(subject (name "%s") (code "%s") (prerequisite' % (subject.name, subject.code)
            for pre in subject.prerequisites.all():
                prelaew.append(pre)
                for s in pre.subjects.all():
                    text+=' "'+s.code+'"'
            text+='))\n'
    clips.BuildDeffacts('database', text.encode('cp874'))
    clips.Reset()
    clips.Run()
    facts = clips.FactList()
    subject_sort=[('end',0)]
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
    grouplearned={} # list of group and require unit
    grouplearned['free']=course.required_free_subject_units
    allgroup={} #group code and group name for check something
    for group in course.required_groups.all():
        grouplearned[group.name]=group.required_units
        for subject in group.subjects.all():
            allgroup[str(subject.code)]=group.name
    subject_sort.pop()
    course_require=[]
    for sub in course.required_subjects.all():
        course_require.append(str(sub.code))
    for sub in subjects:
        learned.append(str(sub.code))
        if str(sub.code) in allgroup.keys():
            if grouplearned[allgroup[str(sub.code)]]>0:
                grouplearned[allgroup[str(sub.code)]]-=unit(str(sub.code))
            else:
                grouplearned['free']-=unit(str(sub.code))
        elif str(sub.code) not in course_require:
            grouplearned['free']-=unit(str(sub.code))
    for n in range((profiles.year-1)*3+profiles.semester-1,len(timeline)):
###first
        if summer_course!=False or n%3!=2:
            kud=[]
            for sub in subject_sort:
                if  sub[0] not in allgroup.keys():
                    subject=Subject.objects.get(code=sub[0])
                    if subject.years_available-1<=n/3 and str(subject.code) not in learned:
                        if n%3==0 and subject.available_in_first_semester==True:
                            kud.append(sub)
                        elif n%3==1 and subject.available_in_second_semester==True:
                            kud.append(sub)
                        elif n%3==2 and subject.available_in_summer_semester==True:
                            kud.append(sub)
            kud=sort_pri(kud)   # sort primary
            for sub in kud:
                subject=Subject.objects.get(code=sub[0])
                if returnMatches(subject.prerequisites.all(),learned,timeline[n][0]) and timeline[n][1]-subject.units>=0:
                    timeline[n][0].append(str(subject.code))
                    timeline[n][1]-=subject.units
    ### second
            kud=[]
            for sub in subject_sort:
                if sub[0] in allgroup.keys():
                    subject=Subject.objects.get(code=sub[0])
                    if subject.years_available-1<=n/3 and subject.code not in learned and grouplearned[allgroup[sub[0]]]>0:
                        if n%3==0 and subject.available_in_first_semester==True:
                            kud.append(sub)
                        elif n%3==1 and subject.available_in_second_semester==True:
                            kud.append(sub)
                        elif n%3==2 and subject.available_in_summer_semester==True:
                            kud.append(sub)
            kud=sort_pri(kud)
            for sub in kud:
                subject=Subject.objects.get(code=sub[0])
                if returnMatches(subject.prerequisites.all(),learned,timeline[n][0]) and timeline[n][1]-subject.units>=0 and grouplearned[allgroup[sub[0]]]>0:
                    timeline[n][0].append(str(subject.code))
                    timeline[n][1]-=subject.units
                    grouplearned[allgroup[sub[0]]]-=subject.units
    ### third
            kud=[]
            for sub in subject_sort:
                if sub[0] in allgroup.keys() and grouplearned[allgroup[sub[0]]]<=0:
                    subject=Subject.objects.get(code=sub[0])
                    if subject.years_available-1<=n/3 and subject.code not in learned:
                        if n%3==0 and subject.available_in_first_semester==True:
                            kud.append(sub)
                        elif n%3==1 and subject.available_in_second_semester==True:
                            kud.append(sub)
                        elif n%3==2 and subject.available_in_summer_semester==True:
                            kud.append(sub)
            kud=sort_pri(kud)
            for sub in kud:
                subject=Subject.objects.get(code=sub[0])
                if returnMatches(subject.prerequisites.all(),learned,timeline[n][0]) and timeline[n][1]-subject.units>=0 and grouplearned['free']>0:
                    if str(subject.code) not in timeline[n][0]:
                        print sub[0]
                        timeline[n][0].append(str(subject.code))
                        timeline[n][1]-=subject.units
                        grouplearned['free']-=subject.units
            for sub in timeline[n][0]:
                learned.append(sub)
### end
    for i in grouplearned.keys():
        print i,grouplearned[i]
        if grouplearned[i]>0:
            return False
    chk=[]
    for sub in course.required_subjects.all():
        chk.append(str(sub.code))
    for i in chk:
        if i not in learned:
            print i
    if (set(chk) & set(learned)) !=set(chk):
        return False
    
    return timeline
def newtimeline(profile,summer=False):
    course=profile.course
    timeline=[]
    for i in range(4):
        timeline.append([[],course.units_limit_in_first_semester])
        timeline.append([[],course.units_limit_in_second_semester])
        timeline.append([[],course.units_limit_in_summer_semester])
    return timeline[:]
def get_recommended_subjects(subjects,prefer_sparse_schedule,profile):
    summer=False
    c=-1
    results=[]
    course=profile.course
    course_require=[]
    for sub in course.required_subjects.all():
        course_require.append(str(sub.code))
    if profile.semester!=3:
        timeline=newtimeline(profile)
        answer=run(subjects,profile,timeline)
    else:
        timeline=newtimeline(profile)
        summer=True
        answer=run(subjects,profile,timeline,True)
    if answer==False:
        while answer==False:
            timeline=newtimeline(profile,True)
            summer=True
            c+=1
            for i in range(c):
                timeline.append([[],course.units_limit_in_first_semester])
                timeline.append([[],course.units_limit_in_second_semester])
                timeline.append([[],course.units_limit_in_summer_semester])
            answer=run(subjects,profile,timeline,True)
    timeline=answer
    unit_can_free=0
    if prefer_sparse_schedule==True:
        if summer==False:
            for i in reversed(range(2,12,3)):
                    del timeline[i]
        for i in range((profile.year-1)*3+profile.semester-1,len(timeline)):
            unit_can_free+=timeline[i][1]
        unit_can_free=unit_can_free*1.0/len(timeline)
        print unit_can_free
        unit_can_free=int(math.ceil(unit_can_free))
        for i in range(len(timeline)-1,-1,-1):
            find_pre=[]
            for j in timeline[i][0]:
                subject=Subject.objects.get(code=j)
                for pre in subject.prerequisites.all():
                    for sub in pre.subjects.all():
                        find_pre.append(str(sub.code))
            for j in range(i-1,-1,-1):
                for sub in timeline[j][0]:
                    subject=Subject.objects.get(code=sub)
                    for pre in subject.prerequisites.all():
                        for sub2 in pre.subjects.all():
                            find_pre.append(str(sub2.code))
                for sub in reversed(timeline[j][0][:]):
                    subject=Subject.objects.get(code=sub)
                    if sub not in find_pre:
                        if summer==True:
                            if (subject.available_in_first_semester==True and i%3==0)or(subject.available_in_second_semester==True and i%3==1)or(subject.available_in_summer_semester==True and i%3==2):
                                    if timeline[i][1]-unit(sub)>=unit_can_free and timeline[i][0]!=[]:
                                        if sub not in course_require:
                                            print 'now=%d source=%d code=%s' %(i,j,sub)
                                            timeline[j][0].remove(sub)
                                            timeline[j][1]+=unit(sub)
                                            timeline[i][0].append(sub)
                                            timeline[i][1]-=unit(sub)
                        else:
                            if (subject.available_in_first_semester==True and i%2==0)or(subject.available_in_second_semester==True and i%2==1):
                                    if timeline[i][1]-unit(sub)>=unit_can_free: #and timeline[j][1]<unit_can_free:
                                        if sub not in course_require:
                                            print 'now=%d source=%d code=%s' %(i,j,sub)
                                            timeline[j][0].remove(sub)
                                            timeline[j][1]+=unit(sub)
                                            timeline[i][0].append(sub)
                                            timeline[i][1]-=unit(sub)
    if summer==False and prefer_sparse_schedule==True:
        for i in range(2,12,3):
            timeline.insert(i,[[],7])
    for i in range(len(timeline)):
        if timeline[i][0]!=[]:
            if i%3==2:
                results.append({'year':(i/3)+1,'semester':'summer','subjects': Subject.objects.filter(code__in=timeline[i][0])})
            else:
                results.append({'year':(i/3)+1,'semester':(i%3)+1,'subjects': Subject.objects.filter(code__in=timeline[i][0])})
    return results
