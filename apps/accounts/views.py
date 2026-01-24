
from django.shortcuts import render, redirect
from .models import TestCase

import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, "public/home.html")


def xml_to_tree(element):
    return {
        "tag": element.tag,
        "attributes": element.attrib,  
        "children": [xml_to_tree(child) for child in element]
    }
      
        
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
            return redirect("xml_view")

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


def xml_view(request):
    xml_content = request.session.get("xml_content", "")
    tree_data = None
    
    if xml_content:
        try:
            root = ET.fromstring(xml_content)
            tree_data = xml_to_tree(root)
        except ET.ParseError:
            # Handle invalid XML
            xml_content = ""
            tree_data = None
    
    return render(request, "public/xml_view.html", {
        "xml_content": xml_content,
        "tree_data": tree_data
    })


def edit_xml_view(request):
    xml_content = request.session.get("xml_content", "")
    tree_data = None
    
    if xml_content:
        try:
            root = ET.fromstring(xml_content)
            # Use execution tree for edit view as well
            tree_data = xml_to_tree(root)
        except ET.ParseError:
            xml_content = ""
            tree_data = None
    
    return render(request, "public/edit_xml_view.html", {
        "xml_content": xml_content,
        "tree_data": tree_data
    })




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





def generate_xml(request):
    if request.method == "POST":
        title = request.POST.get("title")
        test_suite_name = request.POST.get("test_suite_name", "Default Suite")
        test_case_name = request.POST.get("test_case_name", "Default Test Case")
        
        # Generate XML structure
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Project>
    <TestSuite Name="{test_suite_name}">
        <TestCase Name="{test_case_name}">
            <Metadata>
                <SavedVariables>
                    <Variable Index="1">MEASUREMENT_STATE</Variable>
                    <Variable Index="2">TEST_RESULT</Variable>
                </SavedVariables>
            </Metadata>
            <PreCondition>
                <Block ModelType="ReferencedModel" Name="TestEnvReset">
                    <Block ModelType="Subsystem" Name="StartCanoeSimulationIfNotAlready">
                        <Job BlockPath="TestEnvReset/StartCanoeSimulationIfNotAlready/JOB" EvaluationEnable="0" MappingName="CANoeCANalyzer01.IsMeasurementRunning" SaveEnable="1" SaveVariable="MEASUREMENT_STATE"/>
                        <IfThenElse BlockPath="TestEnvReset/StartCanoeSimulationIfNotAlready/IfThenElse" Value="MEASUREMENT_STATE == 0">
                            <ThenBranch>
                                <Job BlockPath="TestEnvReset/StartCanoeSimulationIfNotAlready/JOB1" EvaluationEnable="0" MappingName="CANoeCANalyzer01.StartMeasurement" SaveEnable="0"/>
                                <Wait BlockPath="TestEnvReset/StartCanoeSimulationIfNotAlready/Wait" Time="5" TimeType="numeric" Unit="s"/>
                            </ThenBranch>
                        </IfThenElse>
                    </Block>
                </Block>
            </PreCondition>
            <Action>
                <!-- Add your test actions here -->
                <Block ModelType="Subsystem" Name="MainTestLogic">
                    <Job BlockPath="MainTestLogic/VerifySystem" EvaluationEnable="1" MappingName="SystemMonitor01.VerifySystem" SaveEnable="1" SaveVariable="TEST_RESULT"/>
                </Block>
            </Action>
            <PostCondition>
                <Block ModelType="Subsystem" Name="Cleanup">
                    <Job BlockPath="Cleanup/StopMeasurement" EvaluationEnable="0" MappingName="CANoeCANalyzer01.StopMeasurement" SaveEnable="0"/>
                </Block>
            </PostCondition>
        </TestCase>
    </TestSuite>
</Project>"""
        
        # Save to database
        test_case = TestCase.objects.create(
            title=title,
            xml_content=xml_content
        )
        
        return redirect("editor", test_case_id=test_case.id)
    
    return render(request, "public/generate_xml.html")


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
