from django.shortcuts import render,HttpResponse
from datetime import datetime
from myapp.models import Contact
import math
from scipy.stats import norm
# Create your views here.
def index(request):
    context={
        "variable":"this is sent",
    }
    return render(request,"index.html",context)
    # return HttpResponse("this is home page of myapp")

def about(request):
    return render(request,"about.html")
def services(request):
    return render(request,"services.html")
def two_step(request):
    ob={}
    if request.method=="POST":
        strike=request.POST.get("strike")
        current=request.POST.get("current")
        type=request.POST.get("type")
        rate=request.POST.get("rate")
        upfactor=request.POST.get("upfactor")
        downfactor=request.POST.get("downfactor")
        timeperiod=request.POST.get("timeperiod")
        ob.update({"type":type})
        ob.update({"rate":rate})
        ob.update({"upfactor":upfactor})
        ob.update({"downfactor":downfactor})
        ob.update({"timeperiod":timeperiod})
        ob.update({"strike":strike})
        ob.update({"current":current})
        p=math.exp((int(timeperiod)/1200)*float(rate))
        p=p-float(downfactor)
        p=p/(float(upfactor)-float(downfactor))
        if(p<1):
            value=math.exp(-1*(int(timeperiod)/1200)*float(rate))
            if(type=="call"):
                value=value*p*(float(upfactor)*float(current)-float(strike))
                ob.update({"optionPrice":value})
            else:
                value=value*(1-p)*(float(strike)-float(downfactor)*float(current))
                ob.update({"optionPrice":value})
    return render(request,"two_step.html",ob)
def n_step(request):
    ob={}
    if request.method=="POST":
        strike=request.POST.get("strike")
        current=request.POST.get("current")
        type=request.POST.get("type")
        rate=request.POST.get("rate")
        timeperiod=request.POST.get("timeperiod")
        binomial=request.POST.get("binomial")
        upfactor=request.POST.get("upfactor")
        downfactor=request.POST.get("downfactor")
        pu=((math.exp(float(rate)*float(timeperiod)))-float(downfactor))/(float(upfactor)-float(downfactor))
        pd=1-pu
        disc=math.exp(-float(rate)*float(timeperiod)/int(binomial))

        St = [0] * (int(binomial)+1)
        C = [0] * (int(binomial)+1)
    
        St[0]=float(current)*float(downfactor)**int(binomial)
    
        for j in range(1, int(binomial)+1): 
            St[j] = St[j-1] * float(upfactor)/float(downfactor)
    
        for j in range(1, int(binomial)+1):
            if type == 'put':
                C[j] = max(float(strike)-St[j],0)
            elif type == 'call':
                C[j] = max(St[j]-float(strike),0)
    
        for i in range(int(binomial), 0, -1):
            for j in range(0, i):
                C[j] = disc*(pu*C[j+1]+pd*C[j])
            
        ob.update({"type":type})
        ob.update({"rate":rate})
        ob.update({"upfactor":upfactor})
        ob.update({"downfactor":downfactor})
        ob.update({"timeperiod":timeperiod})
        ob.update({"binomial":binomial})
        ob.update({"strike":strike})
        ob.update({"current":current})
        ob.update({"optionPrice":C[0]})
    return render(request,"n_step.html",ob)
def black_scholes(request):
    
    ob={}
    if request.method=="POST":
        strike=request.POST.get("strike")
        current=request.POST.get("current")
        type=request.POST.get("type")
        rate=request.POST.get("rate")
        timeperiod=request.POST.get("timeperiod")
        sigma=request.POST.get("sigma")
        d1=(math.log(float(current)/float(strike))+(float(rate)+float(sigma)*float(sigma))*float(timeperiod))/float(sigma)*math.sqrt(float(timeperiod))
        d2=d1-float(sigma)*math.sqrt(float(timeperiod))
        price=0
        if(type=="call"):
            price=norm.cdf(float(d1), 0, float(sigma)*float(sigma))*float(current)-norm.cdf(d2, 0, float(sigma)*float(sigma))*float(strike)*math.exp(-float(rate)*float(timeperiod))
        else:
            price=float(current)*math.exp(-float(rate)*float(timeperiod))*norm.cdf(-d2,0,float(sigma)*float(sigma))-float(current)*norm.cdf(-d1,0,float(sigma)*float(sigma))
        ob.update({"type":type})
        ob.update({"rate":rate})
        ob.update({"timeperiod":timeperiod})
        ob.update({"strike":strike})
        ob.update({"current":current})
        ob.update({"volatility":sigma})
        ob.update({"optionPrice":price})
    return render(request,"black_scholes.html",ob)
def contact(request):
    ob={}
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneNumber=request.POST.get("phoneNumber")
        contact=Contact(name=name,email=email,phoneNumber=phoneNumber,date=datetime.today())
        contact.save()
        ob.update({"personname":name})
    return render(request,"contact.html",ob)