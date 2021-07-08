from django.db import models
from datetime import datetime, timedelta
from calendar import isleap
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking first name
        if len(postData['first_name']) == 0:
            errors['first_name_emp'] = "First name can not be empty"
        elif len(postData['first_name']) > 0 and len(postData['first_name']) < 2:
            errors['show_title_len'] = "First name should be less at least 2 characters long"
            
        # checking last name
        if len(postData['last_name']) == 0:
            errors['last_name_emp'] = "Last name can not be empty"
        elif len(postData['last_name']) > 0 and len(postData['last_name']) < 2:
            errors['last_name_len'] = "Last name should be less at least 2 characters long"
                
        # checking valid email 
        if len(postData['email']) == 0:
            errors['email_emp'] = "Email address can not be empty"
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):    # testing if field matches pattern        
                errors['email_val'] = "Email address is invalid"
            
        # checking birthday    
        if len(postData['birthday']) == 0:
            errors['birthday_emp'] = "Birthday can not be empty"      
        else:
            # The strptime() method creates a datetime object from the given string.            
            birthday_date = datetime.strptime(postData['birthday'], "%Y-%m-%d")
            today_date = datetime.today()

            yesterday = today_date - timedelta(days=1)
                
            if birthday_date > yesterday:
                errors['birthday_val'] = "Birthday must be less than today's date"     
                
            start_date = birthday_date
            end_date = today_date
            diffyears = end_date.year - start_date.year
            difference  = end_date - start_date.replace(end_date.year)
            days_in_year = isleap(end_date.year) and 366 or 365
            difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year              
            
            # If user is less than 13 years old
            if difference_in_years < 13:
                errors['birthday_old'] = "Age should be at least 13 years old"   
        
        # checking password    
        if len(postData['password']) == 0:
            errors['password_emp'] = "Password can not be empty"
        elif len(postData['password']) < 8:
            errors['password_len'] = "Password should be less at least 8 characters long"                
        
        # checking password 2   
        if len(postData['password2']) == 0:
            errors['password2_emp'] = "Password confirmation can not be empty"
        elif len(postData['password2']) < 8:
            errors['password2_len'] = "Password confirmation should be less at least 8 characters long"    
            
        # checking password 1 and 2
        if len(postData['password']) > 7 and len(postData['password2']) > 7:
            if postData['password'] != postData['password2']:    
                errors['password_dif'] = "Passwords do not match, please try again"

        return errors
    
    def basic_validator2(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking valid email 
        if len(postData['email_login']) == 0:
            errors['email_login_emp'] = "Email address can not be empty"
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email_login']):    # testing if field matches pattern        
                errors['email_login_val'] = "Email address is invalid"
                
        # checking password    
        if len(postData['password_login']) == 0:
            errors['password_login_emp'] = "Password can not be empty"
        elif len(postData['password_login']) < 8:
            errors['password_login_len'] = "Password should be less at least 8 characters long"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)    
    birthday = models.DateField(default=datetime.now)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User: (ID: {self.id}) -> {self.first_name} {self.last_name} by {self.email}"
    
class MessageManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking first name
        if len(postData['message']) == 0:
            errors['message'] = "Message can not be empty"
            
        return errors
                
    
class Message(models.Model):
    message = models.TextField(default="None")
    user_id = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

    def __repr__(self):
        return f"Message: (ID: {self.id}) -> {self.user_id} {self.message}"
    
class CommentManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking first name
        if len(postData['comment']) == 0:
            errors['comment'] = "Comment can not be empty"
            
        return errors
    
class Comment(models.Model):
    message_id = models.ForeignKey(Message, related_name="messages", on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __repr__(self):
        return f"Comment: (ID: {self.id}) -> {self.comment}"    