from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm,CustomUserForm
from django.contrib.auth.models import User
from google.cloud import vision
from google.cloud.vision import types
from django.conf import settings
from django.contrib.auth.decorators import login_required
import io
import os


# GOOGLE SERVICE ACCOUNT KEY'DEN ALINAN .JSON UN PATH İ BURAYA VERİLMELİ
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'vision/post_list.html',{'posts': posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    needed_file_name = 'C:\\Proje\\media\\'
    needed_file_name += str(post)[7:]
    print(needed_file_name)
    
    with io.open(needed_file_name, 'rb') as image_file:
        content = image_file.read()
    client = vision.ImageAnnotatorClient()
    
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    objects = client.object_localization(image=image).localized_object_annotations
    
    print('labels:')
    for label in labels:
        print(label.description)
    
    return render(request, 'vision/post_detail.html', {'post': post, 'labels': labels, 'objects': objects})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print("FORM Girdi")
            form.author = request.user.id
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'vision/post_edit.html', {'form': form})
   
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
    
    
def register(request):
    if request.method == 'POST':
        print('POST a girdi')
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        print(username)
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save();
        print('user kayıt')
        return redirect('/')
    else:
        form = CustomUserForm()
        return render(request, 'vision/register.html')