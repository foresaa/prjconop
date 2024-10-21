import sys
import os

# Add the parent directory to sys.path to make the apps module discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from apps.ms_project_interface import open_ms_project, update_project_with_optimized_schedule, save_project_as_optimized
from apps.optimization import optimize_schedule

def run_optimization(): 
    # Open the MS Project file and extract task data
    project, tasks, original_file_path = open_ms_project()
    
    # Define the project parameters
    project_start = project.ProjectStart
    hours_per_day = project.HoursPerDay  # Assuming project has this attribute
    
    # Define optimization parameters
    min_duration_percentage = 0.95  # Example: 95% of the original duration
    max_duration_percentage = 1.05  # Example: 105% of the original duration
    avoid_overallocation    = True  # Set this to True to avoid overallocation during optimization
    
    # Run the optimization process
    optimized_schedule = optimize_schedule(tasks, project_start, hours_per_day, 
                                           min_duration_percentage, max_duration_percentage, 
                                           avoid_overallocation)

    # Update the project with the optimized schedule
    update_project_with_optimized_schedule(project, optimized_schedule, hours_per_day)

    # Save the optimized project as a new file
    save_project_as_optimized(project, original_file_path)


if __name__ == "__main__":
    run_optimization()
