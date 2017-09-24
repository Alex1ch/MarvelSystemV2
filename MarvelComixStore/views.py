from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
from MarvelComixStore import forms,models
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate, login, logout
import datetime
import json

# Create your views here.

class Search(DetailView):
    def get(self,request):
        form=forms.searchForm()
        user=request.user
        models.Comic.objects.first().__str__()
        return render(request,'marvel.html',{'form':form, 'user':user})
    def post(self,request):
        Comixes=models.Comic.objects.all()
        form=forms.searchForm(request.POST)

        if form.is_valid():
            keywords_str=form.cleaned_data.get('keywords',None)
            year = form.cleaned_data.get('year',None)
            keywords=keywords_str.split(' ')
            for keyword in keywords:
                Comixes=Comixes.filter(Q(Q(name__icontains=keyword)|Q(description__icontains=keyword)|Q(tags__name__icontains=keyword))).distinct()
            if year!='0':
                print('111')
                Comixes =Comixes.filter(date__year=int(year))

            SerializerList=[models.ComixSerializer(item) for item in Comixes]
            separator="\|/"
            output = (JSONRenderer().render(serializer.data)+separator.encode('ascii') for serializer in SerializerList)

            return HttpResponse(output)
        else:
            return HttpResponse("Oooops")

class Comics(DetailView):
    def get(self,request,*args,**kwargs):
        #comixes=models.Comix.objects.all()
        #comixes.filter(cus)
        user=get_object_or_404(models.User,username=kwargs['username'])
        customer = models.Customer.objects.get(user=user)
        comics=models.Comic.objects.filter(customer=customer)

        context={ 'user':user, 'comics':comics,'authuser':request.user}
        return render(request, 'comics.html', context)

class Master(DetailView):
    def get(self,request,*args,**kwargs):
        #comixes=models.Comix.objects.all()
        #comixes.filter(cus)
        if request.user.is_authenticated():
            customer = models.Customer.objects.get(user=request.user)
            comics=models.Comic.objects.filter(customer=customer)

            context={ 'user':request.user, 'comics':comics,'authuser':request.user}
            return render(request, 'comics.html', context)
        return HttpResponseRedirect(redirect_to='/auth')


class ComicsView(DetailView):
    def get(self,request,*args,**kwargs):
        id=kwargs['id']
        context={'id':id,  'user':request.user}
        return render(request,'comix.html',context)

class Index(DetailView):
    def get(self,requst):
        return HttpResponseRedirect('marvel')

def LogOut(request):
    logout(request)
    return HttpResponseRedirect('marvel')

def get_added(request):
    if not request.user.is_authenticated:
        return HttpResponse("Not authenticated")
    comics=models.Comic.objects.filter(customer__user=request.user)
    added=""
    for comic in comics:
        added+=comic.ean.__str__()+"\n"
    return HttpResponse(added[:-1])

def add(request,*args,**kwargs):
    if not request.user.is_authenticated():
        return HttpResponse('Not authenticated')
    user=request.user
    customer=models.Customer.objects.get(user=user)
    id=kwargs['id']
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    Comic=models.Comic()
    Comic.name=body['title']
    Comic.description=body['description']
    Comic.cover_url=body['cover_url']
    Comic.marvel_id=body['marvel_id']
    Comic.ean=body['ean']
    Comic.characters=body['characters']
    date_raw=body['date']
    Comic.date = datetime.datetime(int(date_raw[:4]),int(date_raw[5:7]),int(date_raw[8:10]))
    Comic.customer=customer
    Comic.save()
    return HttpResponse('Added!')

def delete(request,*args,**kwargs):
    if not request.user.is_authenticated():
        return HttpResponse('Not authenticated')
    models.Comic.objects.get(id=kwargs['id']).delete()
    return HttpResponseRedirect('/master')

class Modify(DetailView):
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            id=kwargs['id']
            comic=get_object_or_404(models.Comic,id=id)
            if comic.customer.user!=request.user:
                return HttpResponseRedirect(redirect_to='/master')
            date=comic.date.year.__str__()+'-'+comic.date.month.__str__()+'-'+comic.date.day.__str__()
            return render(request,'modify.html',{'comic':comic, 'date':date})
        else:
            return HttpResponseRedirect(redirect_to='/auth')

    def post(self, request, **kwargs):
        comic=models.Comic.objects.get(id=kwargs['id'])
        if comic.customer.user!=request.user:
            return HttpResponseRedirect(redirect_to='/master')
        comic.marvel_id=request.POST['marvel_id']
        comic.name=request.POST['name']
        comic.description=request.POST['description']
        comic.characters=request.POST['characters']
        comic.ean=request.POST['ean']
        comic.cover_url=request.POST['cover_url']
        date=request.POST['date'].split('-')
        comic.date=datetime.datetime(year=int(date[0]),month=int(date[1]),day=int(date[2]))
        comic.save()
        return HttpResponseRedirect(redirect_to='/master')