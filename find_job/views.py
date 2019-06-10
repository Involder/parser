from django.shortcuts import render
from django.db import IntegrityError
from django.http import Http404
from scraping.utils import *
from scraping.models import *
from scraping.forms import FindVacancyForm



def list_v(request):
    today = datetime.date.today()
    city = City.objects.get(name='Львов')
    speciality = Speciality.objects.get(name='Python')
    qs = Vacancy.objects.filter(city=city.id, speciality=speciality.id,timestamp=today)
    if qs:
        return render(request, 'scraping/list.html', {'jobs': qs})
    return render(request,'scraping/list.html')



def home(request):
    city = City.objects.get(name='Киев')
    speciality = Speciality.objects.get(name='Python')
    url_qs = Url.objects.filter(city=city, speciality=speciality)
    site = Site.objects.all()
    url_w = url_qs.get(site=site.get(name='Work.ua')).url_address
    url_dj = url_qs.get(site=site.get(name='Djinni.co')).url_address
    url_r = url_qs.get(site=site.get(name='Rabota.ua')).url_address
    url_dou = url_qs.get(site=site.get(name='Dou.ua')).url_address
    jobs = []
    jobs.extend(work(url_w))
    jobs.extend(rabota(url_r))
    jobs.extend(dou(url_dou))
    jobs.extend(djinni(url_dj))


    #v = Vacancy.objects.filter(city=city.id, speciality=speciality.id).values('url')
    #url_list = [i['url'] for i in v]
    for job in jobs:
        vacancy = Vacancy(city=city, speciality=speciality, url=job['href'],
                          title=job['title'], description=job['descript'], company=job['company'])
        try:
            vacancy.save()
        except IntegrityError:
            pass

    return render(request,'scraping/list.html' ,  {'jobs': jobs})
