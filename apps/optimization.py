from docplex.mp.model import Model
import re

def parse_predecessor(predecessor_str): 
    """
    Parses a predecessor string into its components: task ID, relationship type, and lead/lag time.
    
    Args:
        predecessor_str (str): The predecessor string (e.g., '1FS', '2SS+5 days', '3FF-3 days').
    
    Returns:
        tuple: (predecessor_id, relationship_type, lead_lag_days)
            - predecessor_id (int): The ID of the predecessor task.
            - relationship_type (str): The type of relationship ('FS', 'SS', 'FF', 'SF').
            - lead_lag_days (int): The lead/lag time in days (positive for lead, negative for lag).
    """
    default_relationship = 'FS'
    
    if predecessor_str.isdigit(): 
        return int(predecessor_str), default_relationship, 0
    
    pattern = r'(\d+)([FS|SS|FF|SF]+)?([+-]\d+)?\s*(days)?'
    match = re.match(pattern, predecessor_str.strip())
    
    if not match:
        raise ValueError(f"Invalid predecessor format: {predecessor_str}")
    
    predecessor_id = int(match.group(1))
    relationship_type = match.group(2) if match.group(2) else default_relationship
    lead_lag_days = int(match.group(3)) if match.group(3) else 0
    
    return predecessor_id, relationship_type, lead_lag_days


def optimize_schedule(tasks, project_start, hours_per_day, min_duration_percentage, max_duration_percentage, avoid_overallocation=True): 
    model = Model(name="Project_Schedule_Optimization")
    
    start_times   = {}
    finish_times  = {}
    duration_vars = {}

    MINUTES_IN_HOUR = 60
    MINUTES_IN_DAY  = hours_per_day * MINUTES_IN_HOUR

    for task in tasks: 
        task_id          = task['ID']
        duration_seconds = float(task['Duration'])  
        duration_days    = duration_seconds / MINUTES_IN_DAY  

        start_times[task_id]   = model.continuous_var(name=f"start_{task_id}")
        duration_vars[task_id] = model.continuous_var(lb=duration_days * min_duration_percentage,
                                                      ub=duration_days * max_duration_percentage,
                                                      name=f"duration_{task_id}")
        finish_times[task_id] = start_times[task_id] + duration_vars[task_id]
    
    for task in tasks: 
        task_id = task['ID']
        if task['Predecessors']: 
            predecessor_list = re.split(r'[;,]', task['Predecessors'])
            for predecessor_str in predecessor_list: 
                predecessor_id, relationship_type, lead_lag_days = parse_predecessor(predecessor_str)
                lead_lag_days = lead_lag_days / MINUTES_IN_DAY

                if relationship_type == 'FS':  
                    model.add_constraint(start_times[task_id] >= finish_times[predecessor_id] + lead_lag_days)
                elif relationship_type == 'SS':  
                    model.add_constraint(start_times[task_id] >= start_times[predecessor_id] + lead_lag_days)
                elif relationship_type == 'FF':  
                    model.add_constraint(finish_times[task_id] >= finish_times[predecessor_id] + lead_lag_days)
                elif relationship_type == 'SF':  
                    model.add_constraint(finish_times[task_id] >= start_times[predecessor_id] + lead_lag_days)

    # Resource over-allocation constraints
    if avoid_overallocation:
        for task in tasks:
            if 'Resources' in task and task['Resources']:  # Check if the task has resources
                resource_count = task['Resources'].Count  # Example: using the MS Project resources count
                # Add logic to prevent over-allocation based on available resources
                # Example: This is where you would add constraints for resource usage based on project limits
                # For now, we'll simulate a constraint on the maximum number of resources:
                model.add_constraint(resource_count <= task['MaxResourceLimit'])  # Example constraint
    
    first_task_id = tasks[0]['ID']
    last_task_id = tasks[-1]['ID']
    project_span = finish_times[last_task_id] - start_times[first_task_id]
    model.minimize(project_span)

    solution = model.solve()

    optimized_schedule = {}
    for task in tasks:
        task_id = task['ID']
        optimized_schedule[task_id] = {
            'Start': solution.get_value(start_times[task_id]),
            'Finish': solution.get_value(finish_times[task_id]),
            'Duration': solution.get_value(duration_vars[task_id])
        }
    
    return optimized_schedule
