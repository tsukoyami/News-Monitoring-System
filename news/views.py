# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from .models import Subscriber, registeredUsers, Story, Source, Company
from .forms import LoginForm, StoryForm, SourceForm
from .decorator import login_required 


def signup(request):
    print("Entering signup view...")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User signed up successfully.")
            request.session['logged_in_user'] = user.id
            print("Session data set:", request.session)
            for company in form.cleaned_data.get('company', []): 
                Subscriber.objects.create(user=user, company=company)
            print("Redirecting to add_source...")
            return redirect('add_source')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        
            try:
                user = registeredUsers.objects.get(username=username, password=password)
          
                if user:
            
                    request.session['logged_in_user'] = user.id
                  
                    if Source.objects.filter(user=user).exists():
                      
                        return redirect('user_stories')
                    else:
                       
                        return redirect('add_source')
            except registeredUsers.DoesNotExist:
            
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
  
    return redirect('login') 

@login_required
def user_stories(request):

    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:

        user_stories = Story.objects.filter(created_by_id=logged_in_user_id).order_by('-published_date')
        return render(request, 'user_stories.html', {'user_stories': user_stories})
    else:
      
        return render(request, 'login.html', {'error_message': 'You need to login to view your stories.'})

@login_required
def add_story(request):

    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:
        if request.method == 'POST':
            form = StoryForm(request.POST)
            if form.is_valid():
             
                story = form.save(commit=False)
                story.created_by_id = logged_in_user_id
                story.save()
                form.save_m2m() 
                return redirect('user_stories')
        else:
            form = StoryForm()
        return render(request, 'add_story.html', {'form': form})
    else:
  
        return render(request, 'login.html', {'error_message': 'You need to login to add a story.'})

@login_required
def edit_story(request, pk):

    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:
        story = get_object_or_404(Story, pk=pk)
        if story.created_by.id == logged_in_user_id:
            if request.method == 'POST':
                form = StoryForm(request.POST, instance=story)
                if form.is_valid():
                    form.save()
                    return redirect('user_stories')
            else:
                form = StoryForm(instance=story)
            return render(request, 'edit_story.html', {'form': form})
        else:
         
            return redirect('user_stories')
    else:
   
        return render(request, 'login.html', {'error_message': 'You need to login to edit a story.'})
@login_required
def delete_story(request, pk):

    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:
        story = get_object_or_404(Story, pk=pk)
        if story.created_by.id == logged_in_user_id:
            if request.method == 'POST':
                story.delete()
                return redirect('user_stories')
            else:
                return render(request, 'delete_story.html', {'story': story})
        else:
            
            return redirect('user_stories')
    else:
     
        return render(request, 'login.html', {'error_message': 'You need to login to delete a story.'})

@login_required
def user_sources(request):
    
    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:

        user_sources = Source.objects.filter(user_id=logged_in_user_id)
        print(user_sources) 
        return render(request, 'user_sources.html', {'user_sources': user_sources})
    else:
 
        return render(request, 'login.html', {'error_message': 'You need to login to view your sources.'})

@login_required
def add_source(request):

    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:
        if request.method == 'POST':
            form = SourceForm(request.POST)
            if form.is_valid():
    
                source = form.save(commit=False)
                source.user_id = logged_in_user_id
                source.save()

    
                subscriber = Subscriber.objects.get(user_id=logged_in_user_id)
          
                source.company.set([subscriber.company])

                form.save_m2m() 
                return redirect('user_sources')
        else:
            form = SourceForm()
        return render(request, 'add_source.html', {'form': form})
    else:

        return render(request, 'login.html', {'error_message': 'You need to login to add a source.'})

@login_required
def edit_source(request, pk):
 
    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:
        source = get_object_or_404(Source, pk=pk)
        if source.user.id == logged_in_user_id:
            if request.method == 'POST':
                form = SourceForm(request.POST, instance=source)
                if form.is_valid():
                    form.save()
                    return redirect('user_sources')
            else:
                form = SourceForm(instance=source)
            return render(request, 'edit_source.html', {'form': form})
        else:
           
            return redirect('user_sources')
    else:
  
        return render(request, 'login.html', {'error_message': 'You need to login to edit a source.'})
@login_required
def delete_source(request, pk):

    logged_in_user_id = request.session.get('logged_in_user')
    
    if logged_in_user_id:
        source = get_object_or_404(Source, pk=pk)
        if source.user.id == logged_in_user_id:
            if request.method == 'POST':
                source.delete()
                return redirect('user_sources')
            else:
                return render(request, 'delete_source.html', {'source': source})
        else:
        
            return redirect('user_sources')
    else:
 
        return render(request, 'login.html', {'error_message': 'You need to login to delete a source.'})
    

from django.core.management import call_command
@login_required
def update_stories(request):
    user_id = request.session.get('logged_in_user')


    call_command('update_stories', user_id)
    return redirect('user_stories')

def search_user_sources(request):
    query = request.GET.get('query')
    user_sources = Source.objects.filter(source_name__icontains=query) | Source.objects.filter(source_url__icontains=query)
    return render(request, 'user_sources.html', {'user_sources': user_sources, 'query': query})

def search_user_stories(request):
    query = request.GET.get('query')
    user_stories = Story.objects.filter(title__icontains=query) | Story.objects.filter(body_text__icontains=query)
    return render(request, 'user_stories.html', {'user_stories': user_stories, 'query': query})
