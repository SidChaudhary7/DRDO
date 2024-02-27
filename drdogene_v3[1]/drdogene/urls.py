"""drdogene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from genepro.views import index,contact,search,stats,detail,tutorial,query,result,sslinfo,searchtf,searchge,resulttf,resultge,resultdrug,searchdrug,resultdibi,resultontogoid,resultontoterm,searchontogoid,searchontoterm,searchpathwayid,searchpathwayterm,resultpathwayid,resultpathwayterm,mirdetail,addform

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index,name='index'),
    url(r'^contact/', contact, name='contact'),
    url(r'^search/', search, name='search'),
    url(r'^tutorial/', tutorial, name='tutorial'),
    url(r'^stats/', stats, name='stats'),
    url(r'^searchtf/', searchtf, name='searchtf'),
    url(r'^searchge/', searchge, name='searchge'),
    url(r'^addform/', addform, name='addform'),
    url(r'^searchdrug/', searchdrug, name='searchdrug'),
    url(r'^searchonto/term', searchontoterm, name='searchontoterm'),
    url(r'^searchonto/goid', searchontogoid, name='searchontogoid'),
    url(r'^searchpath/term', searchpathwayterm, name='searchpathwayterm'),
    url(r'^searchpath/kegid', searchpathwayid, name='searchpathwayid'),
    url(r'^detail/', detail, name='detail'),
    url(r'^mir-detail/(?P<pk>[a-zA-Z0-9a-z-]+)/$', mirdetail, name='mir-detail'),
    url(r'^query/', query, name='query'),
    url(r'^sslinfo/', sslinfo, name='sslinfo'),
    url(r'^result/tf/',  resulttf, name='resulttf'),
    url(r'^result/gene/',  resultge, name='resultge'),
    url(r'^result/drug/',  resultdrug, name='resultdrug'),
    url(r'^result/dibi/',  resultdibi, name='resultdibi'),
    url(r'^result/ontology/term',  resultontoterm, name='resultontoterm'),
    url(r'^result/ontology/goid',  resultontogoid, name='resultontogoid'),
    url(r'^result/pathway/term',  resultpathwayterm, name='resultpathwayterm'),
    url(r'^result/pathway/keggid',  resultpathwayid, name='resultpathwayid'),
    url(r'^result/(?P<q_r>[a-zA-Z0-9]+)/(?P<q_p>[a-zA-Z]+)$', result, name='result'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
