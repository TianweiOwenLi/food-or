import csv


def get_name_id_map(filename):
  """
  Obtains a name to ID map from `food.csv`
  """
  with open(filename) as f:
    reader = csv.reader(f, delimiter=',')
    name_id_map = {}
    is_fst_row = True
    for row in reader:
      if is_fst_row:
        is_fst_row = False
        FDC_ID_IDX, NAME_IDX = row.index('fdc_id'), row.index('description')
      name, fdc_id = row[NAME_IDX], row[FDC_ID_IDX]
      if name not in name_id_map:
        name_id_map[name] = []
      name_id_map[name].append(fdc_id)

  return name_id_map
    

def extract_foundation(filename):
  """
  Extracts foundational food from `food.csv`
  """

  fnd_rows = []
  with open(filename) as f:
    reader = csv.reader(f, delimiter=',')
    is_fst_row = True
    for row in reader:
      if is_fst_row:
        is_fst_row = False
        DT_IDX, head_row = row.index('data_type'), row
      if row[DT_IDX] == 'foundation_food':
        fnd_rows.append(row)
  
  with open("extracted_foundation.csv", 'w') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(head_row)
    for row in fnd_rows:
      writer.writerow(row)

      
