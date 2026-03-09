from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import schemas
import usecase

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 読み込み
@app.get("/todos", response_model=list[schemas.Todo])
def get_todos():
    return usecase.read_data()

# 作成
@app.post("/todos", response_model=schemas.Todo)
def create_todo(todo_input: schemas.TodoCreate):
    todos = usecase.read_data()
    new_id = len(todos) + 1 if todos else 1
    
    new_todo = {
        "id": new_id,
        "title": todo_input.title,
        "description": todo_input.description,
        "status": schemas.TodoStatus.TODO.value, 
        "created_at": datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    usecase.write_data(todos)
    return new_todo

# 更新
@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate):
    todos = usecase.read_data()
    for todo in todos:
        if todo["id"] == todo_id:
            if todo_update.title is not None:
                todo["title"] = todo_update.title
            if todo_update.description is not None:
                todo["description"] = todo_update.description
            if todo_update.status is not None:
                todo["status"] = todo_update.status.value
            
            usecase.write_data(todos)
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# 削除
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todos = usecase.read_data()
    initial_len = len(todos)
    filtered_todos = [todo for todo in todos if todo["id"] != todo_id]
    
    if len(filtered_todos) == initial_len:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    usecase.write_data(filtered_todos)
    return {"message": "Todo deleted successfully"}

# インポート
@app.post("/todos/import")
def import_todos(todos: list[schemas.Todo]):
    existing_todos = usecase.read_data()
    new_id = max([t["id"] for t in existing_todos], default=0)
    
    for todo in todos:
        new_id += 1
        
        existing_todos.append({
            "id": new_id,
            "title": todo.title,
            "description": todo.description,
            "status": todo.status.value,
            "created_at": todo.created_at.isoformat()
        })
    
    usecase.write_data(existing_todos)
    return {"message": "Import and merge successful"}

# エクスポート
@app.get("/todos/export")
def export_todos():
    todos = usecase.read_data()
    
    return JSONResponse(
        content=todos,
        headers={"Content-Disposition": "attachment; filename=todos_backup.json"}
    )