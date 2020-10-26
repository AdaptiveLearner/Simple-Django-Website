from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import connection
from datetime import date
from django.http import HttpResponse
import os
import json

from f1app.models import employee, country, agent, dependent, dependemp
from f1app.forms import PostForm_employee, PostForm_country, PostForm_agent, PostForm_dependent, PostForm_dependemp

def userInterface(request):

    cursor = connection.cursor()

### employee
    today = date.today()
    averageAge = 0
    cnt = 0
    monthSalary = 0   
    averageSalary = 0   
    str1 = "SELECT emp_id, emp_name, rank, salary, birthdate FROM f1app_employee WHERE status='正常'"
    print(str1)
    cursor.execute(str1)
    elist = []
    for s in cursor.fetchall():
        try:
            dateStr = str(s[4])
            year, month, day = [int(s) for s in dateStr.split('/')]
            age = today.year - year - ((today.month, today.day) < (month, day))
            print("Age[" + str(s[0]) + "] = " + str(age))
            averageAge += age

            monthSalary += int(s[3])

            elist.append({ 'id': str(s[0]), 'name': str(s[1]), 'rank': str(s[2]),
            'salary': str(s[3]), 'birthdate': dateStr, 'age': str(age) })
            cnt += 1
        except:
            age = 0
            print("ERR on Employee Interface")

    if cnt == 0:
        averageSalary = 0
        averageAge = 0
    else:
        averageSalary = round(monthSalary / cnt)
        averageAge = round(averageAge / cnt)

    yearSalary = 12 * monthSalary
    weekSalary = round(yearSalary / 12)

### country
    cntDiplomatic = 0
    cntNonDiplomatic = 0
    str1 = """SELECT country_code, country_name, continent_attr, country_population, country_area,
        has_diplomatic_relatioin FROM f1app_country"""
    print(str1)
    cursor.execute(str1)
    clist = []
    for s in cursor.fetchall():
        try:
            code = str(s[0])
            name = str(s[1])
            continent = str(s[2])
            population = str(s[3])
            area = str(s[4])
            diplomatic = str(s[5])
            clist.append({ 'code': code, 'name': name, 'continent': continent,
            'population': population, 'area': area, 'diplomatic': diplomatic} )
            if diplomatic == "Yes":
                cntDiplomatic += 1
            else:
                cntNonDiplomatic += 1
        except:
            print("ERR on Country Interface")

### agent
    str1 = """SELECT a.emp_id, a.country_code, e.emp_name, a.arrival_date, c.ambassador_name, a.status
            FROM f1app_agent a
            LEFT JOIN f1app_country c ON a.country_code = c.country_code
            LEFT JOIN f1app_employee e ON a.emp_id = e.emp_id"""    
    print(str1)
    cursor.execute(str1)
    list1 = cursor.fetchall()
    alist = []
    for s in list1:
        try:
            aid = str(s[0])
            acode = str(s[1])
            astatus = str(s[5])
            alist.append({ 'id': aid, 'code': acode, 'name': str(s[2]), 'date': str(s[3]),
                'ambassador': str(s[4]), 'status': astatus })
        except:
            print("ERR on Agent Interface")

    str1 = "SELECT country_code, count(*) FROM f1app_agent GROUP BY country_code"
    print(str1)
    cursor.execute(str1)
    list1 = cursor.fetchall()
    aclist = []
    for s in list1:
        try:
            aclist.append({ 'code': str(s[0]), 'cnt': str(s[1]) })
        except:
            print("ERR on Agent Interface")


