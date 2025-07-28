from typing import List , Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from dotenv import load_dotenv 
from langgraph.graph import MessageGraph, END
from chains import reflection_chain , generation_chain
load_dotenv()

graph=MessageGraph()

REFLECT="reflect" 
GENERATE="generate"

def reflect_node(state):
    response=reflection_chain.invoke({
        "messages": state
    })
    return [HumanMessage(content=response)]

def generate_node(state):
    response=    generation_chain.invoke({
        "messages":state
    })
    return response

def should_continue(state):
    if(len(state)>8):
        return "END"
    return "REFLECT"

graph.add_node(GENERATE , generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)





graph.add_conditional_edges(
    GENERATE,
    should_continue,
    path_map={
        "REFLECT": REFLECT,
        "END": END
    }
)
graph.add_edge(REFLECT, GENERATE)

app=graph.compile()


print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

response = app.invoke(HumanMessage(content="write your message on what tweet you want"))

print(response)