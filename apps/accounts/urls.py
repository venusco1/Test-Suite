from asyncio import events
from django.urls import path
from . import views

urlpatterns = [
    path("", views.editor_view, name="home"),
    path("editor/<int:test_case_id>/", views.editor_view, name="editor"),
    path("testcase/", views.create_test_case, name="create_test_case"),
    path("load_xml/", views.load_xml, name="load_xml"),
    path("editor/", views.editor, name="editor"),
]
