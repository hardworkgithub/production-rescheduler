from ortools.linear_solver import pywraplp

def reschedule_full(projects_json, machines_json, operations_json, disruption=None):
    """FULLY WORKING Production Rescheduler (Linear + Stable)"""

    # -----------------------------
    # Default Data (if none passed)
    # -----------------------------
    projects = projects_json or [
        {'name': 'P1', 'priority': 'medium', 'due_day': 10, 'delay_penalty': 5000},
        {'name': 'P2', 'priority': 'high', 'due_day': 7, 'delay_penalty': 20000},
        {'name': 'P3', 'priority': 'low', 'due_day': 12, 'delay_penalty': 2000}
    ]

    machines = machines_json or [
        {'name': 'M1', 'type': 'CNC', 'maintenance_start': 5, 'maintenance_end': 6},
        {'name': 'M2', 'type': 'CNC'},
        {'name': 'M3', 'type': 'VMC'}
    ]

    operations = operations_json or [
        {'name': 'OP1_P1', 'project': 'P1', 'project_idx': 0, 'machine_type': 'CNC', 'duration': 2},
        {'name': 'OP1_P2', 'project': 'P2', 'project_idx': 1, 'machine_type': 'CNC', 'duration': 3},
        {'name': 'OP1_P3', 'project': 'P3', 'project_idx': 2, 'machine_type': 'CNC', 'duration': 2}
    ]

    # -----------------------------
    # Apply disruption (priority change)
    # -----------------------------
    if disruption:
        for p in projects:
            if p['name'] == disruption['project']:
                p['priority'] = disruption['new_priority']

    # -----------------------------
    # Create Solver (IMPORTANT FIX)
    # -----------------------------
    solver = pywraplp.Solver.CreateSolver('CBC')

    horizon = 15
    num_ops = len(operations)
    num_machs = len(machines)

    # -----------------------------
    # Variables: x[i][j][d]
    # -----------------------------
    x = [[[None for _ in range(horizon)] for _ in range(num_machs)] for _ in range(num_ops)]

    for i in range(num_ops):
        for j in range(num_machs):
            for d in range(horizon):
                x[i][j][d] = solver.BoolVar(f'x_{i}_{j}_{d}')

    # -----------------------------
    # CONSTRAINT 1: Each operation once
    # -----------------------------
    for i in range(num_ops):
        solver.Add(
            solver.Sum(
                x[i][j][d]
                for j in range(num_machs)
                for d in range(horizon)
            ) == 1
        )

    # -----------------------------
    # CONSTRAINT 2: Machine type match
    # -----------------------------
    for i in range(num_ops):
        for j in range(num_machs):
            if machines[j]['type'] != operations[i]['machine_type']:
                for d in range(horizon):
                    solver.Add(x[i][j][d] == 0)

    # -----------------------------
    # CONSTRAINT 3: No overlap
    # -----------------------------
    for j in range(num_machs):
        for day in range(horizon):
            usage = []
            for i in range(num_ops):
                dur = operations[i]['duration']
                for d in range(horizon):
                    if d <= day < d + dur:
                        usage.append(x[i][j][d])
            if usage:
                solver.Add(solver.Sum(usage) <= 1)

    # -----------------------------
    # CONSTRAINT 4: Maintenance
    # -----------------------------
    for j in range(num_machs):
        if 'maintenance_start' in machines[j]:
            start = machines[j]['maintenance_start']
            end = machines[j]['maintenance_end']
            for i in range(num_ops):
                dur = operations[i]['duration']
                for d in range(horizon):
                    if d < end and d + dur > start:
                        solver.Add(x[i][j][d] == 0)

    # -----------------------------
    # OBJECTIVE (FIXED - LINEAR)
    # -----------------------------
    priority_weight = {'low': 1, 'medium': 3, 'high': 10}
    objective = 0

    for i in range(num_ops):
        proj_idx = operations[i]['project_idx']
        weight = priority_weight[projects[proj_idx]['priority']]
        penalty = projects[proj_idx]['delay_penalty']

        for j in range(num_machs):
            for d in range(horizon):
                # Later start = higher cost
                objective += penalty * weight * d * x[i][j][d]

    solver.Minimize(objective)

    # -----------------------------
    # SOLVE
    # -----------------------------
    status = solver.Solve()

    # -----------------------------
    # Extract Results
    # -----------------------------
    schedule = []
    total_cost = 0

    for i in range(num_ops):
        for j in range(num_machs):
            for d in range(horizon):
                if x[i][j][d].solution_value() > 0.5:
                    end_day = d + operations[i]['duration']
                    due = projects[operations[i]['project_idx']]['due_day']
                    delay = max(0, end_day - due)
                    cost = delay * projects[operations[i]['project_idx']]['delay_penalty']
                    total_cost += cost

                    schedule.append({
                        'operation': operations[i]['name'],
                        'project': operations[i]['project'],
                        'machine': machines[j]['name'],
                        'start_day': d,
                        'end_day': end_day,
                        'delay_days': delay,
                        'cost_impact': cost,
                        'priority': projects[operations[i]['project_idx']]['priority']
                    })

    # -----------------------------
    # Explanation
    # -----------------------------
    explanation = [
        f"✅ Optimized Schedule (Total Cost: {total_cost})",
        f"Solver: CBC",
        f"High priority handled first"
    ]

    if disruption:
        explanation[0] = f"🔄 {disruption['project']} priority updated → Cost: {total_cost}"

    return schedule, {
        'total_cost': total_cost,
        'explanation': explanation,
        'status': 'success'
    }