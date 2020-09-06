from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from selenium import webdriver
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
urldict = {"Top Stories":"https://timesofindia.indiatimes.com/business/real-estate",
               "Money Control":"https://www.moneycontrol.com/",
               "Magic Bricks":"https://content.magicbricks.com/property-news",
               "Hindu":"https://www.thehindu.com/real-estate/"}
@csrf_exempt
def scrape_news(request):
    driver = webdriver.Chrome()


    source = request.POST["source"]
    if source == "Top Stories":
        try:
            url = urldict[str(source)]
            driver.get(url)

            listinfo = []
            stories = driver.find_elements_by_css_selector("#c_articlelist_stories_1>ul>li>span>a")


            for ul in stories:
                listinfo.append({"title":str(ul.text),"link":str(ul.get_attribute("href")),"source":"Top Stories"})
        except Exception as e:
            print(e)
        try:
            driver.get("https://timesofindia.indiatimes.com/business/real-estate/2")
            stories2 = driver.find_elements_by_css_selector("#c_articlelist_stories_1>ul>li>span>a")
            for ul2 in stories2:
                listinfo.append({"title": str(ul2.text), "link": str(ul2.get_attribute("href")), "source": "Top Stories"})
        except Exception as e:
            print(e)
        try:
            driver.get("https://timesofindia.indiatimes.com/business/real-estate/3")
            stories3 = driver.find_elements_by_css_selector("#c_articlelist_stories_1>ul>li>span>a")
            for ul3 in stories3:
                listinfo.append({"title": str(ul3.text), "link": str(ul3.get_attribute("href")), "source": "Top Stories"})
        except Exception as e:
            print(e)
        try:
            driver.get("https://timesofindia.indiatimes.com/business/real-estate/4")
            stories4 = driver.find_elements_by_css_selector("#c_articlelist_stories_1>ul>li>span>a")
            for ul4 in stories4:
                listinfo.append({"title": str(ul4.text), "link": str(ul4.get_attribute("href")), "source": "Top Stories"})
        except Exception as e:
            print(e)
        listinfo2 = []
        for info in listinfo:
            try:
                news = News()
                try:
                    checktitle = get_list_or_404(News, title=info["title"], source=source)
                    print("Not a new Entry")
                except:
                    print("New entry")
                    listinfo2.append(info)
                    news.title = info["title"]
                    news.url = info["link"]
                    news.source = info["source"]
                    news.save()
            except Exception as e:
                print(e)
        return JsonResponse({"status":"success","count":len(listinfo2),"New Entries":listinfo2})
    elif source != "All":
        url = urldict[str(source)]
        driver.get(url)
        links = driver.find_elements_by_tag_name("a")
        listinfo = []

        for link in links:
            try:
                if link.text and link.get_attribute("href"):
                    if len(link.text.split(" ")) >= 5:
                        try:
                            checktitle = get_list_or_404(News,title=link.text,source=source)
                            print("Not a new Entry")
                        except:
                            print("New Entry")

                            listinfo.append({"title":link.text,"link":link.get_attribute("href"),"source":str(source)})
            except Exception as e:
                print(e)
        for info in listinfo:
            try:
                news = News()
                news.title = info["title"]
                news.url = info["link"]
                news.source = info["source"]
                news.save()
            except Exception as e:
                print(e)
        return JsonResponse({"status":"success","Count":len(listinfo),"New Entry":listinfo})
    elif source == "All":
        listinfo = []
        for source,urlsource in urldict.items():
            driver.get(urlsource)
            links = driver.find_elements_by_tag_name("a")


            for link in links:
                try:
                    if link.text and link.get_attribute("href"):
                        if len(link.text.split(" ")) >= 5:
                            try:
                                checktitle = get_list_or_404(News, title=link.text, source=source)
                                print("Not a new Entry")
                            except:
                                print("New Entry")

                                listinfo.append(
                                    {"title": link.text, "link": link.get_attribute("href"), "source": str(source)})
                except Exception as e:
                    print(e)
            for info in listinfo:
                try:
                    news = News()
                    news.title = info["title"]
                    news.url = info["link"]
                    news.source = info["source"]
                    news.save()
                except Exception as e:
                    print(e)
        return JsonResponse({"status": "success", "Count": len(listinfo), "New Entry": listinfo})


@csrf_exempt
def indexpageforscrape(request):
    listsources = []
    listsources = urldict.keys()
    return render(request,"getpageforscrape.html",{"listsources":listsources})

@csrf_exempt
def index(request):
    return render(request,"index.html")

@csrf_exempt
def results(request,source):
    #source = request.GET("source")
    results = []
    if source == "All":
        results = News.objects.all()
    else:
        results = News.objects.filter(source=source)

    return render(request,"index.html",{"results":results,"source":source})



