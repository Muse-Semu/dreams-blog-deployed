from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Comment, Reply
from .forms import ProfileUpdateForm, UserUpdate, UserRegistrationForm, CommentForm
from django.db.models import Min,Max
from django.views.generic import DetailView ,ListView,UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# GET STARTED VIEWS FOR BLOG

# HOMEPAGE


def getOneRandomPostByCategory(cat):
    post = None
    posts = Post.objects.filter(catagory=cat)
    count = posts.count()
    if count != 0:
        post = posts.order_by('?')[0]
    elif count > 0:
        post = posts.order_by('?')[0:1]
    return post


def homePage(request):
    mostLiked = None
    posts = Post.objects.all()
    count = posts.count()


    if count > 6:
        mostLiked = Post.objects.filter().annotate(
            max_liked=Max('liked')
        ).order_by('-max_liked','-created')[0:6]
    if count != 0:
        if count <= 9:
            post = posts[0:count]
        elif count > 9:
            post = posts[0:9]
    
    else:
        return render(request, 'blog/homepage.html')

    # SELECT ONE RANDOM POST FROM EACH CATEGORY
    sport = getOneRandomPostByCategory('sports')
    technology = getOneRandomPostByCategory('technology')
    entertainment = getOneRandomPostByCategory('entertainment')
    other = getOneRandomPostByCategory('other')
    fashion = getOneRandomPostByCategory('fashion')
    science = getOneRandomPostByCategory('science')

    # THIS IS SEARCH VIEW
    search = request.GET.get('search-area') or ''
    if search:
        post = posts.filter(title__icontains=search)
        result = posts.filter(title__icontains=search).count()
        mostLiked =None

        sech = search
        context = {'post': post,
                   'result': result,
                   'mostLiked': mostLiked,
                   'search': sech}
        return render(request, 'blog/homepage.html', context)
    context = {
        'post': post,
        'mostLiked': mostLiked,
        'sport': sport,
        'technology': technology,
        'entertainment': entertainment,
        'science': science,
        'other': other,
        'fashion': fashion

    }
    return render(request, 'blog/homepage.html', context)

# VIEW POSTS BY CATEGOTIES


def PostCatagory(request, cats):
    mostLiked = None
    yourpost=None
    if (cats == 'all'):
        post = Post.objects.all()
        count = Post.objects.all().count()
        if count > 6:
            mostLiked = Post.objects.filter().annotate(
                max_liked=Max('liked')
            ).order_by('-max_liked', '-created')[0:6]
    elif (cats == 'video'):
        post = Post.objects.filter(is_video=True)
        count = post.count()
        if count > 6:
            mostLiked = Post.objects.filter().annotate(
                max_liked=Max('liked')
            ).order_by('-max_liked', '-created')[0:6]

    elif (cats == 'your-posts'):
        try:
            post = Post.objects.filter(user=request.user)
            count = post.count()
            mostLiked=None

        except:
            return redirect('login')

    else:
        post = Post.objects.filter(catagory=cats)
        count = Post.objects.filter(catagory=cats).count()
        if count > 6:
            mostLiked = Post.objects.filter().annotate(
            max_liked=Max('liked')
        ).order_by('-max_liked','-created')[0:6]

    search = request.GET.get('search-area') or ''
    if search:
        post = post.filter(title__icontains=search)
        count = post.count()
        sech = search
       
        mostLiked = None

        return render(request, 'blog/post-category.html', {'cats': cats, 'post': post, 'yourpost': yourpost, 'count': count,
                                                           'count': count, 'search': sech, 'mostLiked': mostLiked})
    return render(request, 'blog/post-category.html', {'cats': cats, 'post': post, 'count': count, 'mostLiked': mostLiked})


########################### AUTHENTICATION OF USER SECTION ########################################

# LOGIN VIEW
class LoginUser(LoginView):
    template_name = "blog/signin.html"
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('home')

# REGISTRATION


class UserRegister(UserRegistrationForm, FormView):
    template_name = "blog/signup.html"
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    fields = ['username', 'email', 'password1', 'password2']

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)

    def get(self, *args, **kwargs):
        return super(UserRegister, self).get(*args, *kwargs)

    def get_success_url(self):

        return reverse_lazy('registered-succsess')


# ######################## POST RELATED VIEWS #############################

# POST CREATE
class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_form.html'
    model = Post
    fields = ['title', 'discription', 'catagory',
              'articles',  'image', 'videos', 'is_video']
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super(PostCreate, self).form_valid(form)

# POST DETAIL VIEW


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


# POST UPDATE/EDIT VIEW
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'discription', 'articles',
              'image', 'catagory', 'videos', 'is_video')
    success_url = reverse_lazy('home')


# DELETE POST
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')


# ########################### PROFILE OF USER VIEWS ####################

# EDIT PROFILE FIELDS
class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'blog/profile-update.html'
    fields = ('username', 'email', 'first_name', 'last_name',
              'photo', 'bios', 'youtube_url', 'twitter_url', 'telegram_url')
    success_url = reverse_lazy('profile')

# VIEW ANOTHER USER'S PROFILE


