from pyomo.environ import *

model = AbstractModel()

R_p = NonNegativeReals

# TODO: consider food expiration date

model.Foods, model.Nutrients = Set(), Set()

model.abstract_cost = Param(model.Foods, within=R_p)
model.nut_amount = Param(model.Foods, model.Nutrients, within=R_p)

model.nut_min = Param(model.Nutrients, within=R_p, default=0.0)
model.nut_max = Param(model.Nutrients, within=R_p, detault=float('inf'))

model.portion = Param(model.Foods, within=R_p)

def abstract_cost_rule(model):
  return sum(model.abstract_cost[i] * model.x[i] for i in model.Foods)
model.cost = Objective(rule=abstract_cost_rule)

def nutrient_rule(model, n):
  return inequality(
    model.nut_min[n], 
    sum(model.nut_amount[f][n] * model.portion[f] for f in model.Foods),  
    model.nut_max[n]
  )