### dependent
    str1 = """SELECT m.emp_id, d.dep_id, d.dep_name, d.dep_sex, m.relation, d.birthdate, m.status
            FROM f1app_dependent d
            LEFT JOIN f1app_dependemp m ON d.dep_id = m.dep_id"""
    print(str1)
    cursor.execute(str1)
    dlist = []
    cntMale = 0
    cntFemale = 0
    ageMale = 0
    ageFemale = 0
    for s in cursor.fetchall():
        try:
            emp_id = str(s[0])
            dep_id = str(s[1])
            sex = str(s[3])            
            status = str(s[6])

            birthdate = str(s[5])
            year, month, day = [int(s) for s in birthdate.split('/')]
            age = today.year - year - ((today.month, today.day) < (month, day))

            if sex == 'M':
                cntMale += 1
                ageMale += age
            else:
                cntFemale += 1
                ageFemale += age

            dlist.append({ 'emp_id': emp_id, 'dep_id': dep_id, 'dep_name': str(s[2]), 'dep_sex': sex,
                            'relation': str(s[4]), 'birthdate': birthdate, 'age': age, 'status': status })
        except:
            print("ERR on Dependent Interface")

    if cntMale != 0: 
        ageMale = round(ageMale/cntMale)
    if cntFemale != 0: 
        ageFemale = round(ageFemale/cntFemale)


### cross-table
#    str1 = "SELECT COUNT(DISTINCT emp_id) FROM f1app_country"
    str1 = """select count(distinct emp_id) from f1app_agent where ( status = '正常'
            and country_code in (select country_code from f1app_country where continent_attr = 'NorthAmerica'))""" 
    cursor.execute(str1)
    agentContinent = str(cursor.fetchone()[0])
    print('#continents = ' + agentContinent)

    return render(request, "userInterface.html", locals())


def myQuery():
    print('\nmy query')
    cursor = connection.cursor()

# #continents
    str1 = "SELECT COUNT(DISTINCT continent_attr) FROM f1app_country"
    cursor.execute(str1)
    print('#continents = ' + str(cursor.fetchone()[0]))

# #employees
    str1 = "SELECT COUNT(*) FROM f1app_employee"
    cursor.execute(str1)
    cnt = str(cursor.fetchone()[0])
    print('#employees = ' + cnt)

# average salary
    str1 = "SELECT AVG(salary) FROM f1app_employee"
    cursor.execute(str1)
    average = int(cursor.fetchone()[0])
    print('Average salary = ' + str(average))

# rank <10
    str1 = "SELECT COUNT(*) FROM f1app_employee WHERE rank<10"
    cursor.execute(str1)
    Crank = int(cursor.fetchone()[0])
    print('(#rank<10) = ' + str(Crank))

# Age
    str1 = "SELECT emp_name, birthdate FROM f1app_employee"
    cursor.execute(str1)
    today = date.today()
    for p in cursor.fetchall():
        try:
            DateStr = str(p[1])
            year, month, day = [int(s) for s in DateStr.split('/')]
            age = today.year - year - ((today.month, today.day) < (month, day))
            print("Age[" + str(p[0]) + "] = " + str(age))
        except:
            age = 0
            print("ERR: Age Format")

# foreign keys
    emp = employee.objects.get(emp_id='A100000001')
    fk = emp.agent_set.all()
    for f in fk:
        print(str(f.emp_name) + " " + str(f.country_code) +
              " " + str(f.arrival_date))


def FindMaxAgentID():
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM f1app_agent")
    maxID = int(cursor.fetchone()[0])
    print("Max AgentID: " + str(maxID))
    return maxID

def FindMaxDependempID():
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM f1app_dependemp")
    maxID = int(cursor.fetchone()[0])
    print("Max DependentID: " + str(maxID))
    return maxID

def employeeList():
    cursor = connection.cursor()
    cursor.execute("SELECT emp_id FROM f1app_employee")
    idlist = cursor.fetchall()
    print(idlist)
    plist = []
    for p in idlist:
        plist.append(str(p[0]))
    return plist
#    return json.dumps(plist)


def countryList():
    cursor = connection.cursor()
    cursor.execute("SELECT country_code FROM f1app_country")
    idlist = cursor.fetchall()
    print(idlist)
    plist = []
    for p in idlist:
        plist.append(str(p[0]))
    return plist
#    return json.dumps(plist)


def dependentList():
    cursor = connection.cursor()
    cursor.execute("SELECT dep_id FROM f1app_dependent")
    idlist = cursor.fetchall()
    print(idlist)
    plist = []
    for p in idlist:
        plist.append(str(p[0]))
    return plist
#    return json.dumps(plist)


