import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from starlette.responses import JSONResponse
from dotenv import load_dotenv  

load_dotenv()  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(f"Received query: {query}")
        graph = GraphBuilder(model_provider="groq")
        react_app=graph()
        # react_app = graph.build_graph()

        # Generate a visual diagram of the compiled graph using Mermaid
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph generated and saved as my_graph.png in {os.getcwd()}")

        # Assuming request is a pydantic object like: {"question": "your text"}
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Get the last message as the final output which is the AI response
        else:
            final_output = str(output)  # Convert to string if it's not already

        return {"answer": final_output}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

