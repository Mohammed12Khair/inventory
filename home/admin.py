from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(roles)
admin.site.register(user_data)
admin.site.register(department)
admin.site.register(data_to_import)
#admin.site.register(item_name)
admin.site.register(import_type)
#admin.site.register(stock_log)
admin.site.register(stock_log3)
admin.site.register(action_log)
#admin.site.register(stock_log_all)
admin.site.register(stock_log_hist)
admin.site.register(report_log)
admin.site.register(item_name2)