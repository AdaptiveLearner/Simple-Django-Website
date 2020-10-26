from django import forms

class PostForm_employee(forms.Form):
    emp_name = forms.CharField(max_length=14, initial='Nobody', required=True)
    emp_id = forms.CharField(max_length=10, initial='', required=True)
    rank = forms.IntegerField(initial=0, required=True)
    salary = forms.IntegerField(initial=0, required=True)
    phone_number = forms.CharField(max_length=14, initial='', required=False)
    sex = forms.CharField(max_length=1, initial='', required=False)
    birthdate = forms.CharField(max_length=10, required=True)
    recruit_date = forms.CharField(max_length=10, required=False)
    address = forms.CharField(max_length=30, initial='', required=False)
    photo = forms.CharField(initial='', required=False)
    status = forms.CharField(max_length=2, initial='正常', required=False)

class PostForm_country(forms.Form):
    country_code = forms.CharField(max_length=6, initial='', required=True)
    country_name = forms.CharField(max_length=14, initial='', required=True)
    continent_attr = forms.CharField(max_length=14, initial='', required=False)
    head_of_state = forms.CharField(max_length=14, initial='', required=False)
    foreign_minister = forms.CharField(max_length=14, initial='', required=False)
    liaison = forms.CharField(max_length=14, initial='', required=False)
    country_population = forms.IntegerField(initial=1, required=True)
    country_area = forms.IntegerField(initial=1, required=True)
    contact_number = forms.CharField(max_length=14, initial='', required=False)
    has_diplomatic_relatioin = forms.CharField(max_length=6, initial='', required=False)
    ambassador_name = forms.CharField(max_length=14, initial='', required=False)
    status = forms.CharField(max_length=2, initial='正常', required=False)

class PostForm_dependent(forms.Form):
    dep_id = forms.CharField(max_length=10, initial='', required=True)
    dep_name = forms.CharField(max_length=14, initial='', required=False)
    dep_sex = forms.CharField(max_length=1, initial='', required=False)
    birthdate = forms.CharField(max_length=10, initial='1900/01/01', required=False)

class PostForm_agent(forms.Form):
    emp_id = forms.CharField(max_length=10, initial='', required=True)
    country_code = forms.CharField(max_length=6, initial='', required=True)
    arrival_date = forms.CharField(max_length=10, initial='1900/01/01', required=False)
    status = forms.CharField(max_length=2, initial='正常', required=False)

class PostForm_dependemp(forms.Form):
    emp_id = forms.CharField(max_length=10, initial='', required=True)
    dep_id = forms.CharField(max_length=10, initial='', required=True)
    relation = forms.CharField(max_length=10, initial='', required=False)
    status = forms.CharField(max_length=2, initial='正常', required=False)
