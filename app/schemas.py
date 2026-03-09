from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TodoStatus(str, Enum):
    TODO = "todo"     # 未完了
    DONE = "done"     # 完了

# ユーザーが「入力」するデータ
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1) 
    description: str | None = None # 詳細説明は任意

# サーバーが「返す」データ
class Todo(TodoCreate):
    id: int
    status: TodoStatus = TodoStatus.TODO
    created_at: datetime 

# 更新用のデータ
class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1)
    description: str | None = None
    status: TodoStatus | None = None