from se.net.models import *
from django.shortcuts import render_to_response  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db.models import Sum, Count



@login_required
def index(request):
	#getting user name from session
	uname = request.user.username
  	return render_to_response('index.html', {'uname': uname})

@login_required
def taskslist(request):
	#getting user name from session
	uname = request.user.username
	#queries the database for the to-do entries of the logged in user
	items = Task.objects.filter(employee__user__username=uname) 
        #Responds with passing the object items (contains info from the DB) to the template index.html  
  	return render_to_response('taskslist.html', {'items': items}) 

@login_required
def reportgen(request):
  	return render_to_response('reportgen.html') 

def taskcompleted(request):
	errors=[]
	#getting user name from session
	uname = request.user.username

	if request.method == 'POST':
		if not request.POST.get('id', ''):
			errors.append('Enter valid id.')
	if not errors:
		#deleting requested item from tasks list
		Task.objects.filter(id=request.POST.get('id')).delete();
		#saving item to Sold
		gt = Stock.objects.get(type__name=request.POST.get('what'))
		shopkind = Shop.objects.get(name=request.POST.get('shop'), nip=request.POST.get('nip'))
		emp = Employee.objects.get(user__username=uname)
		newsold = Sold(employee=emp, what=gt, shop=shopkind, date=request.POST.get('subdate'), amount=request.POST.get('amount'), price=request.POST.get('price') )
		newsold.save();
		#displaying remaining tasks
		items = Task.objects.filter(employee__user__username=uname)
		return render_to_response('taskslist.html', {'items': items}) 


@login_required
def resp(request):
	uname=request.GET.get('user')
	shops=Sold.objects.filter(employee__user__username=uname)
	people=Employee.objects.filter(supervisor__user__username=uname)
  	return render_to_response('resp.html', {'shops': shops, 'people': people})

@login_required
def reportgen(request): 
	uname=request.GET.get('user')
	#this is temporary, further there will also be user kind (manager/agent)
	if uname == "se":
  		return render_to_response('reportmanager.html', {'user':uname})
	else:
		return render_to_response('reportagent.html', {'user':uname})

@login_required
def repgenmanager(request): 
	uname=request.GET.get('user') 
	kinds=request.GET.get('kinds') 
	amnt = request.GET.get('amount')
	price=request.GET.get('price')
	warehouse=request.GET.get('warehouse')
	datetime=request.GET.get('datetime')
	datefrom=request.GET.get('from')
	dateto=request.GET.get('to')

	people=Employee.objects.filter(supervisor__user__username=uname).values('user__username', 'region__name')
	soldsumcash = Sold.objects.all().filter(employee__supervisor__user__username=uname, date__gte=datefrom, date__lte=dateto).aggregate(earned=Sum('price') )
	salesmade = Sold.objects.all().filter(employee__supervisor__user__username=uname, date__gte=datefrom, date__lte=dateto).aggregate(count=Count('shop'))
	details = Sold.objects.filter(employee__supervisor__user__username=uname, date__gte=datefrom, date__lte=dateto).values('what__type__name', 'amount', 'price', 'what__origin__address', 'date', 'employee__user__username', 'shop__name', 'shop__address', 'shop__region__name')
	return render_to_response('repgenmanager.html',{'soldsumcash': soldsumcash, 'salesmade': salesmade, 'user': uname, 'agents':people, 'details':details, 'amount':amnt, 'warehouse':warehouse, 'datetime':datetime , 'kinds':kinds, 'pr':price} )

@login_required
def repgenagent(request):
	uname=request.GET.get('user') 
	amnt = request.GET.get('amount')
	price = request.GET.get('price')
	warehouse=request.GET.get('warehouse')
	datetime=request.GET.get('datetime')
	datefrom=request.GET.get('from')
	dateto=request.GET.get('to')

	if request.GET.get('kinds') == "1":
		kinds = Sold.objects.filter(employee__user__username=uname, date__gte=datefrom, date__lte=dateto).values('what__type__name', 'amount', 'price', 'what__origin__address', 'date', 'shop__name', 'shop__address', 'shop__region__name' ).annotate(price=Sum('price'), amount=Sum('amount'))
	else:
		kinds = ""

	soldsumcash = Sold.objects.all().filter(employee__user__username=uname, date__gte=datefrom, date__lte=dateto).aggregate(earned=Sum('price') )
	salesmade = Sold.objects.all().filter(employee__user__username=uname, date__gte=datefrom, date__lte=dateto).aggregate(count=Count('amount'))
	contractorslist = Sold.objects.filter(employee__user__username=uname, date__gte=datefrom, date__lte=dateto).values('shop__name', 'shop__address').annotate(solds=Count('shop'))
	return render_to_response('repgenagent.html', {'soldsumcash': soldsumcash, 'salesmade': salesmade, 'contractorslist': contractorslist , 'user': uname, 'kinds':kinds, 'amount':amnt, 'warehouse':warehouse, 'datetime':datetime, 'pr':price} )
