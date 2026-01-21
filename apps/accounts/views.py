
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
            try:
                xml_file = request.FILES["xml_file"]
                
                # Validate file size (5MB max)
                if xml_file.size > 5 * 1024 * 1024:
                    messages.error(request, "File size must be less than 5MB")
                    return render(request, "public/load_xml.html")
                
                # Validate file extension
                if not xml_file.name.endswith('.xml'):
                    messages.error(request, "Please upload an XML file (.xml)")
                    return render(request, "public/load_xml.html")
                
                # Read file with error handling
                try:
                    xml_content = xml_file.read().decode("utf-8")
                except UnicodeDecodeError:
                    try:
                        xml_content = xml_file.read().decode("latin-1")
                    except Exception:
                        messages.error(request, "Unable to read file. Please ensure it's a valid XML file with UTF-8 or Latin-1 encoding.")
                        return render(request, "public/load_xml.html")
                        
            except Exception as e:
                messages.error(request, f"Error reading file: {str(e)}")
                return render(request, "public/load_xml.html")

        # Textarea input
        elif request.POST.get("xml_text"):
            xml_content = request.POST.get("xml_text").strip()

        if not xml_content:
            messages.error(request, "Please upload or paste XML content.")
            return render(request, "public/load_xml.html")

        try:
            # Validate XML structure
            root = ET.fromstring(xml_content)
            
            # Check if root is valid
            if not root.tag:
                messages.error(request, "Invalid XML structure: root element not found.")
                return render(request, "public/load_xml.html")

            # Store in session
            request.session["xml_content"] = xml_content

            messages.success(request, "XML loaded successfully!")
            return redirect("editor_no_id")

        except ET.ParseError as e:
            # More helpful error message
            error_msg = f"Invalid XML syntax at line {e.position[0]}: {str(e)}"
            messages.error(request, error_msg)
            # Keep the content in textarea for user to fix
            return render(request, "public/load_xml.html", {"xml_text": xml_content if not request.FILES.get("xml_file") else ""})
        except Exception as e:
            messages.error(request, f"Error processing XML: {str(e)}")
            return render(request, "public/load_xml.html")

    return render(request, "public/load_xml.html")



import xml.etree.ElementTree as ET

def xml_to_tree(element):
    return {
        "tag": element.tag,
        "attributes": element.attrib,  
        "children": [xml_to_tree(child) for child in element]
    }


def editor(request):
    xml_content = request.session.get("xml_content", "")

    tree_data = None
    if xml_content:
        root = ET.fromstring(xml_content)
        tree_data = xml_to_tree(root)

    return render(request, "public/editor.html", {
        "xml_content": xml_content,
        "tree_data": tree_data
    })
