from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

#def index(request):
 #   return HttpResponse("Page d'accueil: Application Blog")
#def ListBlogs(request):
 #   return HttpResponse('page liste des blogs:Application Blog')
#def ajout(request):
 #   return HttpResponse('page ajout des blogs:Application Blog')


def frontpage(request):
    posts = Post.objects.all()
    
    return render(request, 'blog/frontpage.html', {'posts': posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)

    return render(request, 'blog/post_detail.html', {'post': post})

def post_detail(request, slug):
    post = Post.objects.all()

    if request.method == 'POST':
    	form = CommentForm(request.POST)

    	if form.is_valid():
    		comment = form.save(commit=False)
    		comment.post = post
    		comment.save()

    		return redirect('post_detail', slug=post.slug)
    else:
    	form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})