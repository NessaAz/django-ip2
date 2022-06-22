from django.template import loader
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.urls import resolve

def index(request):	

	template = loader.get_template('instaapp/main.html')

	context = {	}

	return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
        context = {'form':form,}
    return render(request, 'instaapp/signup.html', context)
        
      

def loginuser(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            return redirect('index') # if you want to redirect same page then, return redirect('this function name in urls.py')

    return render(request, 'instaapp/loginuser.html', {'form': form})



@login_required
def newpost(request):
	user = request.user
	tags_objs = []
	files_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('content')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)

			for file in files:
				file_instance = PostFileContent(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			p, created = Post.objects.get_or_create(caption=caption, user=user)
			p.tags.set(tags_objs)
			p.content.set(files_objs)
			p.save()
			return redirect('index')
	else:
		form = NewPostForm()

	context = {
		'form':form,
	}

	return render(request, 'instaapp/newpost.html', context)


def postdetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    profile = Profile.objects.get(user=user)
    favorited = False
    comments = Comment.objects.filter(post=post).order_by('date')
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=user)
        if profile.favorites.filter(id=post_id).exists():
            favorited = True
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.user = user
                    comment.save()
                    return HttpResponseRedirect(reverse('postdetail', args=[post_id]))
                else:
                    form = CommentForm()
                    template = loader.get_template('instaapp/postdetail.html')
                    context = {
                            'post':post,
                            'favorited':favorited,
                            'profile':profile,
                            'form':form,
                            'comments':comments,
	                    }
                    return HttpResponse(template.render(context, request))
                
                
@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('postdetail', args=[post_id]))                


@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    
    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
        post.likes = current_likes
        post.save()
        
        return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    
    
    
@login_required
def follow(request, username, option):
    following = get_object_or_404(User, username=username)
    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)
        
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
                    
                    return HttpResponseRedirect(reverse('profile', args=[username]))
    except:
        User.DoesNotExist
                
    return HttpResponseRedirect(reverse('profile', args=[username]))    



def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
        
    else:
        posts = profile.favorites.all()
        posts_count = Post.objects.filter(user=user).count()
        following_count = Follow.objects.filter(follower=user).count()
        followers_count = Follow.objects.filter(following=user).count()
        follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
        paginator = Paginator(posts, 8)
        page_number = request.GET.get('page')
        posts_paginator = paginator.get_page(page_number)
        
        template = loader.get_template('profile.html')
        context = {'posts': posts_paginator,'profile':profile,'following_count':following_count,
		'followers_count':followers_count,'posts_count':posts_count,'follow_status':follow_status,
		'url_name':url_name,}
        
    return HttpResponse(template.render(context, request))


def UserProfileFavorites(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = profile.favorites.all()
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
        
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)
        
    template = loader.get_template('profile_favorite.html')

    context = {
            'posts': posts_paginator,
            'profile':profile,
            'following_count':following_count,
            'followers_count':followers_count,
            'posts_count':posts_count,
        }

    return HttpResponse(template.render(context, request))


@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('direct/search_user.html')
	
	return HttpResponse(template.render(context, request))