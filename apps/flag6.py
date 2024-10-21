import win32com.client

def mark_tasks_ready_to_start():
    # Connect to the active instance of MS Project
    project = win32com.client.Dispatch("MSProject.Application").ActiveProject
    
    # Iterate through each task in the active project
    for task in project.Tasks:
        # Skip if the task has no predecessors or is 100% complete
        if task is not None and task.PredecessorTasks.Count > 0 and task.PercentComplete == 0:
            ready_to_start = True
            
            # Check if all predecessors are 100% complete
            for pred in task.PredecessorTasks: 
                if task.PredecessorTasks.Count > 0:
                    if pred.PercentComplete < 100:
                      ready_to_start = False
                    break
            
            # Set a custom Flag (e.g., Flag6) if all predecessors are complete
            task.Flag6 = ready_to_start

# Run the function
mark_tasks_ready_to_start()
