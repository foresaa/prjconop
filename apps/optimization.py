from docplex.mp.model import Model
import re


def parse_predecessor(predecessor_str): 
    """
    Parses a predecessor string into its components: task ID, relationship type, and lead/lag time.
    
    Args                 : 
    predecessor_str (str): The predecessor string (e.g., '1FS', '2SS+5 days', '3FF-3 days').
    
      Returns                : 
      tuple                  : (predecessor_id, relationship_type, lead_lag_days)
    - predecessor_id (int)   : The ID of the predecessor task.
    - relationship_type (str): The type of relationship ('FS', 'SS', 'FF', 'SF').
    - lead_lag_days (int)    : The lead/lag time in days (positive for lead, negative for lag).
    """
    # Default relationship type if only a task ID is provided
    default_relationship = 'FS'
    
    # Check if the predecessor string is just a simple integer (e.g., '1')
    if predecessor_str.isdigit(): 
        return int(predecessor_str), default_relationship, 0
    
    # Complex predecessor pattern with relationship type and optional lead/lag
    pattern = r'(\d+)([FS|SS|FF|SF]+)?([+-]\d+)?\s*(days)?'
    match = re.match(pattern, predecessor_str.strip())
    
    if not match:
        raise ValueError(f"Invalid predecessor format: {predecessor_str}")
    
    predecessor_id = int(match.group(1))
    relationship_type = match.group(2) if match.group(2) else default_relationship
    lead_lag_days = int(match.group(3)) if match.group(3) else 0
    
    return predecessor_id, relationship_type, lead_lag_days


def optimize_schedule(tasks, project_start, hours_per_day, min_duration_percentage, max_duration_percentage): 
    """
    Optimize the project schedule by adjusting task durations and minimizing the project span.
    Task durations can vary within ±10%, while respecting predecessor constraints.
    
    Args                    : 
    tasks (list)            : List of task dictionaries with 'ID', 'Duration', 'Start', 'Finish', and 'Predecessors'.
    project_start (datetime): The project's start date.
        hours_per_day (float)          : The number of hours in a working day.
        min_duration_percentage (float): The minimum percentage of the current task duration.
        max_duration_percentage (float): The maximum percentage of the current task duration.
    
    Returns: 
    dict   : A dictionary of optimized task schedules with 'Start' and 'Finish' times in days.
    """
    model = Model(name="Project_Schedule_Optimization")
    
    start_times   = {}
    finish_times  = {}
    duration_vars = {}

    # Convert hours per day to seconds per day
    MINUTES_IN_HOUR = 60
    MINUTES_IN_DAY  = hours_per_day * MINUTES_IN_HOUR

    # Create decision variables for start times, finish times, and task durations
    for task in tasks: 
        task_id          = task['ID']
        duration_minutes = float(task['Duration'])  # Duration is in minutes
        duration_days    = duration_minutes / MINUTES_IN_DAY  # Convert to days based on hours per day

        # Decision variables for task start and finish times
        start_times[task_id]   = model.continuous_var(name=f"start_{task_id}")
        duration_vars[task_id] = model.continuous_var(lb=duration_days * min_duration_percentage,
                                                      ub   = duration_days * max_duration_percentage,
                                                      name = f"duration_{task_id}")
        finish_times[task_id] = start_times[task_id] + duration_vars[task_id]  # Finish = Start + Duration (in days)
    
    # Add predecessor constraints based on the task relationships
    for task in tasks: 
        task_id = task['ID']
        if task['Predecessors']: 
            predecessor_list = re.split(r'[;,]', task['Predecessors'])
            for predecessor_str in predecessor_list: 
                predecessor_id, relationship_type, lead_lag_days = parse_predecessor(predecessor_str)

                # Convert lead/lag days into lead/lag duration in days
                lead_lag_days = lead_lag_days / MINUTES_IN_DAY

                # Handle different types of predecessor relationships
                if relationship_type == 'FS':  # Finish-to-Start
                    model.add_constraint(start_times[task_id] >= finish_times[predecessor_id] + lead_lag_days,
                                         f"pred_{predecessor_id}_FS_{task_id}")
                elif relationship_type == 'SS':  # Start-to-Start
                    model.add_constraint(start_times[task_id] >= start_times[predecessor_id] + lead_lag_days,
                                         f"pred_{predecessor_id}_SS_{task_id}")
                elif relationship_type == 'FF':  # Finish-to-Finish
                    model.add_constraint(finish_times[task_id] >= finish_times[predecessor_id] + lead_lag_days,
                                         f"pred_{predecessor_id}_FF_{task_id}")
                elif relationship_type == 'SF':  # Start-to-Finish
                    model.add_constraint(finish_times[task_id] >= start_times[predecessor_id] + lead_lag_days,
                                         f"pred_{predecessor_id}_SF_{task_id}")
    
    # Objective: Minimize the overall project span (finish of the last task minus start of the first task)
    first_task_id = tasks[0]['ID']
    last_task_id = tasks[-1]['ID']
    project_span = finish_times[last_task_id] - start_times[first_task_id]
    model.minimize(project_span)

    # Solve the model
    solution = model.solve()

    # Collect the optimized schedule
    optimized_schedule = {}
    for task in tasks:
        task_id = task['ID']
        optimized_schedule[task_id] = {
            'Start': solution.get_value(start_times[task_id]),
            'Finish': solution.get_value(finish_times[task_id]),
            'Duration': solution.get_value(duration_vars[task_id])
        }
    
    return optimized_schedule
