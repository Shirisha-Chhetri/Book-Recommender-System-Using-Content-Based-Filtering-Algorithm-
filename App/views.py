import json
import pandas as pd
from django.db.models import Q

from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .ml import get_recommendation_for_book
from .forms import UploadForm
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .models import Book,Genre,Category,Profile
from django.db import transaction

@login_required(login_url ='login')

# to change user password 
def change_password_profile(request):
    img={}
    if Profile.objects.filter(user=request.user):
        img = Profile.objects.get(user=request.user)
        
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Your password is successfully updated!')     
        else: 
            messages.success(request,'You got error while changing password.Please correct them!')    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'profile.html', {'form': form ,'img':img})


def addprofile(request):
    if request.method == "POST" and request.FILES['profileimage']:
        addProfile = Profile(user=request.user, image=request.FILES['profileimage'])
        addProfile.save()
        return redirect('/profile/')
    
def updateImage(request):
    if request.method == "POST":
        img = Profile.objects.get(user=request.user)
        img.image = request.FILES['updateimg']
        img.save()
        return redirect('/profile/')

def deleteimage(request):
    if Profile.objects.filter(user=request.user):
        img = Profile.objects.get(user=request.user)
        request.user.profile.image.delete()  # delete old image file
        request.user.profile.image = '../media/user.png' # set default image
        request.user.profile.save()
    return redirect('/profile/')

def reset_password(request):
    form = PasswordResetForm()
    return render(request, 'reset_confirm_4.html', {'form': form })

# to show books according to genre
def bookongenre(request):
    genreid = request.GET.get('subcategory')
    b = Genre.objects.get(id = genreid)

    if genreid:
        book = Book.get_book_by_id(genreid).order_by('id')[:28] 
    return render(request, 'booksongenre.html',{
        'books':book,
        'genre':genreid,
        'name':b })


# to add books to wishlist
def add_fav(request,id):
    if request.user.is_authenticated:
        book = Book.objects.get(id = id)
        book.wishlist.add(request.user)
        return redirect('/getbook/{0}'.format(id))          
    else:
        return redirect('/login/')  
   
# to remove books from wishlist
def remove_fav(request,id):
    book = Book.objects.get(id = id)
    book.wishlist.remove(request.user)
    return redirect('/getbook/{0}'.format(id))


# to show added wishlist books on my wishlist href
@login_required(login_url ='login')
def get_user_fav(request):
    favbook =request.user.wishlist.all()
    return render(request,'wishlist.html',{'favbook':favbook})

def about(request):
    return render(request,'about.html')

# home module with genre and sliding image
def allgenre(request):
    category = Category.objects.all().order_by('name')
    slider = Book.objects.all().order_by('id')[:6]
    return render(request, 'home.html',{
        'category':category,
        'sliding':slider})

   
# book module
def allbook(request):
    book = Book.objects.all().order_by('-id')[:72]
    return render(request, 'books.html',{'books':book})


def search(request,id):
    try:
        b = Book.objects.get(id = id)

        # to show genre of that book
        category= b.genre.all().values_list('title',flat=True)
        
        # to show book data
        specificbook = get_object_or_404(Book, pk=id)

        # add and remove wishlist
        context = {
                'is_favourite' :False
            }

        if b.wishlist.filter(pk = request.user.pk).exists():
                context['is_favourite']= True

            # for recommendation
        book_ids = get_recommendation_for_book(b.id)
        recommend_book = Book.objects.none()
        re=[]
        for r in book_ids:
            re.append(r[1])
        
            recommend_book |= Book.objects.filter(title= r[0]).order_by('-id')

        # to trim score that is in float to two decimal
        formatted_list = [ '%.2f' % elem for elem in re ]
            
        return render(request,'specific_book.html',{ 
            'book':specificbook,     
            'bookcategory':category,
            'context':context, 
            'recommended_book':recommend_book,
            'book_ids':formatted_list,
            })
    except Book.DoesNotExist:
        return render(request,'404.html')


# autocomplete search module
def search_auto(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q = request.GET.get('term','')

        # to perform slicing in search bar to ignore num and special characters
        if q.isalpha():
            bookey = Book.objects.filter(Q(title__icontains=q[0:]) | Q(author__icontains=q[0:])).order_by('-id')[0:15]     
            results = []      
        else:
            count=0
            for x in q: 
                if (x.isalpha() == False):
                    count+=1
                    bookey = Book.objects.filter(Q(author__icontains=q[count:]) | Q(title__icontains=q[count:])).order_by('-id')[0:15]
                    results = []
        
        for pl in bookey:
            book_json = {}
            book_json['id'] = pl.id 
            book_json['title'] = pl.title 
            book_json['author'] = pl.author 
            book_json['image'] = pl.image
            results.append(book_json)
       
        data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# login module
def loginuser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request,"Invalid username or password")
            return redirect('/login/')   
    return render(request,'login.html')


@login_required(login_url ='login')
def logouts(request):
    logout(request)
    return redirect('/')

# signup module   
def signup(request):
    error_message = {}

    if request.method == "POST":
        fn = request.POST['first_name']
        ln =  request.POST['last_name']
        un =  request.POST['username']
        email = request.POST['email']
        password =  request.POST['password']

        user = User(first_name = fn,
                        last_name = ln,
                        username = un,
                        email = email,
                        password = password)
          
        if(not fn):
            error_message = "Enter firstname"
        elif (fn.isnumeric()):
            error_message = "Name cannot have number"

        elif (not ln):
            error_message = "Enter lastname"
        elif (ln.isnumeric()):
            error_message = "Name cannot have number"
        
        elif not un:
            error_message = "Enter username"
        elif (un.isnumeric()):
            error_message = "Username cannot be the number"

        elif not email:
            error_message = "Enter Email"
        elif (email.isnumeric()):
            error_message = "Email cannot be the number"

        elif not password:
            error_message = "Enter Password"
        elif len(password) < 5:
            error_message = "Password must be greater than 5 character"

        elif User.objects.filter(email = email).exists():
            error_message = "Email already registered.."

        elif User.objects.filter(username = un).exists():
            error_message = "Username already registered.."

        if not error_message:
            user.password = make_password(user.password)
            user.save()
            return redirect('/login')
        else:
            return render(request,'register.html',{'error':error_message})
    return render(request,'register.html')


# dataset upload form module
def upload(request):
    file_form = UploadForm()
    error_messages = {}

    if request.method == "POST":
        file_form = UploadForm(request.POST, request.FILES)
        try:
            if file_form.is_valid():
            
                dataset = pd.read_csv(request.FILES['uploadfile'])
                new_book_list =[]
                with transaction.atomic():

                    for index, row in dataset.iterrows():
                        book = Book(
                            title = row['title'], 
                            genre = row['genre'],                      
                            description = row['description'],
                            author = row['author'],
                            bookformat = row['bookformat'],
                            isbn = row['isbn'],
                            pages = row['pages'],                           
                            image = row['image']
                        )
                        new_book_list.append(book)
                Book.objects.bulk_create(new_book_list)
                return redirect('/book/page/1')

        except Exception as e:
            print(e)
            error_messages['error'] = e

    return render(request, 'upload_dataset.html',{'form' : file_form,
                                    'error_messages': error_messages})