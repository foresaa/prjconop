import win32com.client
from tkinter import Tk, filedialog
from datetime import timedelta, datetime
import os

def convert_pywintypes_datetime(dt):
    """
    Converts a pywintypes.Time object to a standard Python datetime object.
    
    Args:
        dt: The date/time object returned by win32com (MS Project COM interface).
    
    Returns:
        datetime: The equivalent Python datetime object, or the input if no conversion is necessary.
    """
    if type(dt).__name__ == 'Time':
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return dt

def convert_to_datetime(start_date, days):
    """
    Converts the number of days into a datetime object based on the project start date.
    
    Args:
        start_date (datetime): The reference project start date.
        days (float or datetime): The number of days from the project start date 
        or a datetime object.
    
    Returns:
        datetime: The corresponding date and time calculated by adding 'days' to 'start_date', 
        or directly returns 'days' if it is already a datetime object.
    """
    if isinstance(days, datetime):
        return days
    return start_date + timedelta(days=days)

def open_ms_project():
    """
    Opens an MS Project file, reads the tasks, and extracts relevant task data.
    
    - Prompts the user to select an MS Project file using a file dialog.
    - Reads task data from the active MS Project.
    
    Returns:
        project (win32com.client.Dispatch): The active MS Project object.
        tasks (list): A list of dictionaries with task data including:
            - 'ID': Task ID.
            - 'Name': Task name.
            - 'Duration': Task duration in seconds.
            - 'Start': Task start date/time.
            - 'Finish': Task finish date/time.
            - 'Predecessors': The task predecessors in the format provided by MS Project.
        file_path (str): The path to the selected MS Project file.
    """
    project_app = win32com.client.Dispatch("MSProject.Application")
    project_app.Visible = True  # Make MS Project visible to the user

    # Prompt the user to select an MS Project file using a file dialog
    Tk().withdraw()  # Hide the root Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select MS Project File",
        filetypes=(("Microsoft Project files", "*.mpp"), ("All files", "*.*"))
    )
    
    project_app.FileOpen(file_path)
    project = project_app.ActiveProject

    tasks = []
    for task in project.Tasks:
        if task is not None and not task.Summary:
            task_info = {
                'ID': task.ID,  # Task ID
                'Name': task.Name,  # Task name
                'Duration': float(task.Duration),  # Task duration in seconds
                'Start': convert_pywintypes_datetime(task.Start),
                'Finish': convert_pywintypes_datetime(task.Finish),
                'Predecessors': task.Predecessors,
            }
            tasks.append(task_info)
    
    return project, tasks, file_path

def update_project_with_optimized_schedule(project, optimized_schedule, hours_per_day):
    """
    Updates the MS Project schedule with the optimized start and calculated duration 
    (derived from optimized start and finish times). 
    
    Only updates start and duration to allow MS Project to calculate finish dates, 
    then validates that the calculated finish matches the optimized finish.

    Args:
        project (win32com.client.Dispatch): The active MS Project object.
        optimized_schedule (dict): A dictionary where the keys are task IDs and the values are:
            - 'Start': Optimized task start time in days from the project start.
            - 'Finish': Optimized task finish time in days from the project start.
        hours_per_day (float): Number of working hours per day, used to calculate durations in days.
    """
    project_start = project.ProjectStart  # Get project start date
    MINUTES_IN_HOUR = 60
    MINUTES_IN_DAY = hours_per_day * MINUTES_IN_HOUR

    # Iterate over tasks and update their start/duration with optimized times
    for task in project.Tasks:
        if task is not None and task.ID in optimized_schedule:
            optimized_task = optimized_schedule[task.ID]
            
            # Convert the optimized start and finish times to datetime objects using the project start date
            task_start = convert_to_datetime(project_start, optimized_task['Start'])
            task_finish = convert_to_datetime(project_start, optimized_task['Finish'])

            # Calculate the optimized duration in days
            optimized_duration_days = (optimized_task['Finish'] - optimized_task['Start'])
            optimized_duration_seconds = optimized_duration_days * MINUTES_IN_DAY
            # Set the task type to "Fixed Work" (pjFixedWork corresponds to "Fixed Work" in MS Project)
            pjFixedWork =2
            task.Type = pjFixedWork
            # Overwrite start and duration in MS Project (let MS Project calculate the finish date)
            task.Start = task_start
            task.Duration = optimized_duration_seconds # MS Project expects duration in days
            
            # Set the task constraint to "As Soon As Possible"
            task.ConstraintType = 0  # 0 corresponds to "As Soon As Possible"
            

def save_project_as_optimized(project, original_file_path):
    """
    Saves the project file with "_opt" suffix in the same folder as the original file.
    
    Args:
        project (win32com.client.Dispatch): The active MS Project object.
        original_file_path (str): The file path of the original MS Project file.
    """
    folder_path = os.path.dirname(original_file_path)
    optimized_file_name = os.path.join(folder_path, os.path.basename(original_file_path).replace('.mpp', '_opt.mpp'))
    
    # Save the project as the new optimized file
    project.Application.FileSaveAs(optimized_file_name)
    
    # Close the optimised file which is now ActiveProject
    # without saving any changes to it
    pjDoNotSave = 0
    project.Application.FileCloseEx(pjDoNotSave)