class ViewProfile(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'blog/get-profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['id'] = Profile.pk
        return context

# VIEW FOR YOURSELF PROFILE


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
        else:
            u_form = UserUpdate(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdate(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    pro = Profile.objects.filter(user=request.user)
    return render(request, 'blog/profile.html', context)


# ########################### COMMENT AND REPLY VIEWS ###########################

# ADD COMMENT
class AddPostComment(LoginRequiredMixin, CreateView):
    model = Comment
    context_object_name = 'comment'
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']

        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for comment
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        commentid = self.kwargs['pk']
        return reverse_lazy('view-comment', kwargs={'pk': commentid})

# VIEW LIST COMMENTS


class PostComment(ListView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'blog/post_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = context['comment'].filter(
            post_id=self.kwargs['pk'])

        context['id'] = self.kwargs['pk']
        return context

# DELETE COMMENTS


class DeleteComment(LoginRequiredMixin, DeleteView):

    model = Comment
    template_name = 'blog/delete_post.html'
    context_object_name = 'comment'

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if you are passing 'pk' from 'urls' to 'DeleteView' for comment
        # capture that 'pk' as commentid and pass it to 'reverse_lazy()' function
        commentid = self.kwargs['pk']
        return reverse_lazy('view-comment', kwargs={'pk': commentid})


# EDIT COMMENT
class EditComment(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['comment']
    context_object_name = 'comment'

    def get_success_url(self):
        commentid = self.kwargs['pk']
        return reverse_lazy('view-comment', kwargs={'pk': commentid-1})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.request
        context['id'] = self.kwargs['pk']
        return context

# REPLY

# REPLY FOR COMMENT


class ReplyForComment(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'blog/add-reply.html'
    fields = ['reply']
    context_object_name = 'reply'

    def form_valid(self, form):
        form.instance.comment_id = self.kwargs['pk']
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for comment
        # capture that 'pk' as commentid and pass it to 'reverse_lazy()' function
        replyid = self.kwargs['pk']
        return reverse_lazy('view-reply', kwargs={'pk': replyid})

# VIEW REPLY LISTS


class ReplyLists(ListView):
    model = Reply
    context_object_name = 'reply'
    template_name = 'blog/reply_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rp'] = context['reply'].filter(comment_id=self.kwargs['pk'])
        context['id'] = self.kwargs['pk']
        return context


def search(request):
    return render(request, 'blog/homepage.html')


def about(request):
    return render(request, 'blog/about.html')


class ChangePassword(PasswordChangeView):
    template_name = 'blog/change-password.html'
    form_class = PasswordChangeForm

    def get_success_url(self):
        return reverse_lazy('password-changed')

# SUCCEFULL VIEW FOR REGISTER


def successful_registered(request):
    message = "You have registered successfully !"
    return render(request, 'blog/success.html', {'message': message})

# SUCCEFULL VIEW FOR CHANGE PASSWORD


def successful_change_password(request):
    message = "You password is changed successfully !"
    return render(request, 'blog/success.html', {'message': message})


# Like views for post
# @login_required
# def LikeView(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     user = request.user
#     if user in post.liked.all():
#         post.liked.remove(user)
#     else:
#         post.liked.add(user)

#     return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required
def LikeView(request, pk):
    user = request.user
    liked = False
    updated = False
    user_id = user.id
    # print(request.user.is_authenticated)
    if request.user.is_authenticated:
        
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            post_obj = Post.objects.get(id=post_id)
            
            if user in post_obj.liked.all():
                post_obj.liked.remove(user)
                liked = False
            
            else:
                post_obj.liked.add(user)
                liked = True
            updated = True
            
        datas={
            "updated":updated,
            "liked":liked,
            "user_id":user_id,
        }    
        
        
        return JsonResponse(datas,safe=False)
   



# dislike post
# @login_required
# def unlike_post(request):
#     user = request.user
#     if request.method == 'POST':
#         post_id = request.POST.get('unlk')
#         post_obj = Post.objects.get(id=post_id)
#         if user in post_obj.unliked.all():
#             post_obj.unliked.remove(user)
#         else:
#             post_obj.unliked.add(user)
#     return HttpResponse('great')


# ######################### ADMIN PAGE FOR CONTROLLING USER #####################

# VIEWS USEL LLISTS (ALL USER)
class UserView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'user'
    template_name = 'blog/userlist.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            context = super().get_context_data(**kwargs)
            context['ct'] = context['user'].count()
            return context


# ADMIN REGISTER USERS VIEW
class RegisterAdmin(LoginRequiredMixin, CreateView):
    template_name = "blog/signup.html"
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        form.save()
        return super(RegisterAdmin, self).form_valid(form)

    def get(self, *args, **kwargs):
        return super(RegisterAdmin, self).get(*args, *kwargs)

# ADMIN CONTROLLING USERS ACCESSING PERMISSION VIEW


class UpdateUserStatus(UpdateView, FormView):
    model = User
    fields = ['is_superuser', 'is_staff', 'is_active']
    template_name = 'blog/user_status.html'
    # success_url = reverse_lazy('users')

    def form_valid(self, form):
        form.save()
        return super(UpdateUserStatus, self).form_valid(form)

    def get(self, *args, **kwargs):
        return super(UpdateUserStatus, self).get(*args, *kwargs)

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for comment
        # capture that 'pk' as commentid and pass it to 'reverse_lazy()' function
        uid = self.kwargs['pk']
        return reverse_lazy('get-profile', kwargs={'pk': uid})

# ADMIN DELETE USER (It is nor recommended admin can deactivate user instead of delete)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'blog/delete_user.html'
    success_url = reverse_lazy('users')

# AJAX AND JSON VIEW
def getPostAjax(request):
    posts= Post.objects.all()
    lists = list(posts.values())
    return JsonResponse({'posts':lists},safe=False)
def jsonHome(request) :
    posts= Post.objects.all()
    return render(request,'blog/a.html',{'posts':posts})  
