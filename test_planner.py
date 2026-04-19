from app.core.planner import plan_steps

task = "Write a report about the applications of AI in education"

steps = plan_steps(task)

for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")