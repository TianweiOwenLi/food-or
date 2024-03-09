import pyomo.environ as pe


def create_and_solve(filename: str) -> tuple[float, dict[str, int]]:
  """
  Constructs and solves MILP model using given data; returns non-zero foods 
  and their integer quantities as a dictionary.
  """

  R_p, infty = pe.NonNegativeReals, float('inf')

  model = pe.AbstractModel()

  model.Foods, model.Nutrients = pe.Set(), pe.Set()

  model.qtys = pe.Var(model.Foods, within=pe.NonNegativeIntegers, initialize=0)

  model.price = pe.Param(model.Foods, within=R_p, default=infty)
  model.amount = pe.Param(model.Foods, model.Nutrients, within=R_p, default=0.0)
  model.nmin = pe.Param(model.Nutrients, within=R_p, default=0.0)
  model.nmax = pe.Param(model.Nutrients, within=R_p, default=infty)

  def abstract_cost_rule(model):
    return sum(model.price[i] * model.qtys[i] for i in model.Foods)
  model.cost = pe.Objective(rule=abstract_cost_rule)

  def nutrient_rule(model, nutrient):
    value = sum(model.amount[f,nutrient] * model.qtys[f] for f in model.Foods)
    return pe.inequality(model.nmin[nutrient], value, model.nmax[nutrient])
  model.nutrient_limit = pe.Constraint(model.Nutrients, rule=nutrient_rule)

  data = pe.DataPortal()
  data.load(filename)
  instance = model.create_instance(data)

  solver = pe.SolverFactory('scip')
  solver.solve(instance)

  ret = {}
  for idx in instance.qtys:
    qty = round(pe.value(instance.qtys[idx]))
    if qty:
      ret[idx] = qty
  return (pe.value(instance.cost), ret)

