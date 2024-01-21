import numpy as np

def ineq_num_transform(expr_str, fn):
  """
  Transforms number in some inequality expression (ie. <10, 45-65) using `fn`.
  """
  if expr_str[0] == '<':
    num = float(expr_str[1:])
    return f"<{fn(num)}"
  if '-' in expr_str and expr_str[0] != '-': # handles negative case
    lb, ub = expr_str.split('-')
    lb, ub = float(lb), float(ub)
    return f"{fn(lb)}-{fn(ub)}"


def remove_comma(s):
  """
  Removes comma from string
  """
  return ''.join(s.split(','))


def parse_formatted_goals(filename):
  """
  Transforms formatted goals into some numpy matrix...

  WHY THE GOVERNMENT DIETARY GUIDELINE IS NOT PUT INTO `.csv` FILE?
  """
  with open(filename) as f:
    tags, units, data = [], [], []
    for line in f.readlines():
      left_paren_idx, right_paren_idx = line.index('('), line.index(')')
      tag = line[:left_paren_idx]
      unit = line[left_paren_idx+1:right_paren_idx]
      vec = line[right_paren_idx+1:].strip().split(' ')
      vec = [remove_comma(x) for x in vec]

      assert(len(vec) == 13)
      tags.append(tag)
      units.append(unit)
      data.append(vec)

    tags, units = np.array(tags), np.array(units)
    data = np.array(data)

    tags_and_units = np.vstack((tags, units)).T
    tagged_data = np.hstack((tags_and_units, data))
    print(tagged_data)