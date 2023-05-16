from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from datetime import datetime
from .forms import PdfUploadForm
import PyPDF2
from .api import resume_parse, getResponse, get_keywords
import json
from home.forms import JoinForm, LoginForm
from home.forms import JobEntryForm
from home.models import Job, JobCategory, JobStatus
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from urllib.parse import unquote


@login_required(login_url='/login/')
def read_pdf(request):
    if request.method == "POST":
        prompt = "Write a cover letter based on Resume and job desccription 150 words strictly"
        form = PdfUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["pdf_file"]
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Get the text content of the PDF file
            resume_text = ""
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                resume_text += page.extract_text()
            print("resume_text")
            job_desc = request.POST.get("desc-2")
            print(job_desc)
            print(resume_text)

            input_text = prompt + " Job Description :" + \
                job_desc + "Resume : " + resume_text
            print(input_text)
            job_matching_score = resume_parse(resume_text, job_desc)
            print("score is ", job_matching_score)
            cover_letter_text = getResponse(input_text)
            print("All keywords")
            print(get_keywords(job_desc))
            res_keywords = get_keywords(job_desc)

            return render(
                request,
                "coverLetter.html",
                {"cover_letter": cover_letter_text, "keywords": res_keywords},
            )
            # Do something with the text_content variable, such as save it to a database
    else:
        form = PdfUploadForm()
    return render(request, "read_pdf.html", {"form": form})



def index(request):
    context = {"var": "Prasanna"}

    if request.method == "POST":
        prompt = "Write a cover letter based on Resume and job desccription 50 words strictly"
        val1 = request.POST.get("desc-1")
        val2 = request.POST.get("desc-2")
        input_text = prompt + "job :" + val1 + "Resume : " + val2
        print(val1, val2)
        print(getResponse(input_text))

    return render(request, "index.html", context)


def about(request):
    context = {"var": "Prasanna"}

    if request.method == "POST":
        name = request.POST.get("name")
        # email = request.POST.get("email")
        # phone = request.POST.get("phone")
        # desc = request.POST.get("desc")
        # contact = Contact(
        #     name=name, email=email, phone=phone, desc=desc, date=datetime.today()
        # )
        # contact.save()
        # print("data is save")

    return render(request, "about.html", context)


def contact(request):
    context = {"var": "Prasanna"}
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        contact = Contact(
            name=name, email=email, phone=phone, desc=desc, date=datetime.today()
        )
        contact.save()
        print("data is save")
    return render(request, "contact.html", context)


def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = {"join_form": join_form}
            return render(request, 'core/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = {"join_form": join_form}
        return render(request, 'core/join.html', page_data)


def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                # Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request, user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(
                    username, password))
                return render(request, 'core/login.html', {"login_form": LoginForm})
    else:
        # Nothing has been provided for username or password.
        return render(request, 'core/login.html', {"login_form": LoginForm})


@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")


@login_required(login_url='/login/')
def jobs(request):
    if JobCategory.objects.count() == 0:
        JobCategory(category="Full-Time").save()
        JobCategory(category="Part-Time").save()
        JobCategory(category="Internship").save()
        JobCategory(category="On-Campus").save()
        JobCategory(category="Co-Op").save()
        JobCategory(category="Fellowship").save()
        JobCategory(category="Miscellaneous").save()
    if JobStatus.objects.count() == 0:
        JobStatus(status="Applied").save()
        JobStatus(status="Not Applied").save()
        JobStatus(status="On Hold").save()
        JobStatus(status="Pending").save()
        JobStatus(status="Interviewing").save()
        JobStatus(status="Offer Accepted").save()
        JobStatus(status="Withdrawn").save()

    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        # print(id)
        Job.objects.filter(id=id).delete()
        return redirect("/jobs/")
    else:
        table_data = Job.objects.filter(user=request.user)
        print("ssss",Job.objects.all())
        context = {
            "table_data": table_data
        }
        for job in table_data:
            job.suggested_keywords = job.suggested_keywords.replace(']',"")
            job.suggested_keywords = job.suggested_keywords.replace('[',"")
            job.suggested_keywords = job.suggested_keywords.replace('',"")
            job.suggested_keywords = job.suggested_keywords.split(',')
            print(type(job.suggested_keywords))
            print((job.suggested_keywords))
        return render(request, 'jobs/jobs.html', context)


@login_required(login_url='/login/')
def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            add_form = JobEntryForm(
                request.POST, files=request.FILES, request=request)
            if (add_form.is_valid()):

                job = add_form.save(commit=False)
                job.user = request.user
                job.save()
                return redirect("/jobs/")
            else:
                context = {
                    "form_data": add_form
                }
                return render(request, 'jobs/add.html', context)
        else:
            # Cancel
            return redirect("/jobs/")
    else:
        context = {
            "form_data": JobEntryForm()
        }
    return render(request, 'jobs/add.html', context)


# @login_required(login_url='/login/')
# def edit(request, id):
#     if request.method == "GET":
#         # Load Job Entry Form with current model data.
#         job = Job.objects.get(id=id)
#         form = JobEntryForm(instance=job)
#         context = {"form_data": form}
#         return render(request, 'jobs/edit.html', context)
#     elif request.method == "POST":
#         # Process form submission
#         if "edit" in request.POST:
#             form = JobEntryForm(request.POST)
#             if form.is_valid():
#                 job = form.save(commit=False)
#                 job.id = id
#                 if request.user.is_authenticated:
#                     job.user = request.user
#                 job.save()
#                 return redirect("/jobs/")
#             else:
#                 context = {"form_data": form}
#                 return render(request, 'jobs/add.html', context)
#         else:
#             # Cancel
#             return redirect("/jobs/")


@login_required(login_url='/login/')
def edit(request, id):
    print(id,"id")
    if (request.method == "GET"):
        # Load Job Entry Form with current model data.
        job = Job.objects.get(id=id)
        form = JobEntryForm(instance=job)
        context = {"form_data": form}
        return render(request, 'jobs/edit.html', context)
    elif (request.method == "POST"):
        # Process form submission
        if ("edit" in request.POST):
            form = JobEntryForm(request.POST)
            if (form.is_valid()):
                job = form.save(commit=False)
                job.user = request.user
                job.id = id
                job.save()
                return redirect("/jobs/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'jobs/add.html', context)
        else:
            # Cancel
            return redirect("/jobs/")


@login_required(login_url='/login/')
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect("/jobs/")


def my_view(request):
    param_value = request.GET.get('param_name')
    clear_text = unquote(param_value)
    print("clear_text")
    print(clear_text)
    output_string = clear_text.replace(".", ".\n\n")
    output_string = output_string.replace("]", "]\n")
    lines = output_string.split(".")
    return render(
                request,
                "coverLetter.html",
                {"cover_letter": output_string, "keywords": ["res_keywords"],'lines': lines},
            )
    
