from django.db import models


# Create your models here.
class roles(models.Model):
	role_id=models.CharField(max_length=100,default='')
	role_name = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.role_name

class department(models.Model):
	dep_id=models.CharField(max_length=100,default='')
	dep_name = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.dep_name

class data_to_import(models.Model):
	user_name = models.CharField(max_length=100,default='')
	number = models.CharField(max_length=100,default='')
	email = models.CharField(max_length=100,default='')
	company = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.user_name

class import_type(models.Model):
	import_type = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.import_type


class user_data(models.Model):
	user_name = models.CharField(max_length=100,default='')
	role_name = models.ForeignKey(roles,on_delete=models.CASCADE)#null=True,blank=True)
	department = models.ForeignKey(department,on_delete=models.CASCADE)#null=True,blank=True)
	email = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.user_name


class item_name2(models.Model):
	item_number=models.AutoField(primary_key=True)
	item = models.CharField(max_length=100,default='')
	unit = models.CharField(max_length=100,default='')
	curent_stock = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.item

#not used 
class item_name(models.Model):
	item = models.CharField(max_length=100,default='')
	unit = models.CharField(max_length=100,default='')
	curent_stock = models.CharField(max_length=100,default='')
	def __str__(self):
		return self.item


class stock_log3(models.Model):
	action_id=models.AutoField(primary_key=True)
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	info_1=models.CharField(max_length=100,default='')
	info_2=models.CharField(max_length=100,default='')
	info_3=models.CharField(max_length=100,default='')
	info_4=models.CharField(max_length=100,default='')
	info_5=models.CharField(max_length=100,default='')
	info_6=models.CharField(max_length=100,default='')
	info_7=models.CharField(max_length=1000,default='')
	item_other=models.CharField(max_length=100,default='')
	department=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')

class report_log(models.Model):
	action_id=models.AutoField(primary_key=True)
	report_user=models.CharField(max_length=100,default='')
	report_date=models.CharField(max_length=100,default='')
	report_name=models.CharField(max_length=100,default='')





#not used
class stock_log2(models.Model):
	action_id=models.AutoField(primary_key=True)
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	department=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')


#to show log
class stock_log_hist(models.Model):
	action_id=models.CharField(max_length=100,default='')
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	department=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')

#this not used
class stock_log_actions(models.Model):
	action_id=models.AutoField(primary_key=True)
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	department=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')

#this is not userd 
class stock_log_all(models.Model):
	action_id=models.AutoField(primary_key=True)
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	department=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')


#this is not userd 
class stock_log(models.Model):
	action_id=models.AutoField(primary_key=True)
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')


class action_log(models.Model):
	action_no=models.AutoField(primary_key=True)
	user_from=models.CharField(max_length=100,default='')
	user_to=models.CharField(max_length=100,default='')
	date_name=models.CharField(max_length=100,default='')
	item_type=models.CharField(max_length=100,default='')
	stock_count=models.CharField(max_length=100,default='')
	action_type=models.CharField(max_length=100,default='')

class reports(models.Model):
	action_no=models.AutoField(primary_key=True)
	date_sys=models.CharField(max_length=100,default='')
	user=models.CharField(max_length=100,default='')
	file_path=models.CharField(max_length=100,default='')









'''
class items_log(models.Model):
	action_id=models.CharField(max_length=100,default='')
	user_request=models.CharField(max_length=100,default='')
	user_handler=models.CharField(max_length=100,default='')
	date_input=models.CharField(max_length=100,default='')
	date_sys=models.CharField(max_length=100,default='')
	user_action=models.CharField(max_length=100,default='')
	item_name=models.CharField(max_length=100,default='')
	item_count=models.CharField(max_length=100,default='')
	item_other=models.CharField(max_length=100,default='')
	admin_name=models.CharField(max_length=100,default='')
	admin_date=models.CharField(max_length=100,default='')
	action_status=models.CharField(max_length=100,default='')




class items_all(models.Model):
	item = models.CharField(max_length=100,default='')
	uom  = models.CharField(max_length=100,default='')
	Stock  = models.CharField(max_length=100,default='')
	import_stock  = models.CharField(max_length=100,default='')
	consumed_stock  = models.CharField(max_length=100,default='')
	curent_stock  = models.CharField(max_length=100,default='')

class items_log(models.Model):
	batch_number = models.CharField(max_length=100,default='')
	invoice_number = models.CharField(max_length=100,default='')
	item_name = models.CharField(max_length=100,default='')
	user_handler = models.CharField(max_length=100,default='')
	import_type = models.CharField(max_length=100,default='')
	count=models.IntegerField(default='')
	'''




