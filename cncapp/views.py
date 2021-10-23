from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .models import CncProg
from .models import MyCutter
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def create_cnc(request):
    cncprog = CncProg.objects.order_by('-id')[:5]
    if request.method == 'POST':
        cnc_form = forms.CncForm(request.POST)
        dct = {'plastic': [300, 400, 0.02, 0.06, 0.15, 0.20, 0.30],
               'plexiglas': [100, 150, 0.02, 0.05, 0.10, 0.18, 0.25],
               'wood': [200, 450, 0.02, 0.035, 0.055, 0.09, 0.12],
               'non-ferrous metal': [120, 250, 0.01, 0.02, 0.03, 0.04, 0.07],
               'aluminium': [120, 500, 0.01, 0.03, 0.04, 0.05, 0.08],
               'magnesium': [150, 300, 0.01, 0.02, 0.035, 0.04, 0.075],
               'steel': [35, 50, 0.005, 0.01, 0.015, 0.02, 0.03],
               'cast iron': [40, 60, 0.005, 0.015, 0.02, 0.03, 0.04],
               'titanium': [20, 30, 0.005, 0.01, 0.02, 0.03, 0.04]
               }
        if cnc_form.is_valid():
            new_cnc = cnc_form.save(commit=False)
            new_cnc.cut_speed_min = dct[new_cnc.material][0]
            new_cnc.cut_speed_max = dct[new_cnc.material][1]
            if 0.3 <= new_cnc.cutter_diameter <= 0.7:
                new_cnc.feed_per_tooth = dct[new_cnc.material][2]
            elif 0.7 < new_cnc.cutter_diameter <= 2.5:
                new_cnc.feed_per_tooth = dct[new_cnc.material][3]
            elif 2.5 < new_cnc.cutter_diameter <= 4.5:
                new_cnc.feed_per_tooth = dct[new_cnc.material][4]
            elif 4.5 < new_cnc.cutter_diameter <= 7:
                new_cnc.feed_per_tooth = dct[new_cnc.material][5]
            else:
                new_cnc.feed_per_tooth = dct[new_cnc.material][6]

            new_cnc.spindel_speed_min = \
                round(int((1000 * new_cnc.cut_speed_min) / (3.14 * new_cnc.cutter_diameter)), -2)

            new_cnc.moving_speed_min = \
                round(int(new_cnc.feed_per_tooth * new_cnc.teeth_numbers * new_cnc.spindel_speed_min), -2)

            new_cnc.spindel_speed_max = \
                round(int((1000 * new_cnc.cut_speed_max) / (3.14 * new_cnc.cutter_diameter)), -2)

            new_cnc.moving_speed_max = \
                round(int(new_cnc.feed_per_tooth * new_cnc.teeth_numbers * new_cnc.spindel_speed_max), -2)

            new_cnc.save()
            return render(request, "home.html", {'form': cnc_form, 'cncprog': cncprog})
    else:
        cnc_form = forms.CncForm()
    return render(request,  "home.html", {'form': cnc_form, 'cncprog': cncprog})


def view_profile(request):
    return render(request,
                  'profile.html')


def register(request):
    if request.method == 'POST':
        user_form = forms.RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user, photo='unknown.jpeg')
            return render(request, 'registration/reg_compete.html', {'new_user': new_user})
        else:
            return HttpResponse('Bad pass')
    else:
        user_form = forms.RegistrationForm()
        return render(request, 'registration/register_user.html', {'form': user_form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = forms.UserEditForm(request.POST,
                                       instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST,
                                             instance=request.user.profile,
                                             files=request.FILES)
        if user_form.is_valid():

            if profile_form.is_valid():

                if not profile_form.cleaned_data['photo']:
                    profile_form.cleaned_data['photo'] = request.user.profile.photo
                profile_form.save()
                user_form.save()
                return render(request, 'profile.html')
    else:
        user_form = forms.UserEditForm(request.POST,
                                       instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST,
                                             instance=request.user.profile)
        return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def how_it_made(request):
    return render(request, 'how_it_made.html')


@login_required
def my_cutter(request):
    my_cut = MyCutter.objects.order_by('-id')[:10]
    if request.method == 'POST':
        my_cutter_form = forms.MyCatterForm(request.POST)

        if my_cutter_form.is_valid():
            mcut = my_cutter_form.save(commit=False)
            mcut.save()
            return render(request, "my_cutters.html", {'form': my_cutter_form, 'my_cut': my_cut})
    else:
        my_cutter_form = forms.MyCatterForm()
    return render(request,  "my_cutters.html", {'form': my_cutter_form, 'my_cut': my_cut})
