# -*- coding: UTF-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import clips

from planner.core.models import Institution

def index(request):
	#clips.Reset()
	#clips.Assert("(prayook)")
	#clips.Assert("(kidkung)")
	print 'I will try thai in the next line'
	print 'ทดสอบภาษาไทย ทำได้แล้วจริงๆนะ'.decode("UTF-8")
	
	queryset = Institution.objects.all()
	print str(queryset).decode("UTF-8")

	return render_to_response("index.html", {}, context_instance=RequestContext(request))

def run(request):
	clips.Clear()
	clips.BatchStar("C:/Users/multiply/Documents/Work/2553/AI/lab01/lab01.clp")
	clips.Reset()
	clips.Assert(request.POST["code"])
	clips.Run()
	facts = clips.FactList()
	return render_to_response("run.html", {'facts': facts, 'stdout': clips.StdoutStream.Read()}, context_instance=RequestContext(request))