from django.db import models

class employee(models.Model):
	emp_id = models.CharField(max_length=10, primary_key=True, null=False)
	emp_name = models.CharField(max_length=14, null=False)
	rank = models.IntegerField(null=False)
	salary = models.IntegerField(null=False)
	phone_number = models.CharField(max_length=14)
	sex = models.CharField(max_length=1)
	birthdate = models.CharField(max_length=10, null=False)
	recruit_date = models.CharField(max_length=10)
	address = models.CharField(max_length=30)
	photo = models.CharField(max_length=10)
	status = models.CharField(max_length=2)
	class Meta:
		unique_together = (('emp_name', 'emp_id'),)

class country(models.Model):
	country_code = models.CharField(max_length=6, primary_key=True, null=False)
	country_name = models.CharField(max_length=14, null=False)
	continent_attr = models.CharField(max_length=14, null=False)
	head_of_state = models.CharField(max_length=14)
	foreign_minister = models.CharField(max_length=14)
	liaison = models.CharField(max_length=14)
	country_population = models.IntegerField(null=False)
	country_area = models.IntegerField(null=False)
	contact_number = models.CharField(max_length=14)
	has_diplomatic_relatioin = models.CharField(max_length=6)
	ambassador_name = models.CharField(max_length=14)
	status = models.CharField(max_length=2)
	class Meta:
		unique_together = (('country_code', 'country_name'),)

class dependent(models.Model):
	dep_id = models.CharField(max_length=10, primary_key=True, null=False)
	dep_name = models.CharField(max_length=14)
	dep_sex = models.CharField(max_length=1)
	birthdate = models.CharField(max_length=10)

class agent(models.Model):
	id = models.IntegerField(primary_key=True, null=False)
	emp_id = models.CharField(max_length=10, null=False)
	country_code = models.CharField(max_length=6, null=False)
	arrival_date = models.CharField(max_length=10)
	status = models.CharField(max_length=2)
	class Meta:
		unique_together = (('emp_id', 'country_code'),)

class dependemp(models.Model):
	id = models.IntegerField(primary_key=True, null=False)
	emp_id = models.CharField(max_length=10, null=False)
	dep_id = models.CharField(max_length=10, null=False)
	relation = models.CharField(max_length=10)
	status = models.CharField(max_length=2)
	class Meta:
		unique_together = (('emp_id', 'dep_id'),)		