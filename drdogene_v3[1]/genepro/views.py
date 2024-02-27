from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
import numpy as np
from pymongo import MongoClient
from django.core.mail import send_mail
from django.conf import settings
import json

client = MongoClient('localhost:27017')
dbs = client.ntmirnadb

# Create your views here.


def index(request):

    return render(request,'index.html')

def contact(request):

    return render(request,'contact.html')


def query(request):

    return render(request,'query_page.html')

def tutorial(request):

    return render(request,'tutorial.html')

def stats(request):

    return render(request,'stats.html')

def addform(request):
    if request.method=="POST":
        subject        = 'New Data'
        from_email     = settings.DEFAULT_FROM_EMAIL
        message        = 'New Data'
        recipient_list = ["myomirdb@gmail.com"] #self.user.email
        html_message   =  '<p>MIRna human homolog : '+request.POST['mirna']+'</p><p>Muscle atrophy miRna : '+request.POST['musmir']+'</p><p>Experimental Condition : '+request.POST['exp']+'</p><p>Type of model : '+request.POST['tom']+'</p><p>Up/down/Same Regulation : '+request.POST['uds']+'</p><p>Fold Change : '+request.POST['fc']+'</p><p>Diagnostic Biomarker : '+request.POST['dibi']+'</p><p>Site of Expression : '+request.POST['soe']+'</p><p>Duration of experiment : '+request.POST['doe']+'</p><p>Type of Experiment : '+request.POST['toe']+'</p><p>Reference : '+request.POST['ref']+'</p>'

        sent_mail = send_mail(
                          subject,
                          from_email,
                          message,
                          recipient_list,
                          fail_silently=False,
                          html_message=html_message,
                          )
        return render(request,'addform.html',{"mail":1})

    return render(request,'addform.html')

