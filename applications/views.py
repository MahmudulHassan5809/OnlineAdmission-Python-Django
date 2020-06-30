from django.shortcuts import render, redirect, get_object_or_404
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views import View, generic
# Create your views here.
