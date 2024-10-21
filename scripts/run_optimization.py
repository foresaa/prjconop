import sys
import os

# Add the parent directory to sys.path to make the apps module discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from apps.ms_project_interface import open_ms_project, update_project_with_optimized_schedule, save_project_as_optimized
from apps.optimization import optimize_schedule

def run_optimization():
    """
    Runs the optimization on an MS Project file.
    - Opens the MS Project file selected by the user.
    - Runs the optimization process.
    - Updates the MS Project schedulclse with optimized dates.
    - Saves a new version of the project file with the optimized schedule.
    """
    project, tasks, original_file_path = open_ms_project()  # User selects the file through a dialog
    
    if project and tasks:
        project_start = project.ProjectStart  # Get project start date
        hours_per_day = project.HoursPerDay   # Fetch the hours per day for the project
        
        # Run the optimization process, passing the project start date and hours per day
        optimized_schedule = optimize_schedule(tasks, project_start, hours_per_day, min_duration_percentage=0.95, max_duration_percentage=1.05)

        if optimized_schedule:
            update_project_with_optimized_schedule(project, optimized_schedule,hours_per_day)
            save_project_as_optimized(project, original_file_path)
            print(f"Optimization complete and project saved as {original_file_path}_opt.mpp.")
        else:
            print("Optimization was not applied.")
    else:
            print("No project file or tasks found.")

if __name__ == "__main__":
    run_optimization()
