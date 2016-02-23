from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
#from django.core.context_processors import csrf
from .models import Page,Tag
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
import markdown
from django.template import RequestContext

from django import forms

class SearchForm(forms.Form):
	text=forms.CharField(label='Enter search term')
	search_content=forms.BooleanField(label='search content',required=False)
#@csrf_protect
def search_page(request):
	if request.method=='POST':
		f=SearchForm(request.POST)
		print f.is_valid()
		if not f.is_valid():
			return render(request,'search.html',{'form':f})#,context_instance=RequestContext(request))
		else:
			#print 'Page.all=',f.cleaned_data['text']
			for i in Page.objects.all():
				print i
			pages=Page.objects.filter(name__contains=f.cleaned_data['text'])
			contents=[]
			if f.cleaned_data['search_content']:
				contents=Page.objects.filter(content__contains=f.cleaned_data['text'])
			for i in pages.all():
				print i
			print 'pages=',pages
			return render(request,'search.html',{'form':f,'pages':pages,'contents':contents})#,context_instance=RequestContext(request))		
	f=SearchForm()
	return render(request,'search.html',{'form':f})#,context_instance=RequestContext(request))

specialPages={'SearchPage':search_page}
# Create your views here.
def view_page(request,page_name):
	if page_name in specialPages:
		return specialPages[page_name](request)
	try:
		page=Page.objects.get(pk=page_name)
		tags=page.tags.all()
	except Page.DoesNotExist:
		return render_to_response('create.html',{'page_name':page_name})
	content=page.content
	return render_to_response('view.html',{'page_name':page_name,'content':markdown.markdown(content),'tags':tags})

@csrf_protect
def edit_page(request,page_name):
	try:
		page=Page.objects.get(pk=page_name)
		content=page.content
		tags=' '.join([tag.name for tag in page.tags.all()])
		#print 'content:',content
	except Page.DoesNotExist:
		content=''
		tags=''
	return render(request,'edit.html',{'page_name':page_name,'content':content,'tags':tags})

def save_page(request,page_name):
	content=request.POST['content']
	tag_list=[]
	if 'tags' in request.POST:
		tags=request.POST['tags']
		tag_list=[Tag.objects.get_or_create(name=tag)[0] for tag in tags.split()]
	try:
		page=Page.objects.get(pk=page_name)
		page.content=content
		for tag in tag_list:
			page.tags.add(tag)
	except Page.DoesNotExist:
		page = Page( name=page_name, content=content)
	page.save()
	print 'page_name=',page_name
	return HttpResponseRedirect('/wiki/page/'+page_name+'/')


def view_tag(request,tag_name):
	tag=Tag.objects.get(pk=tag_name)
	pages=tag.page_set.all()
	return render_to_response('tag.html',{'tag_name':tag_name,'pages':pages})



