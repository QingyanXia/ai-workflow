from app.models.task import Task
from app.models.step import Step

task = Task(input="test")

step1 = Step(description="step 1")
step2 = Step(description="step 2")

task.steps.append(step1)
task.steps.append(step2)

print(task)