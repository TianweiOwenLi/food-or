from pyomo.environ import *

model = AbstractModel()

R_p = NonNegativeReals

model.Foods, model.Nutrients = Set(), Set()

model.qty = Var(model.Foods, within=NonNegativeIntegers)

model.price = Param(model.Foods, within=R_p)
model.amount = Param(model.Foods, model.Nutrients, within=R_p, default=0.0)

model.nmin = Param(model.Nutrients, within=R_p, default=0.0)
model.nmax = Param(model.Nutrients, within=R_p, default=float('inf'))

def abstract_cost_rule(model):
  return sum(model.price[i] * model.qty[i] for i in model.Foods)
model.cost = Objective(rule=abstract_cost_rule)

def nutrient_rule(model, nutrient):
  value = sum(model.amount[f,nutrient] * model.qty[f] for f in model.Foods)
  return inequality(model.nmin[nutrient], value, model.nmax[nutrient])
model.nutrient_limit = Constraint(model.Nutrients, rule=nutrient_rule)

data = DataPortal()
data.load(filename='../toy_example.json')
ins = model.create_instance(data)