from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import(
  View, TemplateView, RedirectView
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
  CreateView, UpdateView, DeleteView,
  FormView,
)
from .forms import FoodForm, FoodUpdateForm, PictureUploadForm 
from datetime import datetime
from .models import Foods, Pictures
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from . import forms

class IndexView(View):
  
  def get(self, request, *args, **kwargs):
    food_form = FoodForm()  # 修正されたインスタンス化
    return render(request, "index.html", context={
      "food_form": food_form,
    })
    
  def post(self, request, *args, **kwargs):
    food_form = FoodForm(request.POST or None)  # 修正されたインスタンス化
    if food_form.is_valid():
      food_form.save()
      return redirect("food:list_foods")
    return render(request, "index.html", context={
      "food_form": food_form,
    })
    
class HomeView(TemplateView):
  
  template_name = "food/home.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["name"] = kwargs.get("name")
    context["time"] = datetime.now()
    return context
  
class FoodDetailView(DetailView):
  model = Foods
  template_name = "food/food.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context
  
class FoodListView(ListView):
  model = Foods
  template_name = "food/food_list.html"
  
  def get_queryset(self):
    qs = super().get_queryset()
    if "name" in self.kwargs:
      qs = qs.filter(name__startswith=self.kwargs["name"])
    qs = qs.order_by("expirydate")
    return qs
  
class FoodCreateView(CreateView):
  model = Foods
  form_class = FoodForm  # 修正されたインスタンス化
  template_name = "food/add_food.html"
  success_url = reverse_lazy("food:list_foods")
  
  def form_valid(self, form):
    form.instance.create_at = datetime.now()
    form.instance.update_at = datetime.now()
    return super().form_valid(form)
  
  def get_initial(self, **kwargs):
    initial = super().get_initial(**kwargs)
    initial["name"] = "sample"
    return initial
  
class FoodUpdateView(SuccessMessageMixin, UpdateView):
  template_name = "food/update_food.html"
  model = Foods
  form_class = FoodUpdateForm  # 修正されたインスタンス化
  success_message = "更新に成功しました"

  def get_success_url(self):
    return reverse_lazy("food:edit_food", kwargs={"pk": self.object.id})

  def get_success_message(self, cleaned_data):
    return cleaned_data.get("name") + "を更新しました"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    picture_form = forms.PictureUploadForm()
    pictures = Pictures.objects.filter_by_food(food=self.object)
    context["pictures"] = pictures
    context["picture_form"] = PictureUploadForm() 
    return context
  
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    picture_form = PictureUploadForm(request.POST, request.FILES)  # 修正されたインスタンス化
    if picture_form.is_valid():
      picture_form.save(food=self.object)
    return super().post(request, *args, **kwargs)
  
class FoodDeleteView(DeleteView):
  model = Foods
  template_name = "food/delete_food.html"
  success_url = reverse_lazy("food:list_foods")
  
class FoodFormView(FormView):
  
  template_name = "food/form_food.html"
  form_class = FoodForm  # 修正されたインスタンス化
  success_url = reverse_lazy("food:list_foods")
  
  def get_initial(self):
    initial = super().get_initial()
    initial["name"] = "form sample"
    return initial
  
  def form_valid(self, form):
    if form.is_valid():
      form.save()
    return super().form_valid(form)
  
class FoodRedirectView(RedirectView):
  url = "https://google.co.jp"
  
  def get_redirect_url(self, *args, **kwargs):
    food = Foods.objects.first()
    if "pk" in kwargs:
      return reverse_lazy("food:detail_food", kwargs={"pk": kwargs["pk"]})
    return reverse_lazy("food:edit_food", kwargs={"pk": food.pk})
  
def delete_picture(request, pk):
  picture = get_object_or_404(Pictures, pk=pk)
  picture.delete()
  import os
  if os.path.isfile(picture.picture.path):
    os.remove(picture.picture.path)
  messages.success(request, "画像を削除しました")
  return redirect("food:edit_food", pk=picture.food.id)