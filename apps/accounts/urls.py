from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("load-xml/", views.load_xml, name="load_xml"),
    path("xml-view/", views.xml_view, name="xml_view"),
    path("edit-xml-view/", views.edit_xml_view, name="edit_xml_view"),

    
    path("generate-xml/", views.generate_xml, name="generate_xml"),
    # Keep existing URLs for backward compatibility
    
    path("editor/<int:test_case_id>/", views.editor_view, name="editor"),
    path("testcase/", views.create_test_case, name="create_test_case"),
]