def result(request,q_r,q_p):

    mir=[]
    cor = []

    if q_p == "uds":
        title = "Level of Expression"
    if q_p == "soe":
        title = "Tissue of Expression"
    if q_p == "doe":
        title = "Duration of Experiment"
    if q_p == "tom":
        title = "Model Organism"


    if q_r == "Other":

        fmir = dbs.mirnadata.find({q_p:"HEK293T cell line"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("HEK293T cell line")

        fmir = dbs.mirnadata.find({q_p:"C2C12 cell line"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("C2C12 cell line")

        fmir = dbs.mirnadata.find({q_p:"Quadriceps"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("Quadriceps")

        fmir = dbs.mirnadata.find({q_p:"Hind limb muscle"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("Hind limb muscle")

        fmir = dbs.mirnadata.find({q_p:"Soleus muscle"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("Soleus muscle")

        fmir = dbs.mirnadata.find({q_p:"Leg muscle tissue"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("Leg muscle tissue")

        fmir = dbs.mirnadata.find({q_p:"muscle"})
        for i in fmir:
            mir.append(i['name'])
            cor.append("muscle")

        return render(request,'query_result.html',{"mir":mir,"cor":cor,"corre":"yes","title":title})
    else:

        if q_r == "Tibialisanteriormuscle":
            q_r = "Tibialis anterior muscle"

        if q_r == "Vastuslateralismuscle":
            q_r = "Vastus lateralis muscle"

        if q_r == "Rectusfemoris":
            q_r = "Rectus femoris"

        if q_r == "Skeletalmuscle":
            q_r = "Skeletal muscle"

        if q_r == "Gastrocnemiusmuscle":
            q_r = "Gastrocnemius muscle"
        # source organism mice
        if q_r == "BALBcmice":
            q_r = "BALB/c mice"

        if q_r == "FVBmice":
            q_r = "FVB mice"

        if q_r == "CD1mice":
            q_r = "CD1 mice"

        if q_r == "AdultC57mice":
            q_r = "Adult C57 mice"

        if q_r == "C57BL6mice":
            q_r = "C57BL/6 mice"

            #rats
        if q_r == "SpragueDawleyrats":
            q_r = "Sprague Dawley rats"

        if q_r == "Wistarrats":
            q_r = "Wistar rats"

        if q_r == "C2C12cellline":
            q_r = "C2C12 cell line"

        if q_r == "HEK293T":
            q_r = "HEK293T cell line"

        if q_r == "Xuhaigoat":
            q_r = "Xuhai goat"

        if q_r == "Rhesusmonkey":
            q_r = "Rhesus monkey"

        if q_r == "129SvEv":
            q_r = "miR-206–/– mice in a 129SvEv-C57BL/6 mice"

        if q_r == "Quadriceps":
            q_r = "Quadriceps "


        if q_p == "doeh":
            fmir = dbs.mirnadata.find({ q_p: { "$regex":q_r } })
            duroexp=[]
            mir=[]
            title = "Duration of Experiment"

            if dbs.mirnadata.count_documents({ q_p: { "$regex":q_r } }) > 0:
                for i in fmir:
                    for k in i['doeh']:
                        if "hour" in k:
                            duroexp.append(k)
                            mir.append(i['name'])

            else:
                None

            return render(request,'query_result_doe.html',{"mir":mir,"cor":duroexp,"title":title})


        if q_p == "doey":
            fmir = dbs.mirnadata.find({ q_p: { "$regex":q_r } })
            duroexp=[]
            mir=[]
            title = "Duration of Experiment"

            if dbs.mirnadata.count_documents({ q_p: { "$regex":q_r } }) > 0:
                for i in fmir:
                    for k in i['doey']:
                        if "Year" in k:
                            duroexp.append(k)
                            mir.append(i['name'])
            else:
                None

            return render(request,'query_result_doe.html',{"mir":mir,"cor":duroexp,"title":title})


        if q_p == "doew":
            fmir = dbs.mirnadata.find({ q_p: { "$regex":q_r } })
            duroexp=[]
            mir=[]
            title = "Duration of Experiment"
            if dbs.mirnadata.count_documents({ q_p: { "$regex":q_r } }) > 0:
                for i in fmir:
                    for k in i['doew']:
                        if "week" in k:
                            duroexp.append(k)
                            mir.append(i['name'])

            else:
                None

            return render(request,'query_result_doe.html',{"mir":mir,"cor":duroexp,"title":title})

        if q_p == "doed":
            fmir = dbs.mirnadata.find({ q_p: { "$regex":q_r } })
            duroexp=[]
            mir=[]
            title = "Duration of Experiment"
            if dbs.mirnadata.count_documents({ q_p: { "$regex":q_r } }) > 0:
                for i in fmir:
                    for k in i['doed']:
                        if "days" in k:
                            duroexp.append(k)
                            mir.append(i['name'])

            else:
                None

            return render(request,'query_result_doe.html',{"mir":mir,"cor":duroexp,"title":title})

        elif q_r == 'Humans':
            for p in range(2):
                if p == 0:
                    q_r='Humans'
                    fmir = dbs.mirnadata.find({q_p:q_r})

                    if dbs.mirnadata.count_documents({q_p:q_r}) > 0:
                        for i in fmir:
                            mir.append(i['name'])
                    else:
                        None

                        # mir.append(i['name'])
                if p == 1:
                    q_r='C2C12 cell lines, Adult C57 mouse, Human model'
                    fmir = dbs.mirnadata.find({q_p:q_r})

                    if dbs.mirnadata.count_documents({q_p:q_r}) > 0:
                        for i in fmir:
                            mir.append(i['name'])
                    else:
                        None
                        # mir.append(i['name'])

            q_r='Humans'
            mir = set(mir)
            return render(request,'query_result.html',{"mir":mir,"cor":q_r,"title":title})

        else:
            fmir = dbs.mirnadata.find({q_p:q_r})
            if dbs.mirnadata.count_documents({q_p:q_r}) > 0:
                for i in fmir:
                    mir.append(i['name'])
            else:
                None

                # mir.append(i['name'])

            return render(request,'query_result.html',{"mir":mir,"cor":q_r,"title":title})


def resulttf(request):
    if request.method == "POST":
        item = request.POST.getlist('tf')
        mir=[]
        ge=[]
        for k in item:
            fmir = dbs.ntmirnacollection.find({"tf":k})
            mir=[]
            if dbs.ntmirnacollection.count_documents({"tf":k}) > 0:
                for i in fmir:
                    mir.append(i['name'])
                    ge.append(k)
            else:
                None

        return render(request,'query_result_tf.html',{"mir":mir,"cor":ge,"title":"TF"})

def resultge(request):
    if request.method == "POST":
        item = request.POST.getlist('gene')
        mir=[]
        ge=[]
        for k in item:
            try:
                fmir = dbs.ntmirnacollection.find({"gene":k})
                if dbs.ntmirnacollection.count_documents({"gene":k}) > 0:
                    for i in fmir:
                        mir.append(i['name'])
                        ge.append(k)
                else:
                    fmir = dbs.ntmirnacollection.find({"tf":k})
                    if dbs.ntmirnacollection.count_documents({"tf":k}) > 0:
                        for j in fmir:
                            mir.append(j['name'])
                            ge.append(k)
                    else:
                        None
            except:
                None

        return render(request,'query_result_ge.html',{"mir":mir,"cor":ge,"title":"Gene"})

def resultdrug(request):
    if request.method == "POST":
        item = request.POST.get('drug')
        fmir = dbs.mirpharmadata.find({"drug":item})
        mir=[]
        if dbs.mirpharmadata.count_documents({"drug":item}) > 0:
            for i in fmir:
                mir.append(i['name'])
        else:
            None

        return render(request,'query_result.html',{"mir":mir,"cor":item})

def resultdibi(request):

    fmir = dbs.mirnadata.find({"dibi":'Yes'})
    mir=[]
    if dbs.mirnadata.count_documents({"dibi":'Yes'}) > 0:
        for i in fmir:
            mir.append(i['name'])
    return render(request,'query_result.html',{"mir":mir,"cor":'Yes',"title":"Bio Marker"})

def resultontogoid(request):
    if request.method == "POST":
        item = request.POST.get('goid')
        title = "GO ID"
        fmir = dbs.mirnaonto.find({"goid":item})
        mir=[]
        if dbs.mirnaonto.count_documents({"goid":item}) > 0:
            for i in fmir:
                mir.append(i['name'])
        else:
            None

        return render(request,'query_result.html',{"mir":mir,"cor":item,"title":title})

def resultontoterm(request):
    if request.method == "POST":
        item = request.POST.get('term')
        title = "Term"
        fmir = dbs.mirnaonto.find({"term":item})
        mir=[]
        if dbs.mirnaonto.count_documents({"term":item}) > 0:
            for i in fmir:
                mir.append(i['name'])
        else:
            None

        return render(request,'query_result.html',{"mir":mir,"cor":item,"title":title})

def resultpathwayid(request):
    if request.method == "POST":
        item = request.POST.get('goid')
        title = "KGID"
        fmir = dbs.mirnapath.find({"kgid":item})
        mir=[]
        if dbs.mirnapath.count_documents({"kgid":item}) > 0:
            for i in fmir:
                mir.append(i['name'])
        else:
            None
        return render(request,'query_result.html',{"mir":mir,"cor":item,"title":title})

def resultpathwayterm(request):
    if request.method == "POST":
        item = request.POST.get('term')
        title = "Term"
        fmir = dbs.mirnapath.find({"term":item})
        mir=[]
        if dbs.mirnapath.count_documents({"term":item}) > 0:
            for i in fmir:
                mir.append(i['name'])
        else:
            None
        return render(request,'query_result.html',{"mir":mir,"cor":item,"title":title})

def search(request):

    fcol = dbs.mirnadata.find()

    name = []
    for i in fcol:
        name.append(i['name'])

    return render(request,'search.html',{"name":name})

def searchge(request):

    fcol = dbs.ntmirnacollection.find()

    name = []

    for i in fcol:
        try:
            for t in i['gene']:
                name.append(t)
        except:
            None
        try:
            for t in i['tf']:
                name.append(t)
        except:
            None

    name = list(set(name))

    return render(request,'searchge.html',{"name":name})

def searchtf(request):

    fcol = dbs.ntmirnacollection.find()

    name = []
    for i in fcol:
        try:
            for t in i['tf']:
                name.append(t)
        except:
            None

    name = list(set(name))

    return render(request,'searchtf.html',{"name":name})

def searchdrug(request):

    fcol = dbs.mirpharmadata.find()
    name = []
    for i in fcol:
        try:
            for t in i['drug']:
                name.append(t)
        except:
            None

    name = list(set(name))

    return render(request,'searchdrug.html',{"name":name})


def searchontogoid(request):

    fcol = dbs.mirnaonto.find()
    name = []
    for i in fcol:
        try:
            for t in i['goid']:
                name.append(t)
        except:
            None
    name = list(set(name))
    return render(request,'searchontogoid.html',{"name":name})

def searchontoterm(request):

    fcol = dbs.mirnaonto.find()

    name = []

    for i in fcol:
        try:
            for t in i['term']:
                name.append(t)
        except:
            None
    name = list(set(name))
    return render(request,'searchontoterm.html',{"name":name})


def searchpathwayid(request):

    fcol = dbs.mirnapath.find()
    name = []
    for i in fcol:
        try:
            for t in i['kgid']:
                name.append(t)
        except:
            None
    name = list(set(name))
    return render(request,'searchpathwayid.html',{"name":name})

def searchpathwayterm(request):

    fcol = dbs.mirnapath.find()
    name = []
    for i in fcol:
        try:
            for t in i['term']:
                name.append(t)
        except:
            None
    name = list(set(name))
    name.sort()
    return render(request,'searchpathwayterm.html',{"name":name})

def sslinfo(request):

    if request.method == 'POST':
        item = request.POST.get('mir')
        try:
            fmir2 = dbs.mircollection.find({"name":"tri"+item})
            if dbs.mircollection.count_documents({"name":"tri"+item})>0:
                for hu in fmir2:
                    outmirna = hu['mirna']
                    outgene = hu['gene']
                    outtf = hu['tf']
            else:
                outmirna=[0]
                outgene=[0]
                outtf=[0]

        except:
            outmirna=[0]
            outgene=[0]
            outtf=[0]


        try:
            fmir2 = dbs.tyimircollection.find({"name":"ftri"+item})
            trimirna=[]
            trigene=[]
            tritf=[]
            if dbs.tyimircollection.count_documents({"name":"ftri"+item})>0:

                for hu in fmir2:
                    outmirna2 = hu['mirna']
                    outgene2 = hu['gene']
                    outtf2 = hu['tf']
            else:
                outmirna2=[0]
                outgene2=[0]
                outtf2=[0]

        except:
            outmirna2=[0]
            outgene2=[0]
            outtf2=[0]

        if (outmirna[0] == 0) and (outmirna2[0] == 0):
            noshow = 1
        else:
            noshow = None

        context={

                "trimir":outmirna,
                "trigene":outgene,
                "tritf":outtf,
                "noshow":noshow,
                "trimirtr":outmirna2,
                "trigenetr":outgene2,
                "tritftr":outtf2,
        }

        return render(request,'sslinfo.html',context)


def detail(request):
    if request.method == 'POST':
        item = request.POST.get('mir')
        fmir = dbs.mirnadata.find({"name":item})
        dibi = []
        doe = []
        expcon = []
        mam = []
        ref = []
        soe = []
        toe = []
        tom = []
        uds = []
        fc=[]
        for i in fmir:
            dibi = i['dibi']
            doe = np.core.defchararray.add(i['doeh'],i['doed'])
            doe = np.core.defchararray.add(doe,i['doew'])
            doe = [s.replace('na', '') for s in doe]
            for u,v in enumerate(doe):
                if not v:
                    doe[u] = 'na'

            expcon = i['expcon']
            fc = i['fc']
            mam = i['mam']
            ref = i['ref']
            soe = i['soe']
            toe = i['toe']
            tom = i['tom']
            uds = i['uds']

        for i,j in enumerate(dibi):
            if dibi[i] == 'na':
                dibi[i] = 'No'

        try:
            if 'mmu-miR' in item:
                nitem = item.replace('mmu-miR','mmu-mir')
                fmir = dbs.mirnainfo.find({"name":nitem})
                fcount = dbs.mirnainfo.count_documents({"name":nitem})
            else:
                fmir = dbs.mirnainfo.find({"name":item})
                fcount = dbs.mirnainfo.count_documents({"name":item})

            if fcount > 0:
                for i in fmir:
                    miracc = i['miracc'][0]
                    tpri = i['3pri'][0]
                    fpri = i['5pri'][0]
                    chrom = i['chro'][0]
                    fam = i['family'][0]
                    img = i['image'][0]
                    mature = i['mature'][0]
                    prec = i['prec'][0]
                    rnid = i['rnaid'][0]
                    slid = i['slid'][0]
            else:
                miracc = ["na"]
                tpri = ["na"]
                fpri = ["na"]
                chrom = ["na"]
                fam = ["na"]
                img = ["na"]
                mature = ["na"]
                prec = ["na"]
                rnid = ["na"]
                slid = ["na"]

        except:
            info = False


        try:
            fmir = dbs.mirpharmadata.find({"name":item})
            if dbs.mirpharmadata.count_documents({"name":item}) > 0:
                for i in fmir:
                    drug = i['drug']
                    ge = i['gene']
                    pid = i['pid']
            else:
                drug = ["na"]
                ge = ["na"]
                pid = ["na"]

        except:
            pharma = False

        try:
            fmir = dbs.mirdisdata.find({"name":item})
            if dbs.mirdisdata.count_documents({"name":item})>0:
                for i in fmir:
                    disease = i['disease']
                    refid = i['refid']
            else:
                disease = ["na"]
                refid = ["na"]
        except:
            disdata = False

        try:

            fmir = dbs.mirnaonto.find({"name":item})
            if dbs.mirnaonto.count_documents({"name":item})>0:
                for i in fmir:
                    category = i['category']
                    ocount = i['count']
                    geon = i['ge']
                    goid = i['goid']
                    peronto = i['per']
                    pval = i['pval']
                    term = i['term']
            else:
                category = ['na']
                ocount = ['na']
                geon = ['na']
                goid = ['na']
                peronto = ['na']
                pval = ['na']
                term = ['na']
        except:
            onto = False

        try:

            fmir = dbs.mirnapath.find({"name":item})
            if dbs.mirnapath.count_documents({"name":item})>0:
                for i in fmir:

                    pcount = i['count']
                    pgeon = i['ge']
                    kgid = i['kgid']
                    ppval = i['pval']
                    pterm = i['term']
            else:
                pcount = ['na']
                pgeon = ['na']
                kgid = ['na']
                ppval = ['na']
                pterm = ['na']
        except:
            onto = False

        try:
            keys=[]
            fin = []
            href=[]
            fmir = dbs.mirnatissuedata.find_one()
            for key in fmir:
                keys.append(key)
            keys.remove('_id')
            keys.remove('name')

            fmir2 = dbs.mirnatissuedata.find({"name":item})
            count=0
            fcount=[]
            if dbs.mirnatissuedata.count_documents({"name":item})>0:
                for i in fmir2:
                    for j in keys:
                        fin.append(i[j])
                for k in range(len(fin)):
                    fin[k].insert(0,keys[k])
                count = len(fin[0]) - 1
                for l in range(0,int(count)):
                    fcount.append(l)
                href=[i[0] for i in fin]
            else:
                fin = [['na']]

        except:
            distisdata = False

        # print(fin)
        edges=[]
        nodes = []
        dwdata = []
        nodes.append({'id':item,'label':item,"color":'red'})

        try:

            fmir2 = dbs.ntmirnacollection.find({"name":item})

            if dbs.ntmirnacollection.count_documents({"name":item})>0:
                for hu in fmir2:
                    try:
                        outgene3 = hu['gene']
                        couny = 1
                    except:
                        couny = 0
                    outmirna3 = hu['name']
                    outtf3 = hu['tf']

                if couny == 1:

                    for k in range(len(outtf3)):
                        nodes.append({'id':outtf3[k],'label':outtf3[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
                        nodes.append({'id':outgene3[k],'label':outgene3[k],"color":'#FFFF00',"fixed":"true","shape": 'box'})
                        edges.append({"from":item,"to":outtf3[k],"color":'lightgreen',"length":"800","arrows":'to'})
                        edges.append({"from":item,"to":outgene3[k],"color":'#FFFF00',"length":"600","arrows":'to'})

                        dwdata.append({"from":item,"to":outtf3[k]})
                        dwdata.append({"from":item,"to":outgene3[k]})
                else:
                        for k in range(len(outtf3)):
                            nodes.append({'id':outtf3[k],'label':outtf3[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
                            edges.append({"from":item,"to":outtf3[k],"color":'lightgreen',"length":"800","arrows":'to'})
                            dwdata.append({"from":item,"to":outtf3[k]})

        except:
            None

        try:

            fmir2 = dbs.mttrimirnacollection.find({"name":item})

            if dbs.mttrimirnacollection.count_documents({"name":item})>0:

                for hu in fmir2:
                    outmirna = hu['mirna']
                    outgene = hu['gene']
                    outtf = hu['tf']

                for k in range(len(outtf)):
                    nodes.append({'id':outtf[k],'label':outtf[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
                    nodes.append({'id':outgene[k],'label':outgene[k],"color":'#FFFF00',"fixed":"true","shape": 'box'})
                    edges.append({"from":outtf[k],"to":item,"color":'lightgreen',"length":"800","arrows":'to'})
                    edges.append({"from":item,"to":outgene[k],"color":'#FFFF00',"length":"600","arrows":'to'})
                    edges.append({"from":outtf[k],"to":outgene[k],"color":'#FFFF00',"length":"300","arrows":'to'})

                    dwdata.append({"from":outtf[k],"to":item})
                    dwdata.append({"from":item,"to":outgene[k]})
                    dwdata.append({"from":outtf[k],"to":outgene[k]})

        except:
            None

        try:
            fmir2 = dbs.ttrimirnacollection.find({"name":item})
            trimirna=[]
            trigene=[]
            tritf=[]

            if dbs.ttrimirnacollection.count_documents({"name":item})>0:

                for hu in fmir2:
                    outmirna2 = hu['mirna']
                    outgene2 = hu['gene']
                    outtf2 = hu['tf']

                for k in range(len(outtf2)):

                    nodes.append({'id':outtf2[k],'label':outtf2[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
                    nodes.append({'id':outgene2[k],'label':outgene2[k],"color":'#FFFF00',"fixed":"true","shape": 'box'})
                    edges.append({"from":item,"to":outgene2[k],"color":'lightgreen',"length":"600","arrows":'to'})
                    edges.append({"from":item,"to":outtf2[k],"color":'#FFFF00',"length":"800","arrows":'to'})
                    edges.append({"from":outtf2[k],"to":outgene2[k],"color":'#FFFF00',"length":"300","arrows":'to'})

                    dwdata.append({"from":item,"to":outgene2[k]})
                    dwdata.append({"from":item,"to":outtf2[k]})
                    dwdata.append({"from":outtf2[k],"to":outgene2[k]})

        except:
            None

        n_seen = set()
        new_nodes = []
        for d in nodes:
            if type(d['id']) == str:
                t = tuple(d['id'])
                if t not in n_seen:
                    n_seen.add(t)
                    new_nodes.append(d)
            else:
                None

        e_seen = set()
        new_edges = []
        for f in edges:
            u = tuple(f.items())
            if u not in e_seen:
                e_seen.add(u)
                new_edges.append(f)

        ndw_seen = set()
        ndw_data = []
        for d in dwdata:
            t = tuple(d.items())
            if t not in ndw_seen:
                ndw_seen.add(t)
                ndw_data.append(d)


        context={
            "dibi":dibi,
            "doe" :doe,
            "expcon":expcon,
            "fc":fc,
            "mam" :mam,
            "ref" :ref,
            "soe" :soe,
            "toe" :toe,
            "tom" :tom,
            "uds":uds,


            "miracc" :miracc,
            "tpri":tpri,
            "fpri":fpri,
            "chrom":chrom,
            "fam":fam,
            "img":img,
            "mature":mature,
            "prec":prec,
            "rnid":rnid,
            "slid":slid,
            "mirna":item,

            "drug":drug,
            "ge":ge,
            "pid":pid,


            "disease":disease,
            "refid":refid,

            "fink":fin,
            "count":fcount,

            "edges":new_edges,
            "nodes":new_nodes,

            "dwdata":dwdata,

            "category":category,
            "ocount":ocount,
            "geon":geon,
            "goid":goid,
            "peronto":peronto,
            "pval":pval,
            "term":term,

            "pcount":pcount,
            "kgid":kgid,
            "pgeon":pgeon,
            "ppval":ppval,
            "pterm":pterm,

        }

        return render(request,'details.html',context)


def mirdetail(request,pk):

    item = pk
    fmir = dbs.mirnadata.find({"name":item})
    dibi = []
    doe = []
    expcon = []
    mam = []
    ref = []
    soe = []
    toe = []
    tom = []
    uds = []
    fc=[]
    for i in fmir:
        dibi = i['dibi']
        doe = np.core.defchararray.add(i['doeh'],i['doed'])
        doe = np.core.defchararray.add(doe,i['doew'])
        doe = [s.replace('na', '') for s in doe]
        for u,v in enumerate(doe):
            if not v:
                doe[u] = 'na'

        expcon = i['expcon']
        fc = i['fc']
        mam = i['mam']
        ref = i['ref']
        soe = i['soe']
        toe = i['toe']
        tom = i['tom']
        uds = i['uds']

    for i,j in enumerate(dibi):
        if dibi[i] == 'na':
            dibi[i] = 'No'

    try:
        if 'mmu-miR' in item:
            nitem = item.replace('mmu-miR','mmu-mir')
            fmir = dbs.mirnainfo.find({"name":nitem})
            fcount = dbs.mirnainfo.count_documents({"name":nitem})
        else:
            fmir = dbs.mirnainfo.find({"name":item})
            fcount = dbs.mirnainfo.count_documents({"name":item})
        if fcount > 0:
            for i in fmir:
                miracc = i['miracc'][0]
                tpri = i['3pri'][0]
                fpri = i['5pri'][0]
                chrom = i['chro'][0]
                fam = i['family'][0]
                img = i['image'][0]
                mature = i['mature'][0]
                prec = i['prec'][0]
                rnid = i['rnaid'][0]
                slid = i['slid'][0]
        else:
            miracc = ["na"]
            tpri = ["na"]
            fpri = ["na"]
            chrom = ["na"]
            fam = ["na"]
            img = ["na"]
            mature = ["na"]
            prec = ["na"]
            rnid = ["na"]
            slid = ["na"]

    except:
        info = False


    try:
        fmir = dbs.mirpharmadata.find({"name":item})
        if dbs.mirpharmadata.count_documents({"name":item}) > 0:
            for i in fmir:
                drug = i['drug']
                ge = i['gene']
                pid = i['pid']
        else:
            drug = ["na"]
            ge = ["na"]
            pid = ["na"]

    except:
        pharma = False

    try:
        fmir = dbs.mirdisdata.find({"name":item})
        if fdbs.mirdisdata.count_documents({"name":item})>0:
            for i in fmir:
                disease = i['disease']
                refid = i['refid']
        else:
            disease = ["na"]
            refid = ["na"]
    except:
        disdata = False

    try:

        fmir = dbs.mirnaonto.find({"name":item})
        if dbs.mirnaonto.count_documents({"name":item})>0:
            for i in fmir:
                category = i['category']
                ocount = i['count']
                geon = i['ge']
                goid = i['goid']
                peronto = i['per']
                pval = i['pval']
                term = i['term']
        else:
            category = ['na']
            ocount = ['na']
            geon = ['na']
            goid = ['na']
            peronto = ['na']
            pval = ['na']
            term = ['na']
    except:
        onto = False

    try:

        fmir = dbs.mirnapath.find({"name":item})
        if dbs.mirnapath.count_documents({"name":item})>0:
            for i in fmir:

                pcount = i['count']
                pgeon = i['ge']
                kgid = i['kgid']
                ppval = i['pval']
                pterm = i['term']
        else:
            pcount = ['na']
            pgeon = ['na']
            kgid = ['na']
            ppval = ['na']
            pterm = ['na']
    except:
        onto = False

    try:
        keys=[]
        fin = []
        fmir = dbs.mirnatissuedata.find_one()
        for key in fmir:
            keys.append(key)
        keys.remove('_id')
        keys.remove('name')

        fmir2 = dbs.mirnatissuedata.find({"name":item})
        count=0
        fcount=[]
        if dbs.mirnatissuedata.count_documents({"name":item})>0:
            for i in fmir2:
                for j in keys:
                    fin.append(i[j])
            for k in range(len(fin)):
                fin[k].insert(0,keys[k])
            count = len(fin[0]) - 1
            for l in range(0,int(count)):
                fcount.append(l)
        else:
            fin = [['na']]

    except:
        distisdata = False

    edges=[]
    nodes = []
    dwdata = []
    nodes.append({'id':item,'label':item,"color":'red'})

    try:
        fcol = dbs.mircollection.find({"name":"tri"+item})

        for hu in fcol:
            outmirna = hu['mirna']
            outgene = hu['gene']
            outtf = hu['tf']
        # print(outgene)
        try:
            for ik in range(len(outgene)):
                # print(ik)
                edges.append({"from":outtf[ik],"to":outgene[ik],"color":'#FFFF00',"length":"600","arrows":'to'})
                echoo.append({"from":outtf[ik],"to":outgene[ik]})
        except:
            None

        count=len(outmirna)

    except:
        fcol=0
        count=0
        outmirna=0
        outgene=0
        outtf=0

    try:

        fcol = dbs.tyimircollection.find({"name":"ftri"+item})

        if dbs.tyimircollection.count_documents({"name":"ftri"+item})>0:

            for hu in fcol:

                outmirna2 = hu['mirna']
                outgene2 = hu['gene']
                outtf2 = hu['tf']

            try:
                for ik in range(len(outtf2)):
                    # print(ik)
                    edges.append({"from":outtf2[ik],"to":outgene2[ik],"color":'#FFFF00',"length":"600","arrows":'to'})
                    echoo.append({"from":outtf2[ik],"to":outgene2[ik]})
                    edges.append({"from":outtf2[ik],"to":outmirna2[ik],"color":'#FFFF00',"length":"600","arrows":'to'})
                    echoo.append({"from":outtf2[ik],"to":outmirna2[ik]})

                for itf in set(outtf2):
                    nodes.append({'id':itf,'label':itf,"color":'lightgreen',"fixed":"true","shape": 'box'})

                for itg in set(outgene2):
                    nodes.append({'id':itg,'label':itg,"color":'#FFFF00',"fixed":"true","shape": 'box'})

            except:
                outmirna2=0
                outgene2=0
                outtf2=0
        else:
            outmirna2=0
            outgene2=0
            outtf2=0

    except:
        outmirna2=0
        outgene2=0
        outtf2=0
        # try:
        #     if (outmirna != 0) & (outmirna2 != 0):
        #         outmirna = outmirna + outmirna2
        #         outgene = outgene + outgene2
        #         outtf = outtf + outtf2
        #
        #         afg=[]
        #         for ri in range(len(outmirna)):
        #             afg.append({"mir":outmirna[ri],"gene":outgene[ri],"tf":outtf[ri]})
        #
        #         e_seen = set()
        #         new_afg = []
        #         for f in afg:
        #             u = tuple(f.items())
        #             if u not in e_seen:
        #                 e_seen.add(u)
        #                 new_afg.append(f)
        #         outmirna=[]
        #         outtf=[]
        #         outgene=[]
        #         for rt in range(len(new_afg)):
        #             outmirna.append(new_afg[rt]['mir'])
        #             outtf.append(new_afg[rt]['tf'])
        #             outgene.append(new_afg[rt]['gene'])
        # except:
        #     None

    e_seen = set()
    new_nodes = []
    for o in nodes:
        u = tuple(o.items())
        if u not in e_seen:
            e_seen.add(u)
            new_nodes.append(o)

    e_seen = set()
    new_edges = []
    for f in edges:
        u = tuple(f.items())
        if u not in e_seen:
            e_seen.add(u)
            new_edges.append(f)

    ndw_seen = set()
    ndw_data = []
    for d in echoo:
        t = tuple(d.items())
        if t not in ndw_seen:
            ndw_seen.add(t)
            ndw_data.append(d)
    #
    # try:
    #
    #     fmir2 = dbs.ntmirnacollection.find({"name":item})
    #
    #     if fmir2.count()>0:
    #
    #         for hu in fmir2:
    #             outmirna = hu['name']
    #             outgene = hu['gene']
    #             outtf = hu['tf']
    #
    #         for k in range(len(outtf)):
    #             nodes.append({'id':outtf[k],'label':outtf[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
    #             nodes.append({'id':outgene[k],'label':outgene[k],"color":'#FFFF00',"fixed":"true","shape": 'box'})
    #             edges.append({"from":item,"to":outtf[k],"color":'lightgreen',"length":"800","arrows":'to'})
    #             edges.append({"from":item,"to":outgene[k],"color":'#FFFF00',"length":"600","arrows":'to'})
    #
    #             dwdata.append({"from":item,"to":outtf[k]})
    #             dwdata.append({"from":item,"to":outgene[k]})
    #
    # except:
    #     None
    #
    # try:
    #
    #     fmir2 = dbs.mttrimirnacollection.find({"name":item})
    #
    #     if fmir2.count()>0:
    #
    #         for hu in fmir2:
    #             outmirna = hu['mirna']
    #             outgene = hu['gene']
    #             outtf = hu['tf']
    #
    #         for k in range(len(outtf)):
    #             nodes.append({'id':outtf[k],'label':outtf[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
    #             nodes.append({'id':outgene[k],'label':outgene[k],"color":'#FFFF00',"fixed":"true","shape": 'box'})
    #             edges.append({"from":outtf[k],"to":item,"color":'lightgreen',"length":"800","arrows":'to'})
    #             edges.append({"from":item,"to":outgene[k],"color":'#FFFF00',"length":"600","arrows":'to'})
    #             edges.append({"from":outtf[k],"to":outgene[k],"color":'#FFFF00',"length":"300","arrows":'to'})
    #
    #             dwdata.append({"from":outtf[k],"to":item})
    #             dwdata.append({"from":item,"to":outgene[k]})
    #             dwdata.append({"from":outtf[k],"to":outgene[k]})
    #
    # except:
    #     None
    #
    # try:
    #     fmir2 = dbs.ttrimirnacollection.find({"name":item})
    #     trimirna=[]
    #     trigene=[]
    #     tritf=[]
    #
    #     if fmir2.count()>0:
    #
    #         for hu in fmir2:
    #             outmirna2 = hu['mirna']
    #             outgene2 = hu['gene']
    #             outtf2 = hu['tf']
    #
    #         for k in range(len(outtf2)):
    #
    #             nodes.append({'id':outtf2[k],'label':outtf2[k],"color":'lightgreen',"fixed":"true","shape": 'box'})
    #             nodes.append({'id':outgene2[k],'label':outgene2[k],"color":'#FFFF00',"fixed":"true","shape": 'box'})
    #             edges.append({"from":item,"to":outgene2[k],"color":'lightgreen',"length":"600","arrows":'to'})
    #             edges.append({"from":item,"to":outtf2[k],"color":'#FFFF00',"length":"800","arrows":'to'})
    #             edges.append({"from":outtf2[k],"to":outgene2[k],"color":'#FFFF00',"length":"300","arrows":'to'})
    #
    #             dwdata.append({"from":item,"to":outgene2[k]})
    #             dwdata.append({"from":item,"to":outtf2[k]})
    #             dwdata.append({"from":outtf2[k],"to":outgene2[k]})
    #
    #
    # except:
    #     None
    #
    # n_seen = set()
    # new_nodes = []
    # for d in nodes:
    #     t = tuple(d.items())
    #     if t not in n_seen:
    #         n_seen.add(t)
    #         new_nodes.append(d)
    #
    #
    # e_seen = set()
    # new_edges = []
    # for f in edges:
    #     u = tuple(f.items())
    #     if u not in e_seen:
    #         e_seen.add(u)
    #         new_edges.append(f)
    #
    # ndw_seen = set()
    # ndw_data = []
    # for d in dwdata:
    #     t = tuple(d.items())
    #     if t not in ndw_seen:
    #         ndw_seen.add(t)
    #         ndw_data.append(d)

    context={
        "dibi":dibi,
        "doe" :doe,
        "expcon":expcon,
        "fc":fc,
        "mam" :mam,
        "ref" :ref,
        "soe" :soe,
        "toe" :toe,
        "tom" :tom,
        "uds":uds,


        "miracc" :miracc,
        "tpri":tpri,
        "fpri":fpri,
        "chrom":chrom,
        "fam":fam,
        "img":img,
        "mature":mature,
        "prec":prec,
        "rnid":rnid,
        "slid":slid,
        "mirna":item,

        "drug":drug,
        "ge":ge,
        "pid":pid,


        "disease":disease,
        "refid":refid,

        "fink":fin,
        "count":fcount,

        "edges":new_edges,
        "nodes":new_nodes,

        "dwdata":ndw_data,

        "category":category,
        "ocount":ocount,
        "geon":geon,
        "goid":goid,
        "peronto":peronto,
        "pval":pval,
        "term":term,

        "pcount":pcount,
        "kgid":kgid,
        "pgeon":pgeon,
        "ppval":ppval,
        "pterm":pterm,

    }

    return render(request,'details.html',context)