def countryNames():
    cursor = connection.cursor()
    cursor.execute("SELECT country_name FROM f1app_country")
    idlist = cursor.fetchall()
    print(idlist)
    plist = []
    for p in idlist:
        plist.append(str(p[0]))
    return json.dumps(plist)


def index(request):
    print('in dex')
    employees = employee.objects.all().order_by('emp_id')  # 讀取資料表, 依 id 遞增排序
    countries = country.objects.all().order_by('country_code')
    dependents = dependent.objects.all().order_by('dep_id')
    agents = agent.objects.all().order_by('id')
    dependemps = dependemp.objects.all().order_by('id')

#    myQuery()
    return render(request, "index.html", locals())
#    return render( request, "index.html", {'current time' : str(datetime.now())} )


def EmployeeDuplicate(id):
    print('\ncheck if Employee duplicate')
    cursor = connection.cursor()
    str1 = "SELECT COUNT(*) FROM f1app_employee WHERE emp_id='" + id +"'"
    print(str1)
    cursor.execute(str1)
    s = str(cursor.fetchone()[0])
    print("s=" + s)
    return  ( s != '0')


def new_employee(request):  # 新增資料，資料必須驗證
    print('new employee')
    imgs = ["bob", "conan", "elsa", "fiona", "kawhi", "mario", "maruko", "woody", "yoda"]

    if request.method == "POST":  # 如果是以POST方式才處理
        postform = PostForm_employee(request.POST)  # 建立forms物件
        if postform.is_valid():  # 通過forms驗證
            print('employee postform.cleaned_data')
            emp_id = postform.cleaned_data['emp_id']

            if EmployeeDuplicate(emp_id):
                print('ERR: employee ID duplicates')   
                message = '員工身分證字號重複, 請重新輸入' 
            else:

                emp_name = postform.cleaned_data['emp_name']
                rank = postform.cleaned_data['rank']
                salary = postform.cleaned_data['salary']
                birthdate = postform.cleaned_data['birthdate']

                phone_number = postform.cleaned_data['phone_number']
                sex = postform.cleaned_data['sex']
                recruit_date = postform.cleaned_data['recruit_date']
                address = postform.cleaned_data['address']
                photo = postform.cleaned_data['photo']
                status = postform.cleaned_data['status']
                # 新增一筆記錄
                unit = employee.objects.create(emp_name=emp_name, emp_id=emp_id, rank=rank, salary=salary,
                        phone_number=phone_number, sex=sex, birthdate=birthdate,
                        recruit_date=recruit_date, address=address, photo=photo, status=status)
                return redirect('/index/')
        else:
            message = '驗證碼錯誤！'
    else:
        message = '綠色欄位必須輸入！'        
        postform = PostForm_employee()
    return render(request, "new_employee.html", locals())


def CountryDuplicate(code, name):
    print('\ncheck if Country duplicate')
    cursor = connection.cursor()
    str1 = "SELECT COUNT(*) FROM f1app_country WHERE country_code='" + code +"' OR country_name='" + name + "'"
    print(str1)
    cursor.execute(str1)
    s = str(cursor.fetchone()[0])
    print("s=" + s)
    return  ( s != '0')


def new_country(request):  # 新增資料，資料必須驗證
    if request.method == "POST":  # 如果是以POST方式才處理
        print('new_country POST')
        postform_country = PostForm_country(request.POST)  # 建立forms物件
        if postform_country.is_valid():  # 通過forms驗證
            country_code = postform_country.cleaned_data['country_code']
            country_name = postform_country.cleaned_data['country_name']
            if CountryDuplicate(country_code, country_name):
                print('ERR: country code or name duplicates')   
                message = '國家重複, 請重新輸入' 
            else:
                continent_attr = postform_country.cleaned_data['continent_attr']
                head_of_state = postform_country.cleaned_data['head_of_state']
                foreign_minister = postform_country.cleaned_data['foreign_minister']
                liaison = postform_country.cleaned_data['liaison']
                country_population = postform_country.cleaned_data['country_population']
                country_area = postform_country.cleaned_data['country_area']
                contact_number = postform_country.cleaned_data['contact_number']
                has_diplomatic_relatioin = postform_country.cleaned_data['has_diplomatic_relatioin']
                ambassador_name = postform_country.cleaned_data['ambassador_name']
                status = postform_country.cleaned_data['status']
                # 新增一筆記錄
                unit = country.objects.create(country_code=country_code, country_name=country_name,
                        continent_attr=continent_attr, head_of_state=head_of_state,
                        foreign_minister=foreign_minister, liaison=liaison,
                        country_population=country_population, country_area=country_area,
                        contact_number=contact_number, has_diplomatic_relatioin=has_diplomatic_relatioin,
                        ambassador_name = ambassador_name, status=status)                        
                return redirect('/index/')
        else:
            message = '驗證碼錯誤！'
    else:
        print('post_country else')
        message = '綠色欄位必須輸入！'
        postform_country = PostForm_country()
    return render(request, "new_country.html", locals())


