from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

import xlsxwriter

# Create your views here.


def add_to_log(u_from,u_to,d_date,i_type,s_count,a_type):
	data_to_save=action_log(user_from=u_from,user_to=u_to,\
		date_name=d_date,item_type=i_type,stock_count=s_count,\
		action_type=a_type)
	data_to_save.save()


def add_log_action(a,b,c,d,e,f,g,h,i,j,k,l,m):
	insert=stock_log_actions(\
		action_id=a,\
    	user_request=b,\
    	user_handler=c,\
    	date_input=d,\
    	date_sys=e,\
    	user_action=f,\
    	item_name=g,\
    	item_count=h,\
    	item_other=i,\
    	department=j,\
    	admin_name=k,\
    	admin_date=l,\
    	action_status=m)
	insert.save()



def  get_params():
	department_item=department.objects.all()
	import_user=data_to_import.objects.all()
	items=item_name2.objects.all()
	type_name=import_type.objects.all()
	Action=stock_log3.objects.values('action_status').distinct()
	user_req=stock_log3.objects.values('user_request').distinct()
	return department_item,import_user,items,type_name,Action,user_req


@login_required(login_url='../login')
def import_stock(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','wearhouse']
	role_control=get_user_role(str(request.user))
	if role_control not in can_access:
		return render(request,"access_denied.html",{"role_control":role_control})


	user_details=user_data.objects.filter(user_name=str(request.user))
	for i in user_details:
		print("___________________________________________")

		print(str(i.department))
		print(str(i.role_name))
		role=i.role_name
		department=i.department
		print("___________________________________________")
	if request.method == "POST":
		print("inpost")
		input_date=request.POST['date']
		import_useX=request.POST['import_user']
		#import_typeX=request.POST['import_type']
		#batch=request.POST['batch']
		#bill=request.POST['bill']
		import_item=request.POST['import_item']
		Stock=request.POST['Stock']
		Document=request.POST['Document']
		comment=request.POST['comment']
		#more=request.POST['more']
		sys_date=str(datetime.now())[:19]
		stock_data=stock_log3(user_request=import_useX,user_handler=str(request.user),date_input=input_date,date_sys=sys_date\
			,item_name=import_item,item_count=Stock,admin_name=str(request.user),admin_date=sys_date\
			,action_status="import action",info_7=comment,info_1=Document)
		stock_data.save()
		if stock_data.save():
			print("saved")
			return render(request,"import_page.html",{"info_page":"Done","import_name":import_user,\
		"items":items,"import_type":type_name\
		,"user_sys":request.user,"role":role,"department":department})
		else:
			return render(request,"import_page.html",{"import_name":import_user,\
		"items":items,"import_type":type_name\
		,"user_sys":request.user,"role":role,"department":department,"role_control":role_control,\
		"ADD":1})
	else:
		return render(request,"import_page.html",{"import_name":import_user,"items":items,"import_type":type_name\
		,"user_sys":request.user,"role":role,"department":department,"role_control":role_control})

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('../login')


@login_required(login_url='../login')
def export(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','client']
	role_control=get_user_role(str(request.user))
	if role_control not in can_access:
		return render(request,"access_denied.html",{"role_control":role_control})


	user_details=user_data.objects.filter(user_name=str(request.user))
	for i in user_details:
		print("___________________________________________")

		print(str(i.department))
		print(str(i.role_name))

		role=i.role_name
		department=i.department

		print("___________________________________________")

	if request.method == "POST":
		input_date=request.POST['date']
		import_item=request.POST['import_item']
		Stock="-" + str(request.POST['Stock'])
		comment=request.POST['comment']
		sys_date=str(datetime.now())[:19]

		stock_data=stock_log3(user_request=str(request.user),department=str(department),user_handler="1st approval",date_input=input_date,date_sys=sys_date\
			,item_name=import_item,item_count=Stock,admin_name=str(request.user),admin_date=sys_date\
			,action_status="export request",info_7=comment,info_2=str(role),\
			info_3=str(datetime.now()))
		stock_data.save()
		'''
		stock_data=stock_log3(user_request=str(request.user),user_handler="1st approval",date_input=input_date,date_sys=sys_date\
			,item_name2=import_item,item_count=Stock,item_other=more,admin_name=str(request.user),admin_date=sys_date\
			,action_status="import action")
		'''
		if stock_data.save():
			print("saved")
			return render(request,"export_page.html",{"info_page":"Done","import_name":import_user,\
		"items":items,"import_type":type_name\
		,"user_sys":request.user,"role":role,"department":department,\
		"role_control":role_control})
		else:
			return render(request,"export_page.html",{"ADD":1,"import_name":import_user,\
		"items":items,"import_type":type_name\
		,"user_sys":request.user,"role":role,"department":department,\
		"role_control":role_control})
	else:
		return render(request,"export_page.html",{"import_name":import_user,"items":items,"import_type":type_name\
		,"user_sys":request.user,"role":role,"department":department,\
		"role_control":role_control})

def index(request):
	return render(request,"nav.html",{})


def login_page(request):
	if request.method == "POST":
		username=request.POST['username']
		password=request.POST['password']
		auth = authenticate(request,username=username,password=password)
		if auth is not None:
			login(request,auth)
			return HttpResponseRedirect('../')			
		else:
			print("Error in user")
			return render(request,"login.html",{"data":"failed"})
	else:
		return render(request,"login.html",{"data":"none"})

@login_required(login_url='../login')
def Home(request):
	can_access=['admin','wearhouse','manger','client']
	role_control=get_user_role(str(request.user))
	if role_control not in can_access:
		return render(request,"access_denied.html",{"role_control":role_control})
	'''
	if request.method == "POST":
		data=stock_log3.objects.all()
		generate_report(data)
		return render(request,"home_page.html",{"role_control":role_control})
	'''
	return render(request,"home_page.html",{"role_control":role_control})




def add_user(request):
	information=User.objects.all()
	if request.method == "POST" and request.POST['btn'] == "save":
		username=request.POST['username']
		password=request.POST['password']
		email=request.POST['email']
		depart=request.POST['depr']
		role=request.POST['rol']
		try:
			user = User.objects.create_user(username,email,password)
			user.first_name = depart
			user.last_name = role
			user.save()
			return render(request,"add_user.html",{"information":information,"info":"Success"})
		except Exception as e:
			return render(request,"add_user.html",{"info":"failed " + str(e),"username":username,"Password":password\
				,"email":email,"Dep":depart})

	if request.method == "POST" and request.POST['btn'] == "find":
		username=request.POST['username']
		data_=User.objects.all().filter(username=str(username))
		return render(request,"add_user.html",{"username":data_.username,"Password":data_.password\
				,"email":data_.first_name,"Dep":data_.last_name})



	return render(request,"add_user.html",{"information":information})

def remove_user(request,username):
	try:
		clear__=User.objects.filter(username=str(username)).delete()
		return HttpResponseRedirect('../add_user')
		#return render(request,"add_user.html",{"info":"Success Delete user " + str(username)})
	except Exception as e:
		return render(request,"add_user.html",{"info":"Failed Delete user " + str(e)})

def test(request):
	return render(request,"nav.html",{})

@login_required(login_url='../login')
def request_view(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	page = request.GET.get('page')

	can_access=['admin','client','warehouse']
	role_control=get_user_role(str(request.user))
	if role_control not in can_access:
		return render(request,"access_denied.html",{"role_control":role_control})

	#all_data=stock_log3.objects.filter(date_input__range=[sd,ed]).order_by('-date_sys')
	all_data=stock_log3.objects.all().order_by('-date_sys')
	paginator = Paginator(all_data, 100)
	request_data = paginator.get_page(page)


	if request.method == "POST":
		sd=request.POST['start']
		ed=request.POST['end']

		id_actoin=request.POST['id']
		req_user=request.POST['user_req']
		item_import=request.POST['import_item']
		dep_item=request.POST['items_dep']
		Action_sts=request.POST['Action_name']
		action=request.POST['action']

		if request.POST.get('id'):
			all_data=all_data.filter(action_id=id_actoin)

		if request.POST.get('user_req'):
			all_data=all_data.filter(user_request=req_user)

		if request.POST.get('import_item'):
			all_data=all_data.filter(item_name=item_import)

		if request.POST.get('items_dep'):
			all_data=all_data.filter(department=dep_item)

		if request.POST.get('Action_name'):
			all_data=all_data.filter(action_status=Action_sts)

		
		page = request.GET.get('page')
		#all_data=all_data.filter(date_input__range=[sd,ed])
		paginator = Paginator(all_data, 2)
		request_data = paginator.get_page(page)

		if action == "filter":
			return render(request,"request_page.html",{"requests":request_data,"role_control":role_control,\
				"items":items,"items_dep":department_item,"items_Action":Action,"user_req":user_req,\
				"sd":sd,"ed":ed,"id":id_actoin,"user_req_data":req_user,"import_item_n":item_import,\
				"items_dep_val":dep_item,"Action_name_val":Action_sts})

		if action == "Export":
			file_name="Report_" + str(datetime.now()).replace(":","_")[:19]
			generate_report_admin(all_data,str(file_name))
			report_info=report_log(report_user=str(request.user),report_date=str(datetime.now()),report_name=file_name + ".xlsx")
			report_info.save()
			return render(request,"request_page.html",{"requests":request_data,"role_control":role_control,\
				"sd":sd,"ed":ed,"id":id_actoin,"user_req_data":req_user,"import_item_n":item_import,\
				"items_dep_val":dep_item,"Action_name_val":Action_sts,"info":1})

	all_data=stock_log3.objects.all().order_by('-date_sys')
	return render(request,"request_page.html",{"requests":request_data,"role_control":role_control,\
		"items":items,"items_dep":department_item,"items_Action":Action,"user_req":user_req})


@login_required(login_url='../login')
def request_view_user(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','client','warehouse']
	role_control=get_user_role(str(request.user))
	if role_control not in can_access:
		return render(request,"access_denied.html",{"role_control":role_control})

	
	if request.method == "POST":
		sd=request.POST['start']
		ed=request.POST['end']
		action=request.POST['action']
		all_data=stock_log3.objects.filter(\
			date_input__range=[sd,ed],\
			user_request=str(request.user)).order_by('-date_sys')

		if action == "filter":
			return render(request,"request_page_user.html",{"data_view":all_data,"role_control":role_control,\
				"sd":sd,"ed":ed})

		if action == "Export":
			file_name="Report_" + str(datetime.now()).replace(":","_")[:19]
			generate_report_user(all_data,str(file_name))
			report_info=report_log(report_user=str(request.user),report_date=str(datetime.now()),report_name=file_name + ".xlsx")
			report_info.save()
			return render(request,"request_page_user.html",{"data_view":all_data,"role_control":role_control,\
				"sd":sd,"ed":ed})

	all_data=stock_log3.objects.filter(user_request=str(request.user)).order_by('-date_sys')
	return render(request,"request_page_user.html",{"data_view":all_data,"role_control":role_control})




@login_required(login_url='../login')
def import_req(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','warehouse','client']
	role_control=get_user_role(str(request.user))
	if role_control in can_access:
		pass
	else:
		return render(request,"access_denied.html",{"role_control":role_control})


	all_data=stock_log3.objects.filter(action_status="import action").order_by('-date_sys')
	if request.method == "POST":
		id_value=request.POST['ID']
		I=request.POST['item_n']
		C=request.POST['item_c']
		action_value=request.POST['action']
		stock_log3.objects.filter(action_id=id_value).update(action_status=action_value,\
			admin_name=str(request.user),\
			date_sys=str(datetime.now())[:19])
		return render(request,"import_req.html",{"data_view":all_data,"role_control":role_control})

	return render(request,"import_req.html",{"data_view":all_data,"role_control":role_control})



@login_required(login_url='../login')
def export_req(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','warehouse']
	role_control=get_user_role(str(request.user))
	if role_control in can_access:
		pass
	else:
		return render(request,"access_denied.html",{"role_control":role_control})


	all_data=stock_log3.objects.filter(action_status="export request",user_handler="1st approval").order_by('-date_sys')
	if request.method == "POST":
		id_value=request.POST['ID']
		I=request.POST['item_n']
		C=request.POST['item_c']
		action_value=request.POST['action']
		if action_value == "Export Rejected 1st":
			stock_log3.objects.filter(action_id=id_value).update(action_status=action_value,\
			admin_date=str(datetime.now())[:19],date_sys=str(datetime.now())[:19],\
			admin_name=str(request.user),\
			user_handler="")
		else:
			stock_log3.objects.filter(action_id=id_value).update(action_status=action_value,\
			admin_date=str(datetime.now())[:19],date_sys=str(datetime.now())[:19],\
			admin_name=str(request.user),\
			user_handler="2nd approval")

		return render(request,"export_req.html",{"data_view":all_data,"role_control":role_control})

	return render(request,"export_req.html",{"data_view":all_data,"role_control":role_control})

@login_required(login_url='../login')
def export_req_2(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','client']
	role_control=get_user_role(str(request.user))
	if role_control not in can_access:
		return render(request,"access_denied.html",{"role_control":role_control})

	all_data=stock_log3.objects.filter(action_status="export 1st aprroved",user_handler="2nd approval").order_by('-date_sys')
	if request.method == "POST":
		id_value=request.POST['ID']
		I=request.POST['item_n']
		C=request.POST['item_c']
		action_value=request.POST['action']
		if action_value == "Export Rejected 2nd":
			stock_log3.objects.filter(action_id=id_value).update(action_status=action_value,\
			admin_date=str(datetime.now())[:19],date_sys=str(datetime.now())[:19],\
			admin_name=str(request.user),\
			user_handler="")
		else:
			stock_log3.objects.filter(action_id=id_value).update(action_status=action_value,\
			admin_date=str(datetime.now())[:19],date_sys=str(datetime.now())[:19],\
			admin_name=str(request.user),\
			user_handler="2nd approval")

		return render(request,"export_req_2.html",{"data_view":all_data,"role_control":role_control})

	return render(request,"export_req_2.html",{"data_view":all_data,"role_control":role_control})


@login_required(login_url='../login')
def stock_req(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','warehouse']
	role_control=get_user_role(str(request.user))
	print("________________________" + str(role_control))
	if role_control in can_access:
		pass
	else:
		return render(request,"access_denied.html",{"role_control":role_control})

	if request.method == "POST":
		item_req=request.POST['item_req']
		itemD=item_name2.objects.filter(item__contains=item_req)
	else:
		item_req=''
		itemD=item_name2.objects.all()
	
	item_array=[]
	item_type=[]
	item_id=[]
	first_stock=[]
	item_stock=[]
	item_consumed=[]
	item_import=[]
	for i in itemD:
		item_array.append(str(i.item))
		item_type.append(str(i.unit))
		first_stock.append(str(i.curent_stock))
		item_id.append(str(i.item_number))

	for x in item_array:
		stock_data=stock_log3.objects.filter(item_name=str(x),action_status__in=("In Stock","Export Approved"))
		total=0
		for z in stock_data:
			total+=int(z.item_count)
		item_stock.append(total)

		stock_data=stock_log3.objects.filter(item_name=str(x),action_status=("Export Approved"))
		consumed=0
		for z in stock_data:
			consumed+=int(z.item_count)
		item_consumed.append(consumed)

		stock_data=stock_log3.objects.filter(item_name=str(x),action_status=("In Stock"))
		import_c=0
		for z in stock_data:
			import_c+=int(z.item_count)
		item_import.append(import_c)


	list_zip=zip(item_id,item_type,item_array,item_stock,item_consumed,item_import,first_stock)

	return render(request,"stock_req.html",{"list_zip":list_zip,"role_control":role_control\
		,"item_req":item_req})

@login_required(login_url='../login')
def report_page(request):
	department_item,import_user,items,type_name,Action,user_req=get_params()
	can_access=['admin','warehouse','client','manger']
	role_control=get_user_role(str(request.user))
	if role_control in can_access:
		pass
	else:
		return render(request,"access_denied.html",{"role_control":role_control})

	all_data=report_log.objects.filter(report_user=str(request.user)).order_by('-action_id')
	return render(request,"report_req.html",{"data_view":all_data,\
		"role_control":role_control})


def get_user_role(user):
	data_to_check=user_data.objects.filter(user_name=user)
	role=''
	for i in data_to_check:
		role=i.role_name
	return str(role)


def generate_report_admin(data,name):
	workbook = xlsxwriter.Workbook("assets\\report_export\\" + str(name) + ".xlsx")
	worksheet = workbook.add_worksheet("Stock Log Data")
	row = 1
	col = 0
	worksheet.write(0, 0,"REQUEST ID")
	worksheet.write(0, 1,"USER REQUEST")
	worksheet.write(0, 2,"USER HANDLER")
	worksheet.write(0, 3,"DATE INPUT")
	worksheet.write(0, 4,"DATE SYSTEM")
	worksheet.write(0, 5,"USER ACTION")
	worksheet.write(0, 6,"ITEM NAME")
	worksheet.write(0, 7,"ITEM COUNT")
	worksheet.write(0, 8,"OTHER DATA")
	worksheet.write(0, 9,"REF. NUMBER")
	worksheet.write(0, 10,"ٌUSER ROLE")
	worksheet.write(0, 11,"FIRST REQUEST TIME")
	worksheet.write(0, 12,"INFO_4")
	worksheet.write(0, 13,"INFO_5")
	worksheet.write(0, 14,"INFO_6")
	worksheet.write(0, 15,"COMMENT")
	worksheet.write(0, 16,"DEPARTMENT")
	worksheet.write(0, 17,"ADMIN NAME")
	worksheet.write(0, 18,"ADMIN DATE")
	worksheet.write(0, 19,"ACTION STATUS")

	for i in data:
		print(str(i))
		worksheet.write(row, col,     i.action_id)
		worksheet.write(row, col + 1, i.user_request)
		worksheet.write(row, col + 2, i.user_handler)
		worksheet.write(row, col + 3, i.date_input)
		worksheet.write(row, col + 4, str(i.date_sys))
		worksheet.write(row, col + 5, i.user_action)
		worksheet.write(row, col + 6, str(i.item_name))
		worksheet.write(row, col + 7, int(i.item_count))
		worksheet.write(row, col + 8, str(i.item_other))
		worksheet.write(row, col + 9, str(i.info_1))
		worksheet.write(row, col + 10, str(i.info_2))
		worksheet.write(row, col + 11, str(i.info_3))
		worksheet.write(row, col + 12, str(i.info_4))
		worksheet.write(row, col + 13, str(i.info_5))
		worksheet.write(row, col + 14, str(i.info_6))
		worksheet.write(row, col + 15, str(i.info_7))
		worksheet.write(row, col + 16, str(i.department))
		worksheet.write(row, col + 17, str(i.admin_name))
		worksheet.write(row, col + 18, str(i.admin_date))
		worksheet.write(row, col + 19, str(i.action_status))

		row += 1

	itemD=item_name2.objects.all()
	item_array=[]
	item_id=[]
	item_type=[]
	first_stock=[]
	item_stock=[]
	item_consumed=[]
	item_import=[]
	for i in itemD:
		item_array.append(str(i.item))
		item_type.append(str(i.unit))
		first_stock.append(str(i.curent_stock))
		item_id.append(str(i.item_number))


	for x in item_array:
		stock_data=stock_log3.objects.filter(item_name=str(x),action_status__in=("In Stock","Export Approved"))
		total=0
		for z in stock_data:
			total+=int(z.item_count)
		item_stock.append(total)

		stock_data=stock_log3.objects.filter(item_name=str(x),action_status=("Export Approved"))
		consumed=0
		for z in stock_data:
			consumed+=int(z.item_count)
		item_consumed.append(consumed)

		stock_data=stock_log3.objects.filter(item_name=str(x),action_status=("In Stock"))
		import_c=0
		for z in stock_data:
			import_c+=int(z.item_count)
		item_import.append(import_c)




	list_zip=zip(item_type,item_id,item_array,item_stock,item_consumed,item_import,first_stock)

	worksheet = workbook.add_worksheet("STOCK")
	row = 1
	col = 0
	worksheet.write(0, 0,"UNIT")
	worksheet.write(0, 1,"ID")
	worksheet.write(0, 2,"ITEM NAME")
	worksheet.write(0, 3,"STOCK")
	worksheet.write(0, 4,"CONSUMED")
	worksheet.write(0, 5,"IMPORT")
	worksheet.write(0, 6,"FIRST STOCK")
	worksheet.write(0, 7,"Report GEN at " + str(datetime.now()))

	for name,id_name,unit,count,cuns,impo,fs in list_zip:
		worksheet.write(row, col,     name)
		worksheet.write(row, col + 1, id_name)
		worksheet.write(row, col + 2, unit)
		worksheet.write(row, col + 3, count)
		worksheet.write(row, col + 4, cuns)
		worksheet.write(row, col + 5, impo)
		worksheet.write(row, col + 6, fs)
		row += 1

	workbook.close()

def generate_report_user(data,name):
	workbook = xlsxwriter.Workbook("assets\\report_export\\" + str(name) + ".xlsx")
	worksheet = workbook.add_worksheet("Stock Log Data")
	row = 1
	col = 0
	worksheet.write(0, 0,"REQUEST ID")
	worksheet.write(0, 1,"USER REQUEST")
	worksheet.write(0, 2,"USER HANDLER")
	worksheet.write(0, 3,"DATE INPUT")
	worksheet.write(0, 4,"DATE SYSTEM")
	worksheet.write(0, 5,"USER ACTION")
	worksheet.write(0, 6,"ITEM NAME")
	worksheet.write(0, 7,"ITEM COUNT")
	worksheet.write(0, 8,"OTHER DATA")
	worksheet.write(0, 9,"REF. NUMBER")
	worksheet.write(0, 10,"ٌUSER ROLE")
	worksheet.write(0, 11,"FIRST REQUEST TIME")
	worksheet.write(0, 12,"INFO_4")
	worksheet.write(0, 13,"INFO_5")
	worksheet.write(0, 14,"INFO_6")
	worksheet.write(0, 15,"COMMENT")
	worksheet.write(0, 16,"DEPARTMENT")
	worksheet.write(0, 17,"ADMIN NAME")
	worksheet.write(0, 18,"ADMIN DATE")
	worksheet.write(0, 19,"ACTION STATUS")

	for i in data:
		print(str(i))
		worksheet.write(row, col,     i.action_id)
		worksheet.write(row, col + 1, i.user_request)
		worksheet.write(row, col + 2, i.user_handler)
		worksheet.write(row, col + 3, i.date_input)
		worksheet.write(row, col + 4, str(i.date_sys))
		worksheet.write(row, col + 5, i.user_action)
		worksheet.write(row, col + 6, str(i.item_name))
		worksheet.write(row, col + 7, int(i.item_count))
		worksheet.write(row, col + 8, str(i.item_other))
		worksheet.write(row, col + 9, str(i.info_1))
		worksheet.write(row, col + 10, str(i.info_2))
		worksheet.write(row, col + 11, str(i.info_3))
		worksheet.write(row, col + 12, str(i.info_4))
		worksheet.write(row, col + 13, str(i.info_5))
		worksheet.write(row, col + 14, str(i.info_6))
		worksheet.write(row, col + 15, str(i.info_7))
		worksheet.write(row, col + 16, str(i.department))
		worksheet.write(row, col + 17, str(i.admin_name))
		worksheet.write(row, col + 18, str(i.admin_date))
		worksheet.write(row, col + 19, str(i.action_status))

		row += 1

	'''
	itemD=item_name2.objects.all()
	item_array=[]
	item_id=[]
	item_type=[]
	first_stock=[]
	item_stock=[]
	item_consumed=[]
	item_import=[]
	for i in itemD:
		item_array.append(str(i.item))
		item_type.append(str(i.unit))
		first_stock.append(str(i.curent_stock))
		item_id.append(str(i.item_number))


	for x in item_array:
		stock_data=stock_log3.objects.filter(item_name=str(x),action_status__in=("In Stock","Export Approved"))
		total=0
		for z in stock_data:
			total+=int(z.item_count)
		item_stock.append(total)

		stock_data=stock_log3.objects.filter(item_name=str(x),action_status=("Export Approved"))
		consumed=0
		for z in stock_data:
			consumed+=int(z.item_count)
		item_consumed.append(consumed)

		stock_data=stock_log3.objects.filter(item_name=str(x),action_status=("In Stock"))
		import_c=0
		for z in stock_data:
			import_c+=int(z.item_count)
		item_import.append(import_c)




	list_zip=zip(item_type,item_id,item_array,item_stock,item_consumed,item_import,first_stock)

	worksheet = workbook.add_worksheet("STOCK")
	row = 1
	col = 0
	worksheet.write(0, 0,"UNIT")
	worksheet.write(0, 1,"ID")
	worksheet.write(0, 2,"ITEM NAME")
	worksheet.write(0, 3,"STOCK")
	worksheet.write(0, 4,"CONSUMED")
	worksheet.write(0, 5,"IMPORT")
	worksheet.write(0, 6,"FIRST STOCK")
	worksheet.write(0, 7,"Report GEN at " + str(datetime.now()))

	for name,id_name,unit,count,cuns,impo,fs in list_zip:
		worksheet.write(row, col,     name)
		worksheet.write(row, col + 1, id_name)
		worksheet.write(row, col + 2, unit)
		worksheet.write(row, col + 3, count)
		worksheet.write(row, col + 4, cuns)
		worksheet.write(row, col + 5, impo)
		worksheet.write(row, col + 6, fs)
		row += 1
	'''
	workbook.close()