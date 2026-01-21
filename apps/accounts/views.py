
from django.shortcuts import render, redirect
from .models import TestCase



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

