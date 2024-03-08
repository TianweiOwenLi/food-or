from pyomo.environ import *

model = AbstractModel()

R_p = NonNegativeReals

model.Foods, model.Nutrients = Set(), Set()

model.qty = Var(model.Foods, within=NonNegativeIntegers)

model.price = Param(model.Foods, within=R_p)
model.nuts = Param(model.Foods, model.Nutrients, within=R_p, default=0.0)

model.nmin = Param(model.Nutrients, within=R_p, default=0.0)
model.nmax = Param(model.Nutrients, within=R_p, default=float('inf'))

def abstract_cost_rule(m):
  return sum(m.price[i] * m.qty[i] for i in m.Foods)
model.cost = Objective(rule=abstract_cost_rule)

def nutrient_rule(m, n):
  return m.nmin[n] <= sum(m.nuts[f][n] for f in m.Foods) <= m.nmax[n]
model.constraint = Constraint(rule=nutrient_rule)

model.Nutrients.construct()