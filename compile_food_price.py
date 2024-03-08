import pickle

def rm_last_words(s: str, ct: int) -> str:
  """
  Remove last `ct` words of a string
  """
  return ' '.join(s.split(' ')[:-ct])


def process_qty(qty: str) -> tuple[float, str] | None:
  """
  Processes a string denoting a quantity. Returns `None` if not processable.
  """
  new_qty = str(qty)

  if not qty:
    new_qty = '1 ct'
  if new_qty.startswith('per'):
    new_qty = new_qty.replace('per', '1')
  if new_qty.startswith('About'):
    new_qty = ''.join(new_qty.split(' ')[1:3])
  if new_qty.endswith('each'):
    new_qty = new_qty.replace('each', 'ct')
  if new_qty.endswith(('Container', 'container', 'bag', 'jar', 'box', 'bunch')):
    new_qty = rm_last_words(new_qty, 1)
  if new_qty.endswith('options'):
    new_qty = rm_last_words(new_qty, 3)

  new_qty = new_qty.replace("fl oz", "floz")
  new_qty = new_qty.replace('pint', 'pt')
  new_qty = new_qty.replace('count', 'ct')
  new_qty = new_qty.replace('sq ft', 'sqft')

  # perform quantity multiplication
  if ' x ' in new_qty:
    segs = new_qty.split(' ')
    mult_idx = segs.index('x')
    lhs, rhs = segs[mult_idx-1], segs[mult_idx+1]
    amount = float(lhs) * float(rhs)
    segs[mult_idx-1:mult_idx+2] = [f'{amount}']
    new_qty = ' '.join(segs)


  l = new_qty.split(' ')
  if len(l) == 1:
    # add space between number and unit
    idx = 0
    while new_qty[idx] == '.' or new_qty[idx].isnumeric():
      idx += 1
    new_qty = new_qty[:idx] + ' ' + new_qty[idx:]
  elif len(l) != 2:
    assert(False and f"Failed to parse {qty}")

  amount, unit = new_qty.split(' ')
  amount = float(amount)
  
  if unit in {'floz', 'lb', 'pt', 'sticks', 'in', 'gal', 'oz', 'L', 'ct', 'g'}:
    return (amount, unit)
  return None
  


with open('items_raw.pkl', 'rb') as f:
  l = pickle.load(f)

food_item_dict = {}
for line in l:
  name, price, qty, meat_part = None, None, None, None
  bad = False
  for word in line.split('\n'):
    word: str = word.strip()
    if word in ['Leg', 'Thigh', 'Ribs', 'Roast', 'Chops', 'Breast', 'Sirloin', 
                'Round Steak', 'Wing', 'Skirt Steak', 'Strip Steak', 'Whole']:
      meat_part = word
    elif price and '$' in word:
      # ill-formatted price, skip
      continue
    elif word in ['each (est.)', '/pkg (est.)']:
      # redundant unit, skip
      continue
    elif word in ['Many in stock', 'Likely out of stock', 'Best seller', 
                  'Buy it again']:
      # keywords, skip
      continue
    elif word in ['Gluten-Free', 'Whole Grain', 'Organic', 'Vegan', 'Keto', 
                  'Non-GMO', 'Low Fat', 'Zero Sugar', 'Multigrain', 
                  'Zero Calories', 'Sodium-Free', 'Unsweetened']:
      # food traits, skip
      continue
    elif word in ['Grass-Fed', 'Cage-Free', 'Free Range', 'Pasture-Raised']:
      # animal traits, skip
      continue
    elif word in ['Cow Milk', 'Goat Milk']:
      # cheese traits, skip
      continue
    elif word.startswith('Serves '):
      # redundant unit again, skip
      continue
    elif word in ['●']:
      # useless words, skip
      continue
    elif (not price) and '$' in word and '.' in word:
      price = float(word[1:])
    elif (not name) and price and '(est.)' not in word and '$' not in word:
      name = word
    elif (not qty) and (word.startswith(('About', 'per')) or word[0].isnumeric()):
      qty = word
    else:
      assert(False and 'Unreachable')

  assert(name and price)

  if (name) and (meat_part) and meat_part not in name:
    name += (f' ({meat_part})')

  # only handle known quantities
  if (processed_qty := process_qty(qty)):
    d = {'price': price, 'qty': processed_qty}
    if meat_part:
      d['meat_part'] = meat_part
    food_item_dict[name] = d
      
  else:
    print(f"Rejected invalid quantity: {qty}")


with open('food_item_dict.pkl', 'wb') as f:
  pickle.dump(food_item_dict, f)