def DependentDuplicate(id):
    print('\ncheck if Dependent duplicate')
    cursor = connection.cursor()
    str1 = "SELECT COUNT(*) FROM f1app_dependent WHERE dep_id='" + id + "'"
    print(str1)
    cursor.execute(str1)
    s = str(cursor.fetchone()[0])
    print("s=" + s)
    return  ( s != '0')


def new_dependent(request):  # 新增資料，資料必須驗證
    print('post_dependent')
    if request.method == "POST":  # 如果是以POST方式才處理
        print('new_dependent POST')
        postform_dependent = PostForm_dependent(request.POST)  # 建立forms物件
        if postform_dependent.is_valid():  # 通過forms驗證

            dep_id = postform_dependent.cleaned_data['dep_id']
            dep_name = postform_dependent.cleaned_data['dep_name']
            if DependentDuplicate(dep_id):
                print('ERR: dependent ID duplicates')   
                message = '眷屬重複, 請重新輸入' 
            else:
                dep_sex = postform_dependent.cleaned_data['dep_sex']
                birthdate = postform_dependent.cleaned_data['birthdate']

                unit = dependent.objects.create(dep_id=dep_id, dep_name=dep_name, dep_sex=dep_sex, birthdate=birthdate)
                message = '已儲存...'
                return redirect('/index/')
        else:
            message = '驗證碼錯誤！'
    else:
        print('post_dependent else')
        message = '綠色欄位必須輸入！'
        elist = employeeList()
        postform_dependent = PostForm_dependent()
    return render(request, "new_dependent.html", locals())


def new_agent(request):  # 新增資料，資料必須驗證
    print('post_agent')
    elist = employeeList()
    clist = countryList()    
    if request.method == "POST":  # 如果是以POST方式才處理
        print('new_agent POST')
        postform_agent = PostForm_agent(request.POST)  # 建立forms物件
        if postform_agent.is_valid():  # 通過forms驗證
            print('Postform agent')
            eid = postform_agent.cleaned_data['emp_id']
            code = request.POST['country_code']    # foreign key
            arrival_date = postform_agent.cleaned_data['arrival_date']
            status = postform_agent.cleaned_data['status']

            id = FindMaxAgentID() + 1
            print(' agent id = ' + str(id))

            try:
                unit = agent.objects.create(id=id, emp_id=eid, country_code=code,
                                            arrival_date=arrival_date, status=status)
            except:
                message = '資料重複 請重新輸入...'
                postform_agent = PostForm_agent()
                return render(request, "new_agent.html", locals())                

            message = '已儲存...'
            return redirect('/index/')
        else:
            message = '驗證碼錯誤！'
    else:
        print('post_agent else')
        message = '綠色欄位必須輸入！'
        postform_agent = PostForm_agent()
    return render(request, "new_agent.html", locals())


