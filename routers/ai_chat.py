# from fastapi import APIRouter,HTTPException
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from schema import ChatRequest, ChatResponse
# from langchain.agents import create_agent
# from langgraph.checkpoint.sqlite import SqliteSaver
# import sqlite3

# router = APIRouter(
#     prefix="/ai",
#     tags=["AI Chat"]
# )

# DB_PATH = "blog_mng.db"
# load_dotenv()


# def get_checkpointer():
#     conn = sqlite3.connect(DB_PATH,check_same_thread=False)
#     checkpointer = SqliteSaver(conn)
#     checkpointer.setup()
#     return checkpointer


# checkpointer = get_checkpointer()

# def initialize_agent():
    
#     llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")
    
#     agent = create_agent(
#         model = llm,
#         tools=[],
#         checkpointer=checkpointer
#     )
    
#     return agent
    
# agent = initialize_agent()
    

# @router.post("/chat",response_model=ChatResponse)
# def chat_with_ai(request: ChatRequest):
#     try:
#         if not request.question.strip():
#             raise HTTPException(
#                 status_code=400,detail="Question cannont be empty"
#             )
            
#         config = {"configurable": {"thread_id": "chirag"}}
        
#         # def get_all_blogs(db:Session = Depends(get_db)):
#         # blogs = db.query(DbBlog).all()
        

#         # system_message = {
#         #     "role": "system",
#         #     "content": f"""You are a helpful assistant that answers questions about blog posts.
#         #
#         # Here are the available blogs:
#         # {blog_context}
#         #
#         # Use this information to answer user questions accurately."""
#         # }
        
        
#         result =agent.invoke(
#             {"messages": [{"role": "user","content": request.question}]},config=config
#         )
            
#         response_content = result["messages"][-1].content
        
        
#         return ChatResponse(response=response_content)
            
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error processing request : {e}"  
#             )


# @router.delete("/chat/history") 
# def clear_chat_history():
    
#     conn = sqlite3.connect(DB_PATH,check_same_thread=False)
#     cursor = conn.cursor()
    
#     cursor.execute("DELETE FROM checkpoints WHERE thread_id = 'sagar'")
#     cursor.execute("DELETE FROM writes WHERE thread_id = 'sagar'")
#     conn.commit()
#     conn.close
    
#     return {"message": "Chat history cleaned successfully"}
     
    