# Project Optimization `prjconop`

---

This project, `prjconop`, is focused on optimizing task schedules within a Microsoft Project file, while ensuring that dependencies, project calendars, and potential overallocations of resources are respected. The model provides actionable insights into resource requirements and task scheduling, offering users the flexibility to optimize their project plans based on various constraints and conditions.

## Objective

---

The core objective of this project is to optimize task durations and schedules within Microsoft Project files, reducing the overall project span without violating critical constraints such as resource allocations or task dependencies. The model helps users balance the need for speedier project completion with the realities of resource limitations.

### Key Features:

---

- **Predecessor Compliance**: The model respects task predecessors and dependencies, ensuring that start and finish dates adhere to the logical order of tasks.
- **Optimized Task Durations**: Users can specify percentage tolerances for task durations, allowing for flexibility in shortening or lengthening durations to optimize the project.
- **Resource Overallocation Detection**: The model has been extended to detect potential resource overallocations caused by changes in task durations.
- **Configurable Parameters**: Users have the ability to configure parameters such as percentage limits for task duration optimization and tolerances for resource overallocations.
- **Optimization Without Overallocation**: The model can be configured to optimize task durations only if it does not cause resource overallocations, offering users control over the resource impact of their project schedule.

## Workflow and Steps

---

1. **Model Setup**: The model takes input in the form of tasks with associated dependencies, resource assignments, and durations. It uses [IBM's DOcplex](https://ibmdecisionoptimization.github.io/docplex-doc/) to build a mathematical model.
2. **Task Optimization**: The model optimizes tasks, adjusting start dates and durations to minimize overall project span while adhering to dependencies and constraints.
3. **Resource Impact Insights**: During optimization, resource impacts are calculated, giving insight into potential resource shortages or overallocations.
4. **Output to MS Project**: The optimized schedule is then written back to an `.mpp` file, where it can be reviewed and analyzed using Microsoft Project.
5. **Reporting on Resource Overallocations**: Resource overallocations are highlighted in the output, providing users with actionable insights to manage resource distribution across tasks.

## Installation

---

Once `prjconop` is ready, it will be available via [PyPI](https://pypi.org/). You can install it using pip:

```bash
pip install prjconop
```

To import the functionality into your project, you can use:

```python
from prjconop import open_ms_project, run_optimization
```

## Usage

---

- **Optimizing a Project File**: Open an `.mpp` file using the file dialog provided by the script. Once the file is opened, the model will run optimizations based on your settings and constraints. The optimized project will be saved as a new file with the `_opt` suffix.
- **User Parameters**: The user can define the minimum and maximum duration adjustments allowed for each task, along with the acceptable tolerance for resource overallocations. These parameters can be specified at the start of the process.

## OPL Model File

A detailed description of the OPL model used in this project is available [here](https://github.com/foresaa/prjconop/blob/master/docs/OPL_prjconop.md). The OPL file outlines the mathematical formulation and constraints of the optimization problem, providing insights into how task schedules are adjusted while respecting task dependencies and project constraints.

## Future Directions

---

We are continuously improving the model, with upcoming features including:

1. **Resource Balancing**: The ability to adjust resource allocations automatically to avoid overallocation.
2. **Web Interface**: Providing a user-friendly web interface using Dash, allowing users to upload their project files and get optimized schedules without needing to install Python locally.
3. **Educational Tool**: We aim to turn this tool into a resource for learning project management optimization techniques, using Jupyter Notebooks for demonstrations.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. For any questions or suggestions, open a new issue on GitHub.

---