def new_dependemp(request):  # 新增資料，資料必須驗證
    print('post_dependemp')
    elist = employeeList()
    dlist = dependentList()

    if request.method == "POST":  # 如果是以POST方式才處理
        print('new_dependemp POST')
        postform_dependemp = PostForm_dependemp(request.POST)  # 建立forms物件
        if postform_dependemp.is_valid():  # 通過forms驗證
            print('e')
            eid = postform_dependemp.cleaned_data['emp_id']
            did = postform_dependemp.cleaned_data['dep_id']
            relation = postform_dependemp.cleaned_data['relation']
            status = postform_dependemp.cleaned_data['status']
            id = FindMaxDependempID()+1

            try:
                unit = dependemp.objects.create(id=id, emp_id=eid, dep_id=did,
                        relation=relation, status=status)
            except:
                message = '資料重複 請重新輸入...'
                postform_dependemp = PostForm_dependemp()
                return render(request, "new_dependemp.html", locals())

            message = '已儲存...'
            return redirect('/index/')
        else:
            message = '驗證碼錯誤！'
    else:
        print('post_dependent else')
        message = '綠色欄位必須輸入！'
        postform_dependemp = PostForm_dependemp()
    return render(request, "new_dependemp.html", locals())


def print_employee(request, emp_id=None):
    unit = employee.objects.get(emp_id=emp_id)  # 取得要修改的資料記
    return render(request, "print_employee.html", locals())


def print_country(request, code=None):
    unit = country.objects.get(country_code=code)  # 取得要修改的資料記
    return render(request, "print_country.html", locals())

def print_agent(request, id=None):
    unit = agent.objects.get(id=id)  # 取得要修改的資料記
    return render(request, "print_agent.html", locals())

def print_dependent(request, id=None):
    unit = dependent.objects.get(dep_id=id)  # 取得要修改的資料記
    return render(request, "print_dependent.html", locals())


def print_dependemp(request, id=None):
    unit = dependemp.objects.get(id=id)  # 取得要修改的資料記
    return render(request, "print_dependemp.html", locals())


def status_employee(request, id=None, mode=None):
    print('status employee')
    if id != None:
        if request.method == "POST":  # 如果是以POST方式才處理
            id = request.POST['emp_id']  # 取得表單輸入的編號

        try:
            unit = employee.objects.get(emp_id=id)
            if mode == "normal":
                unit.status = '正常'                
            else:
                unit.status = '刪除'
                
            unit.save()
            # unit.delete()
        except:
            message = "讀取錯誤!"
    return redirect('/index/')


def status_country(request, code=None,mode=None):
    print('delete country')
    if code != None:
        if request.method == "POST":  # 如果是以POST方式才處理
            code = request.POST['country_code']  # 取得表單輸入的編號
        try:
            unit = country.objects.get(country_code=code)
            if mode == "normal":
                unit.status = '正常'                
            else:
                unit.status = '亡國'

            unit.save()
            # unit.delete()
        except:
            message = "讀取錯誤!"
    return redirect('/index/')


def delete_agent(request, id=None):  # 刪除資料
    print('delete agent')
    if id != None:
        if request.method == "POST":  # 如果是以POST方式才處理
            id = request.POST['emp_id']  # 取得表單輸入的編號
        try:
            unit = agent.objects.get(id=id)
            unit.status = '離職'
            unit.save()
            # unit.delete()
        except:
            message = "讀取錯誤!"
    return redirect('/index/')


def delete_dependent(request, id=None):  # 刪除資料
    print('delete dependent')
    if id != None:
        if request.method == "POST":  # 如果是以POST方式才處理
            id = request.POST['dep_id']  # 取得表單輸入的編號
        try:
            unit = dependent.objects.get(id=id)
            unit.status = '離婚'
            unit.save()
            # unit.delete()
        except:
            message = "讀取錯誤!"
    return redirect('/index/')


def edit_employee(request, emp_id=None, mode=None):
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        print('mode load ' + emp_id + "\n")
        unit = employee.objects.get(emp_id=emp_id)  # 取得要修改的資料記

        imgs = ["bob", "conan", "elsa", "fiona", "kawhi", "mario", "maruko", "woody", "yoda"]

        return render(request, "edit_employee.html", locals())
    elif mode == "save":  # 由 edit_employee.html 按 submit
        print('mode save')
        try:
            unit = employee.objects.get(emp_id=emp_id)  # 取得要修改的資料記錄
        except:
            print('\nERR in employee.objects.get\n')
            return redirect('/index/')

        unit.emp_name = request.POST['emp_name']
        unit.emp_id = request.POST['emp_id']
        unit.rank = request.POST['rank']
        unit.salary = request.POST['salary']
        unit.phone_number = request.POST['phone_number']
        unit.sex = request.POST['sex']
        unit.birthdate = request.POST['birthdate']
        unit.recruit_date = request.POST['recruit_date']
        unit.address = request.POST['address']
        unit.photo = request.POST['photo']
        unit.status = request.POST['status']

        unit.save()  # 寫入資料庫
        message = '已修改...'
        return redirect('/index/')


