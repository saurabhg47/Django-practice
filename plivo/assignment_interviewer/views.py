from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.contrib.auth import logout
from models import Candidate, Rating
from django.db.models import Avg


def dashboard(request, template="login.html"):
    """
    Render the login page
    """
    return render(request, template)


def hr_login(request, template="login.html"):
    """
    Render the hr page
    """
    result = {'context': 'Admin Page'}
    return render(request, template, result)


def register_user_page(request, template="interviewer_registration.html"):
    """
    Render the interviewer registration page
    """
    return render(request, template)


def register_user(request):
    """
    Method to register new interviewer
    """
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
    except IntegrityError:
        result = {'msg': "Username already Registered, Please Choose different username"}
        return render(request, "interviewer_registration.html", result)
    user.save()
    result = {'msg': "You have Successfully Registered"}
    return render(request, "login.html", result)


def login_user(request, template="rate_add_candidate.html"):
    """
    Method to login interviewer
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        Rating.objects
        request.session['user_id'] = user.id
        result = list_candidate(user.id)
        if user.is_superuser:
            result = show_final_rating()
            return render(request, "show_final_rating.html", result)
        return render(request, template, result)
    result = {'msg': "Sorry Invalid Login"}
    return render(request, "login.html", result)


def list_candidate(user_id):
    """
    Method to list all candidates and rating
    """
    result = dict()
    my_rated_candidate = Rating.objects.filter(interviewer_id=user_id)
    my_rated_candidate_id_rating = {candidate.candidate_id: candidate.rating for candidate in my_rated_candidate}
    all_candidate = Candidate.objects.all()
    for candidate in all_candidate:
        if candidate.id in my_rated_candidate_id_rating:
            candidate.rating = my_rated_candidate_id_rating[candidate.id]
        else:
            candidate.rating = ''
        candidate.name = candidate.last_name + ' ' + candidate.first_name
    result['data'] = all_candidate
    return result


def add_candidate(request, template="add_candidate.html"):
    """
    Render the add new candidate page
    """
    return render(request, template)


def add_new_candidate(request, template="rate_add_candidate.html"):
    """
    Method to add new candidates
    """
    try:
        request.session['user_id']
    except KeyError:
        result = {'msg': "User got logged out, Please login"}
        return render(request, "login.html", result)
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    email = request.POST.get('email')
    candidate = Candidate(email=email, first_name=first_name, last_name=last_name)
    try:
        candidate.save()
    except IntegrityError:
        result = {'msg': "This Email Id already Registered"}
        return render(request, "add_candidate.html", result)
    user_id= request.session['user_id']
    result = list_candidate(user_id)
    return render(request, template, result)


def go_to_rate_candidate(request, template="rate_candidate.html"):
    """
    Render the rate candidate page
    """
    request.session['candidate_id'] = request.POST.get('candidate_id')
    return render(request, template)


def logout_user(request):
    """
    Render the logout page
    """
    logout(request)
    result = {'msg': "You have Successfully Logged Out"}
    return render(request, "login.html", result)


def rate_candidate(request):
    """
    Method to Rate or update rating
    """
    try:
        user_id = request.session['user_id']
    except KeyError:
        result = {'msg': "User got logged out, Please login"}
        return render(request, "login.html", result)
    rating = request.POST.get('rating')
    result = dict()
    candidate_id = request.session['candidate_id']
    rate_obj = Rating.objects.filter(interviewer_id=user_id, candidate_id=candidate_id)
    try:
        rating = int(rating)
    except ValueError:
        result['msg'] = "Rating Should be Integer 1-5"
        return render(request, "rate_candidate.html", result)
    if rating == 0 or rating > 5:
        result['msg'] = "Please Rate between 1-5"
        return render(request, "rate_candidate.html", result)
    if rate_obj.exists():
        rate_obj = rate_obj.select_for_update()[0]
        rate_obj.rating = rating
    else:
        rate_obj = Rating(interviewer_id=user_id, candidate_id=candidate_id, rating=rating)
    rate_obj.save()
    result = list_candidate(user_id)
    result['msg'] = "Rating Saved Successfully"
    return render(request, "rate_add_candidate.html", result)


def show_final_rating():
    """
    Method to List candidates final rating
    """
    candidates = Rating.objects.all()
    candidate_ids = [candidate.candidate_id for candidate in candidates]
    all_candidate = []
    candidate_fnl_rating = Rating.objects.values('candidate_id').filter(candidate_id__in=candidate_ids).annotate(final_rating=Avg('rating'))
    for candidate in candidate_fnl_rating:
        candidate_obj = Candidate.objects.filter(pk=candidate['candidate_id'])[0]
        name = candidate_obj.last_name + ' ' + candidate_obj.first_name
        candidate.update({'name': name})
        all_candidate.append(candidate)
    result = {'data': all_candidate}
    return result