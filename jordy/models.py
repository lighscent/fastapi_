from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Todo(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=250)
    due_date = fields.CharField(max_length=250)

class PydanticMeta:
    pass


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)

# if __name__ == "__main__":
#     # uvicorn.run(app, host="127.0.0.1", port=8000)
#     uvicorn.run("models:app", host="127.0.0.1", port=8000, reload=True)
#     print("Ready.")