def edit_country(request, country_code=None, mode=None):
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        print('mode load ' + country_code + "\n")
        message = '修改中...'
        try:        
            unit = country.objects.get(country_code=country_code)  # 取得要修改的資料記
        except:
            print('\nERR in country.objects.get\n')
            return redirect('/index/')
        return render(request, "edit_country.html", locals())
    elif mode == "save":  # 由 edit2.html 按 submit
        print('mode save')

        unit = country.objects.get(country_code=country_code)  # 取得要修改的資料記錄
        unit.country_code = request.POST['country_code']
        unit.country_name = request.POST['country_name']
        unit.continent_attr = request.POST['continent_attr']
        unit.head_of_state = request.POST['head_of_state']
        unit.foreign_minister = request.POST['foreign_minister']
        unit.liaison = request.POST['liaison']
        unit.country_population = request.POST['country_population']
        unit.country_area = request.POST['country_area']
        unit.contact_number = request.POST['contact_number']
        unit.has_diplomatic_relatioin = request.POST['has_diplomatic_relatioin']
        unit.ambassador_name = request.POST['ambassador_name']
        unit.status = request.POST['status']
        
        unit.save()  # 寫入資料庫
#        message = '結束修改...'
        return redirect('/index/')


def edit_dependent(request, id=None, mode=None):
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        print('dependent load ')
        try:
            unit = dependent.objects.get(dep_id=id)
        except:
            print('\nERR in dependent.objects.get\n')
            return redirect('/index/')
        return render(request, "edit_dependent.html", locals())
    elif mode == "save":  # 由 edit_dependent.html 按 submit
        print('dependent save')
        unit = dependent.objects.get(dep_id=id)  # 取得要修改的資料記錄

        unit.dep_id = request.POST['dep_id']
        unit.dep_name = request.POST['dep_name']
        unit.dep_sex = request.POST['dep_sex']
        unit.birthdate = request.POST['birthdate']

        unit.save()  # 寫入資料庫
        message = '已修改...'
        return redirect('/index/')


def edit_agent(request, id, mode=None):
    elist = employeeList()
    clist = countryList()        
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        print('\nagent load')
        message = '修改中...'
        try:
            unit = agent.objects.get(id=id)
        except:
            print('\nERR in agent.objects.get\n')
            return redirect('/index/')
        return render(request, "edit_agent.html", locals())

    elif mode == "save":  # 由 edit_agent.html 按 submit
        print('agent save')
        unit = agent.objects.get(id=id)  # 取得要修改的資料記錄
        unit.id = id
        unit.emp_id = request.POST['emp_id']
        unit.country_code = request.POST['country_code']
        unit.arrival_date = request.POST['arrival_date']
        unit.status = request.POST['status']

        unit.save()  # 寫入資料庫
        return redirect('/index/')


def edit_dependemp(request, id=None, mode=None):
    elist = employeeList()
    dlist = dependentList() 
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        print('dependemp load ')
        message = '修改中...'        
        try:
            unit = dependemp.objects.get(id=id)
        except:
            print('\nERR in dependemp.objects.get\n')
            return redirect('/index/')
        return render(request, "edit_dependemp.html", locals())
    elif mode == "save":  # 由 edit_dependent.html 按 submit
        print('dependent save')
        unit = dependemp.objects.get(id=id)  # 取得要修改的資料記錄
        unit.id = id
        unit.emp_id = request.POST['emp_id']
        unit.dep_id = request.POST['dep_id'] 
        unit.relation = request.POST['relation']
        unit.status = request.POST['status']

        unit.save()  # 寫入資料庫
        return redirect('/index/')