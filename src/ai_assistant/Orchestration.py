from langgraph.graph import START,StateGraph,END
from Planner import plan_node,PlanState,pre_plan_node

from Creator import coder_node,test_node


def check_dev_test(state:PlanState):
    print(len(state["files_to_create"]))
    if state["current_file_index"]<len(state["files_to_create"]):
        return "Coder_node"
    else:
        return "Test_node"
graph_builder = StateGraph(PlanState)
graph_builder.add_node("plan_node", plan_node)
graph_builder.add_node("pre_plan_node", pre_plan_node)
graph_builder.add_node("Coder_node",coder_node)
graph_builder.add_node("Test_node",test_node)
# graph_builder.add_node("requirement_node", requirement_node)
# graph_builder.add_edge(START, "requirement_node")
graph_builder.add_edge(START, "pre_plan_node")
graph_builder.add_edge("pre_plan_node", "plan_node")
graph_builder.add_conditional_edges("plan_node",check_dev_test,{"Coder_node":"Coder_node","Test_node":"Test_node"})
graph_builder.add_conditional_edges("Coder_node",check_dev_test,{"Coder_node":"Coder_node","Test_node":"Test_node"})
graph_builder.add_edge("Test_node", END)
graph=graph_builder.compile()

graph.invoke({"input":"create a calculator using python "})


