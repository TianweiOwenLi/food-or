import csv

def read_food(filename):
  """
  Reads in the food.csv file
  """
  with open(filename) as f:
    reader = csv.reader(f, delimiter=',')
    rowcount = 0
    for row in reader:
      if rowcount == 1125:
        print(row)
      rowcount += 1

  return rowcount
    