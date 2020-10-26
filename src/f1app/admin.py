from django.contrib import admin
from f1app.models import employee

class employeeAdmin(admin.ModelAdmin):
    # 第三種方式，加入 ModelAdmin 類別，定義顯示欄位、欄位過濾資料、搜尋和排序
    list_display = ('emp_name', 'emp_id', 'rank', 'salary', 'phone_number', 'sex',
                    'birthdate', 'recruit_date', 'address', 'photo', 'status')

    list_filter = ('emp_name', 'emp_id')
    search_fields = ('emp_name',)
    ordering = ('emp_id',)

admin.site.register(employee, employeeAdmin)
