from langchain_groq import ChatGroq
from Planner import PlanState
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel,Field
import os
from pathlib import Path

load_dotenv()

model=ChatGroq(
    api_key=os.getenv("api_key"),
    model="openai/gpt-oss-120b",
)

class coder_output(BaseModel):
    file_Name: str
    file_type: str
    content: str
    
class TestCaseFile(BaseModel):
    file_name: str = Field(description="Name of the test file, e.g. test_calculator.py")
    source_file_to_test: str = Field(description="The source code file being tested, e.g. calculator.py")
    description: str = Field(description="Overall responsibility of this test suite")
    test_scenarios: list[str] = Field(description="List of specific test scenarios, e.g. ['test addition of floats', 'test division by zero raises ZeroDivisionError']")


class TestCasePlanOutput(BaseModel):
    test_files: list[TestCaseFile]


def coder_node(state:PlanState):
    """
    this node is to create a code based on the plan generated
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are a code generation assistant. Generate a code based on the plan generated.for given file generate the code based on the description"),
        ("user", "complete project plan: {plan_generated}\n, i need the code based on the file description {file_description}"),
    ])

    model_with_structured_output=model.with_structured_output(coder_output)
    chain=prompt|model_with_structured_output
    response=chain.invoke({"plan_generated":state["plan_generated"],"file_description":state["files_to_create"][state["current_file_index"]].description })

    if not Path("Workfolder/temp_project/").exists():
        project_path =Path(__file__).resolve().parent/"Workfolder"/"temp_project"
        project_path.mkdir(parents=True,exist_ok=True)
    file_path=Path("Workfolder/temp_project/"+response.file_Name)
    file_path.write_text(response.content,encoding="utf-8")

    return{
        "current_file_index":state["current_file_index"]+1
    }


def test_plan_node(state:PlanState):
    """
Role & Persona:
You are an expert Senior QA Automation & Test Architect with deep expertise in test planning, file architecture design, and comprehensive test suite structuring across modern software architectures.
    """

    prompt = ChatPromptTemplate([
        ("system",
            """You are a Senior QA Automation Architect.
Your task is to analyze the project plan and created files to design a complete test file architecture.
For every code file that requires testing:
1. Determine the test file name (following standard conventions, e.g. test_<module>.py).
2. Specify which source file it is testing.
3. Provide a clear description and scope of the test suite.
4. List comprehensive test scenarios covering:
   - Happy paths and core functionality
   - Edge cases and boundary values
   - Negative paths and error handling (exceptions, invalid inputs)"""
        ),
        (
            "user",
            """Project Plan:
{plan_generated}
Project Type:
{project_type}
Code Files Created:
{files_created}
Generate the test file plan for this project.""")
    ])


    files_created_summary = "\n".join(
        [f"- {f.file_name}: {f.description}" for f in state.get("files_to_create", [])]
    )
    model_with_output = model.with_structured_output(TestCasePlanOutput)
    chain = prompt | model_with_output
    response = chain.invoke({
        "plan_generated": state.get("plan_generated", ""),
        "project_type": state.get("Project_Type", "new"),
        "files_created": files_created_summary,
    })
    print(response.test_files)
    return {
        "test_case_files": response.test_files
    }

    
    