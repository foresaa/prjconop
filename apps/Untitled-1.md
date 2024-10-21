# MS Project Specific Optimisation OPL code

## Define parameters

int numTasks; // Number of tasks
range Tasks = 1..numTasks;

## Task data (inputs)

float min_duration[Tasks]; // Minimum allowed duration for each task
float max_duration[Tasks]; // Maximum allowed duration for each task
float predecessors[Tasks]; // Array to represent predecessor relationships
float lead_lag[Tasks]; // Lead/lag time for each task

#### Hours per day

float hours_per_day;

## Decision variables

dvar float start[Tasks];
dvar float duration[Tasks];
dvar float finish[Tasks];

## Objective: minimize the project span

minimize max(finish[t] | t in Tasks) - min(start[t] | t in Tasks);

## Constraints

subject to {

#### Duration bounds: ensure durations are between the minimum and maximum allowed values

forall(t in Tasks) {
duration[t] >= min_duration[t];
duration[t] <= max_duration[t];
}

#### Calculate finish time as start + duration (duration is in days, convert based on hours per day)

forall(t in Tasks) {
finish[t] == start[t] + duration[t];
}

## Predecessor constraints

forall(t in Tasks: predecessors[t] != 0) {
if (predecessors[t] == t) {

#### Finish-to-start constraint (FS)

      start[t] >= finish[predecessors[t]] + lead_lag[t];
    }

#### Add other relationships like SS, FF, SF if applicable

}
}

## Data section example

numTasks = 10;
min_duration = [0.9, 1.1, ...]; // Filled with task-specific data
max_duration = [1.2, 1.5, ...];
predecessors = [0, 1, 0, 2, ...]; // Predecessor task IDs
lead_lag = [0, 1, -2, ...]; // Lead/lag times in days
hours_per_day = 8;
