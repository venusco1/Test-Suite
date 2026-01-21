
from django.shortcuts import render, redirect
from .models import TestCase

# def home(request):
#     return render(request, "public/home.html")


DEFAULT_TESTCASE_XML = """
<Project>
    <TestSuite Name="Sessions">
        <TestCase Name="RA_Sanity">
            <PreCondition>
                <!-- blocks -->
            </PreCondition>

            <Action>
                <!-- blocks -->
            </Action>

            <PostCondition>
                <!-- blocks -->
            </PostCondition>
        </TestCase>
    </TestSuite>
</Project>
"""




def editor_view(request, test_case_id=None):
    if test_case_id is None:
        return render(request, "public/editor.html")

    test_case = TestCase.objects.get(id=test_case_id)

    return render(request, "public/editor.html", {
        "test_case": test_case,
        "xml": test_case.xml_content
    })




from django.shortcuts import redirect

def create_test_case(request):
    if request.method == "POST":
        title = request.POST.get("title")

        test_case = TestCase.objects.create(
            title=title,
            xml_content=DEFAULT_TESTCASE_XML
        )

        # 🔥 REDIRECT WITH ID
        return redirect("editor", test_case_id=test_case.id)

    # fallback (optional)
    return redirect("editor", test_case_id=1)




import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.contrib import messages

def load_xml(request):
    if request.method == "POST":
        xml_content = None

        # File upload
        if request.FILES.get("xml_file"):
            xml_content = request.FILES["xml_file"].read().decode("utf-8")

        # Textarea input
        elif request.POST.get("xml_text"):
            xml_content = request.POST.get("xml_text")

        if not xml_content:
            messages.error(request, "Please upload or paste XML.")
            return render(request, "public/load_xml.html")

        try:
            # Validate XML
            ET.fromstring(xml_content)

            # Store in session
            request.session["xml_content"] = xml_content

            return redirect("editor")

        except ET.ParseError as e:
            messages.error(request, f"Invalid XML: {e}")

    return render(request, "public/load_xml.html")



import xml.etree.ElementTree as ET

def xml_to_tree(element):
    return {
        "tag": element.tag,
        "children": [xml_to_tree(child) for child in element]
    }

def editor(request):
    xml_content = request.session.get("xml_content", "")

    tree_data = None
    if xml_content:
        root = ET.fromstring(xml_content)
        tree_data = xml_to_tree(root)

    return render(request, "public/editor1.html", {
        "xml_content": xml_content,
        "tree_data": tree_data
    })
