
from langgraph.graph import MessagesState
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from langgraph.graph.message import add_messages
from typing import Annotated
from pydantic import BaseModel,Field
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class PlanState(MessagesState):
    input: str
    Project_Name : str
    Project_Type : str
    Project_description: str
    Project_requirement: str
    Existing_files : list[str]
    plan_generated : str
    files_to_create : list[dict]
    files_to_update : list[dict]
    files_to_delete : list[dict]
    test_case_files : list[dict]
    current_file_index : int
    code_generated : str
    test_generated : str
    test_execution  : str
    report_generated : str
    test_passed : str
    iteration : int
    code_refinement_iteration : int

class FileItem(BaseModel):
    file_name: str
    description: str
class preplan_output(BaseModel):
    Project_Name :str
    Project_Type : str = Field(
        description="Must be either 'new' or 'existing'"
    )
    Project_description: str
    Project_requirement: str

class plan_output(BaseModel):
    plan_generated : str
    files_to_create : list[FileItem]
    files_to_update : list[FileItem]
    files_to_delete : list[FileItem]
    current_file_index : int
model=ChatGroq(model="openai/gpt-oss-120b",api_key=os.getenv("api_key"))

# def requirement_node(state:PlanState):
#     """
#     this node is for taking the input from the user
#     """
#     user_input=input("what is the input you want to give")
#     return {
#         "Input":user_input,
#         "iteration":0,
#         "code_refinement_iteration":0,
#         "test_passed":"pending"
#     }
    
def pre_plan_node(state:PlanState):
    """we have to check the existing file in the folder
    if any existing file is there then we have to check the requirement with the existing file
    and check the requirement is related to modify the existing file or it complete new project"""
    
    if Path("Workfolder").exists():

        workfolder=Path("Workfolder")

        folderlist=list(workfolder.rglob("*"))
        
        if len(folderlist)==0:
            return{
                "Project_Type":"new",
                "Project_description":"",
                "Project_requirement":""
            }
        else:
            projectdetails_file=Path("Workfolder/temp_project/README.md")
            if projectdetails_file.exists():
                projectdetails=projectdetails_file.read_text()
            
            prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a project evaluation engine.

            Analyze the existing project details and the user's new requirement.

            Determine whether the user wants:

            - "new" → a completely new project
            - "existing" → modify or extend the existing project

            Return:
            1. Project_Type
            2. Project_description
            3. Project_requirement

            Project_Type MUST be exactly "new" or "existing".

            Existing project details:
            {projectdetails}

            New user requirement:
            {input}
            """
            )
        ])

            model_with_output=model.with_structured_output(preplan_output)

            chain=prompt|model_with_output
            response=chain.invoke({"projectdetails":projectdetails,"input":state["input"]})
            
            return {
                "Project_Type": response.Project_Type,
                "Project_description": response.Project_description,
                "Project_requirement": response.Project_requirement
            }





    

def plan_node(state:PlanState):
    """
    this node to define the plan from the input
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are a code generation assistant. Generate a plan for the given input.what all files is required and what are the steps to be taken to generate the code.you have give only 1 best approach and steps must be in point format and you have to focus only on development and don't include anything extra files must have need files requiremt.txt and Readme.md"),
        ("user", "{input}"),
    ])
    model_output=model.with_structured_output(plan_output)
    chain=prompt|model_output
    response=chain.invoke({"input":state["input"]})
    # print(response.plan_generated)
    print(response.files_to_create)
    # print(response.files_to_update)
    # print(response.files_to_delete)
    # print(response.current_file_index)
    return{
        "plan_generated":response.plan_generated,
        "files_to_create":response.files_to_create,
        "files_to_update":response.files_to_update,
        "files_to_delete":response.files_to_delete,
        "current_file_index":0,
    }


if __name__=="__main__":
   pass