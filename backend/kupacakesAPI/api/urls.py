from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path("cupcakes/create/", views.CupcakeCreate.as_view(), name="cupcake_create"),
    path(
        "cupcakes/<int:pk>/",
        views.CupcakeRetrieveUpdateDestroy.as_view(),
        name="cupcake_retrieve_update_destroy",
    ),
    path(
        "cupcakes/user/<int:pk>/",
        views.CupcakeListByUserId.as_view(),
        name="cupcake_list_by_user_id",
    ),
    path(
        "users/<int:pk>/",
        views.UserRetrieveUpdateDestroy.as_view(),
        name="user_retrieve_update_destroy",
    ),
    path("ingredients/", views.IngredientsList.as_view(), name="ingredients_list"),
    path("cupcakes/", views.CupcakeList.as_view(), name="cupcake_list"),
]
