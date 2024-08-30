
import token
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
#from .forms import LoginForm
#import mysql.connector as sql  # type: ignore
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
#from login.models import Profile
from django.contrib import messages
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Create your views here.
import csv


def get_result(name):
    df=pd.read_csv("cosmetics.csv")
    df['tags']= df['Brand'] +','+ df['Label']+','+df['Name']+','+df['Ingredients']
    vectorizer = TfidfVectorizer()

    # fit the vectorizer to the documents and transform them into a matrix
    tfidf_matrix = vectorizer.fit_transform(df['tags'])

    # Compute the sigmoid kernel
    sig = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
        # Get the index corresponding to original_title
    idx = indices[name]

        # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

        # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

        # Movie indices
    indices = [i[0] for i in sig_scores]

        # Top 10 most similar movies
    result = df.iloc[indices].sort_values(by='Rank',ascending=False)
    return list(result.values)

def get_data():
    data = []
    with open('E:\projects\Cosmetics_recommandation_engine\cosmetics.csv', 'r',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def home(request):
    data=get_data()
    return render(request,'home.html',{'data': data})

def products(request):
    data=get_data()
    return render(request, 'products.html',{'data': data[0:10]})

def productdetails(request):
    data=get_data()
    if request.method=='GET':
        name=request.GET['name']
    result=get_result(name)
    return render(request, 'product_details.html', {'data': data,'result':result})

def contact(request):
    return render(request, 'contact.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def cart(request):
    return render(request,'cart.html')

def login_view(request):
    """if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Perform the authentication
            try:
                m = sql.connect(host='localhost', user='root', password='root', database='cosmetic')
                cursor = m.cursor()
                cursor.execute("SELECT id FROM users WHERE Email=%s AND Password=%s", (email, password))
                user = cursor.fetchone()

                if user:
                    user_id = user[0]
                    
                    # Log the login attempt
                    cursor.execute("INSERT INTO login (user_id) VALUES (%s)", (user_id,))
                    m.commit()
                    send_mail_after_registration(email , token)
                    return render(request, 'welcome.html')  # Replace with your welcome page
                else:
                    return request("error.html")

            except sql.Error as e:
                 return HttpResponse(f"Error connecting to the database: {e}")

            finally:
                if m.is_connected():
                    cursor.close()
                    m.close()
    else:
        form = LoginForm()
"""
    return render(request, 'login_page.html')


def signup(request):
    return render(request, 'signup_page.html')


def token_send(request):
    return render(request , 'token_send.html')

def error_page(request):
    return  render(request , 'error.html')

"""def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
"""


"""
def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            m = sql.connect(host='localhost', user='root', password='root', database='cosmetic')
            cursor = m.cursor()
            cursor.execute("SELECT id FROM users WHERE Email=%s", (email,))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                reset_token = get_random_string(32)
                
                # Insert the reset token into the database
                cursor.execute("INSERT INTO password_reset_tokens (user_id, reset_token) VALUES (%s, %s)", (user_id, reset_token))
                m.commit()

                # Send the reset email
                reset_link = f"http://localhost:8000/password_reset_confirm/{reset_token}/"
                send_mail(
                    'Password Reset Request',
                    f'Click the link below to reset your password:\n{reset_link}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'registration/password_reset_done.html')

            else:
                return HttpResponse("Email not found")

        except sql.Error as e:
            return HttpResponse(f"Error connecting to the database: {e}")

        finally:
            if m.is_connected():
                cursor.close()
                m.close()
    else:
        return render(request, 'registration/password_reset.html')

def password_reset_confirm_view(request, reset_token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        
        try:
            m = sql.connect(host='localhost', user='root', password='root', database='cosmetic')
            cursor = m.cursor()
            cursor.execute("SELECT user_id FROM password_reset_tokens WHERE reset_token=%s", (reset_token,))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                
                # Update the user's password
                cursor.execute("UPDATE users SET Password=%s WHERE id=%s", (new_password, user_id))
                m.commit()

                # Optionally delete the used token
                cursor.execute("DELETE FROM password_reset_tokens WHERE reset_token=%s", (reset_token,))
                m.commit()

                return render(request, 'registration/password_reset_complete.html')
            else:
                return HttpResponse("Invalid reset token")

        except sql.Error as e:
            return HttpResponse(f"Error connecting to the database: {e}")

        finally:
            if m.is_connected():
                cursor.close()
                m.close()
    else:
        return render(request, 'registration/password_reset_confirm.html', {'reset_token': reset_token})


"""