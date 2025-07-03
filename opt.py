import pulp as pl

# 1. Define the Business Problem Parameters

# Product details: (carpentry_hours, finishing_hours, wood_units, profit_per_unit)
product_a = {"name": "Chair A", "carpentry": 2, "finishing": 1, "wood": 0.5, "profit": 20}
product_b = {"name": "Chair B", "carpentry": 1, "finishing": 1.5, "wood": 1, "profit": 15}

# Resource limits
resource_limits = {
    "carpentry_hours": 100,
    "finishing_hours": 80,
    "wood_units": 50
}

print("--- Business Problem Setup ---")
print(f"Product A: Carpentry={product_a['carpentry']}h, Finishing={product_a['finishing']}h, Wood={product_a['wood']} units, Profit=${product_a['profit']}")
print(f"Product B: Carpentry={product_b['carpentry']}h, Finishing={product_b['finishing']}h, Wood={product_b['wood']} units, Profit=${product_b['profit']}")
print(f"Resource Limits: Carpentry={resource_limits['carpentry_hours']}h, Finishing={resource_limits['finishing_hours']}h, Wood={resource_limits['wood_units']} units")
print("-" * 30)

# 2. Formulate the Optimization Problem using PuLP

# Create a LP problem instance
# LpMinimize for minimization, LpMaximize for maximization
prob = pl.LpProblem("Furniture_Production_Planning", pl.LpMaximize)

# Decision Variables:
# x_a = number of Chair A to produce
# x_b = number of Chair B to produce
# Variables must be non-negative integers (cannot produce negative chairs, or fractional chairs)
x_a = pl.LpVariable("Chair_A_Quantity", lowBound=0, cat='Integer')
x_b = pl.LpVariable("Chair_B_Quantity", lowBound=0, cat='Integer')

# Objective Function: Maximize total profit
# Profit = (profit_A * x_a) + (profit_B * x_b)
prob += (product_a["profit"] * x_a) + (product_b["profit"] * x_b), "Total Profit"

# Constraints:
# 1. Carpentry hours constraint
# (carpentry_A * x_a) + (carpentry_B * x_b) <= max_carpentry_hours
prob += (product_a["carpentry"] * x_a) + (product_b["carpentry"] * x_b) <= resource_limits["carpentry_hours"], "Carpentry Hours Constraint"

# 2. Finishing hours constraint
# (finishing_A * x_a) + (finishing_B * x_b) <= max_finishing_hours
prob += (product_a["finishing"] * x_a) + (product_b["finishing"] * x_b) <= resource_limits["finishing_hours"], "Finishing Hours Constraint"

# 3. Wood units constraint
# (wood_A * x_a) + (wood_B * x_b) <= max_wood_units
prob += (product_a["wood"] * x_a) + (product_b["wood"] * x_b) <= resource_limits["wood_units"], "Wood Units Constraint"

print("\n--- Optimization Problem Formulation ---")
print("Objective: Maximize Total Profit")
print("Variables: Chair_A_Quantity (Integer >= 0), Chair_B_Quantity (Integer >= 0)")
print("Constraints:")
for name, constraint in prob.constraints.items():
    print(f"- {name}: {constraint}")
print("-" * 30)

# 3. Solve the Problem

print("\n--- Solving the Optimization Problem ---")
# The problem is solved using the default solver (usually CBC, which comes with PuLP)
prob.solve()

# Check the status of the solution
print(f"Status: {pl.LpStatus[prob.status]}")

# 4. Display the Results

if prob.status == pl.LpStatus.Optimal:
    print("\n--- Optimal Production Plan ---")
    print(f"Produce {x_a.varValue} units of {product_a['name']}")
    print(f"Produce {x_b.varValue} units of {product_b['name']}")
    print(f"Maximum Total Profit: ${pl.value(prob.objective):.2f}")

    print("\n--- Resource Utilization ---")
    # Calculate used resources
    used_carpentry = (product_a["carpentry"] * x_a.varValue) + (product_b["carpentry"] * x_b.varValue)
    used_finishing = (product_a["finishing"] * x_a.varValue) + (product_b["finishing"] * x_b.varValue)
    used_wood = (product_a["wood"] * x_a.varValue) + (product_b["wood"] * x_b.varValue)

    print(f"Carpentry Used: {used_carpentry:.2f} hours (out of {resource_limits['carpentry_hours']}h)")
    print(f"Finishing Used: {used_finishing:.2f} hours (out of {resource_limits['finishing_hours']}h)")
    print(f"Wood Used: {used_wood:.2f} units (out of {resource_limits['wood_units']} units)")

else:
    print("\nNo optimal solution found.")
    print("Possible reasons: Infeasible problem (constraints cannot be satisfied) or unbounded problem.")

