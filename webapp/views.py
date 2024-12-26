import pickle
import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.urls import reverse
from .models import CreditScorePrediction, Feedback, APILog
from django.contrib.auth.decorators import login_required

# Load the model once at the start
with open('webapp/credit_score_model_1.pkl', 'rb') as model_file:
    credit_score_model = pickle.load(model_file)

# Home View
def home(request):
    return render(request, 'home.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')  # Manually get and save the email
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Credit Score Form View
def credit_form(request):
    if request.method == 'POST':
        # Collect data from the form
        name = request.POST.get('name')
        age = int(request.POST.get('age'))
        annual_income = float(request.POST.get('annual_income'))
        monthly_salary = float(request.POST.get('monthly_salary'))
        num_bank_accounts = int(request.POST.get('num_bank_accounts'))
        num_credit_cards = int(request.POST.get('num_credit_cards'))
        num_credit_inquiries = int(request.POST.get('num_credit_inquiries'))
        credit_history_age = int(request.POST.get('credit_history_age'))

        # Prepare data for prediction (this matches the order of training data)
        input_data = [[
            age, annual_income, monthly_salary, num_bank_accounts, 
            num_credit_cards, num_credit_inquiries, credit_history_age
        ]]

        # Generate prediction
        predicted_score = int(credit_score_model.predict(input_data)[0])

        

        # Save the data to the database
        CreditScorePrediction.objects.create(
            user=request.user,  # Save the logged-in user
            name=name,
            age=age,
            annual_income=annual_income,
            monthly_inhand_salary=monthly_salary,
            num_bank_accounts=num_bank_accounts,
            num_credit_card=num_credit_cards,
            # interest_rate=Interest_Rate,
            num_credit_inquiries=num_credit_inquiries,
            credit_history_age=credit_history_age,
            # total_emi_per_month=Total_EMI_per_month,
            # amount_invested_monthly=Amount_invested_monthly,
            predicted_credit_score=predicted_score
        )

        # Redirect to the dashboard to display the predicted score
        return redirect(reverse('dashboard') + f"?score={predicted_score}")

        # Redirect to dashboard with the predicted credit score
        # return redirect(reverse('dashboard') + f"?score={predicted_score}")

    return render(request, 'credit_form.html')

# Dashboard View to Display Credit Score
# def user_dashboard(request, credit_score):
#     return render(request, 'dashboard.html', {'credit_score': credit_score})

# def dashboard(request, credit_score):
#     predictions = CreditScorePrediction.objects.filter(user=request.user)
#     return render(request, 'dashboard.html', {'credit_score': credit_score, 'predictions': predictions})

# Dashboard View
@login_required(login_url='login')
def dashboard(request):
    # Retrieve the credit score from the URL query parameters
    credit_score = request.GET.get('score', None)

    # Fetch past predictions for the user
    if request.user.is_authenticated:
        predictions = CreditScorePrediction.objects.filter(user=request.user).order_by('-id')
        credit_scores = [prediction.predicted_credit_score for prediction in predictions]
        dates = [prediction.date_submitted.strftime('%Y-%m-%d') for prediction in predictions]
    else:
        credit_scores, dates = [], []
    

    
    context = {
        'credit_score': credit_score,
        'credit_scores': credit_scores,
        'dates': json.dumps(dates),
        'predictions': predictions,
        'first_prediction': predictions.first() if predictions.exists() else None,
    }

    # Get all predictions made by the logged-in user
    predictions = CreditScorePrediction.objects.filter(user=request.user)

    return render(request, 'dashboard.html', context)

def about_us(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def help(request):
    return render(request, 'help.html')

def tc(request):
    return render(request, 'tc.html')

def tariff(request):
    return render(request, 'tariff.html')

# def user_dashboard(request):
#     return render(request, 'dashboard.html')

def user_home(request):
    return render(request, 'user_home.html')

def thank_you(request):
    return render(request, 'thank_you.html')

# View to handle the feedback form submission
def feedback_form(request):
    if request.method == 'POST':
        # Get form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the feedback in the database
        feedback = Feedback.objects.create(
            name=name,
            email=email,
            message=message,
            user=request.user if request.user.is_authenticated else None  # Store the user if logged in
        )

        # Redirect to a thank you page or show a success message
        return redirect('thank_you')  # Replace with the appropriate view name

    return render(request, 'contactus.html')

def fetch_financial_news(request):
    api_key = settings.NEWS_API_KEY
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&category=business&language=en"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        news_data = response.json().get("results", [])

        # Log successful API request
        APILog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            endpoint="Financial News API",
            status_code=response.status_code,
            response_message="Success"
        )

    except requests.exceptions.RequestException as e:
        # Log failed API request
        APILog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            endpoint="Financial News API",
            status_code=response.status_code if response else 500,
            response_message=str(e)
        )
        news_data = []

        print(f"Error fetching news data: {e}")
    
    return render(request, 'financial_news.html', {'news_data': news_data})


def calculate_loan_amount(credit_score):
    """Calculates the eligible loan amount based on the credit score."""
    if credit_score >= 750:
        return 1000000  # Maximum loan amount for excellent credit
    elif 700 <= credit_score < 750:
        return 500000  # Moderate loan amount for good credit
    elif 650 <= credit_score < 700:
        return 200000  # Lower loan amount for fair credit
    else:
        return 50000  # Minimal or limited loan amount for poor credit

@login_required
def loan_information(request):
    user = request.user
    prediction = CreditScorePrediction.objects.filter(user=user).last()  # Adjust as needed

    if prediction:
        user_credit_score = prediction.predicted_credit_score
        eligible_loan_amount = calculate_loan_amount(user_credit_score)
    else:
        user_credit_score = 'N/A'
        eligible_loan_amount = 0

    context = {
        'user_credit_score': user_credit_score,
        'eligible_loan_amount': eligible_loan_amount,
    }
    return render(request, 'loan_information.html', context)


