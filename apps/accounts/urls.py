from asyncio import events
from django.urls import path
from . import views

urlpatterns = [
    path('', views.editor_view, name='editor'),
    # path("testcase/", views.create_test_case, name="create_test_case"),

    # urls.py
path("editor/<int:test_case_id>/", views.editor_view, name="editor"),
path("testcase/", views.create_test_case, name="create_test_case"),


    ]