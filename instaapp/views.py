from django.template import loader
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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




def PostDetails(request, post_id):
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
                    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
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
                
                
                
                
                