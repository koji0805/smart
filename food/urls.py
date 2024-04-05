from django.urls import path
from .views import (
  IndexView, HomeView, FoodDetailView,
  FoodListView, FoodCreateView, FoodUpdateView,
  FoodDeleteView, FoodFormView, FoodRedirectView,
  delete_picture,
)
from django.views.generic.base import RedirectView

app_name = "food"

urlpatterns = [
  path("index/", IndexView.as_view(), name="index"),
  path("home/<name>/", HomeView.as_view(), name="home"),
  path("detail_food/<int:pk>/", FoodDetailView.as_view(), name="detail_food"),
  path("list_foods/", FoodListView.as_view(), name="list_foods"),
  path("add_food/", FoodCreateView.as_view(), name="add_food"),
  path("edit_food/<int:pk>/", FoodUpdateView.as_view(), name="edit_food"),
  path("delete_food/<int:pk>/", FoodDeleteView.as_view(), name="delete_food"),
  path("food_form/", FoodFormView.as_view(), name="food_form"),
  path("food_redirect_view/<int:pk>/", FoodRedirectView.as_view(), name="food_redirect_view"),
  path("delete_picture/<int:pk>/", delete_picture, name="delete_picture"),
]
