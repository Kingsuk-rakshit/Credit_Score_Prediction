from django.db import models
from django.contrib.auth.models import User

class CreditScorePrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who filled out the form
    name = models.CharField(max_length=100, default="Unknown")
    age = models.IntegerField()
    annual_income = models.FloatField()
    monthly_inhand_salary = models.FloatField()
    num_bank_accounts = models.IntegerField()
    num_credit_card = models.IntegerField()
    # interest_rate = models.FloatField()
    num_credit_inquiries = models.IntegerField()
    credit_history_age = models.IntegerField()
    # total_emi_per_month = models.FloatField()
    # amount_invested_monthly = models.FloatField()
    predicted_credit_score = models.IntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Credit Score Prediction for {self.user.username}"


# Feedback Model to store feedback data
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"
    

class APILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.CharField(max_length=255)  # e.g., "Financial News API"
    request_time = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()  # HTTP status code of the API response
    response_message = models.TextField(blank=True, null=True)  # Error messages or data summary


    def _str_(self):
        return f"API Log for {self.user} - {self.endpoint} at {self.request_time}"