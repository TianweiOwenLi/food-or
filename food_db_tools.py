import csv, sqlite3, sys
from pathlib import Path

def mk_food_db(food_csv: str, db_name: str):
  con = sqlite3.connect(db_name + '.db')
  cur = con.cursor()
  stem = Path(food_csv).stem
  cur.execute(f'''CREATE TABLE IF NOT EXISTS {stem} (
              fdc_id INTEGER PRIMARY KEY,
              description TEXT NOT NULL,
              publication_date TEXT)''')

  with open(food_csv, 'r') as f:
    dr = csv.DictReader(f)
    rows = [(
      item['fdc_id'], 
      item['description'], 
      item['publication_date']
    ) for item in dr]

  cur.executemany(f'''INSERT INTO {stem} (
                  fdc_id, description, publication_date
                  ) VALUES (?, ?, ?)''', rows)

  con.commit()
  con.close()


def mk_nutrient_db(nutrient_csv: str, db_name: str):
  con = sqlite3.connect(db_name + '.db')
  cur = con.cursor()
  stem = Path(nutrient_csv).stem
  cur.execute(f'''CREATE TABLE IF NOT EXISTS {stem} (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              unit_name TEXT)''')

  with open(nutrient_csv, 'r') as f:
    dr = csv.DictReader(f)
    rows = [(item['id'], item['name'], item['unit_name']) for item in dr]

  cur.executemany(f'''INSERT INTO {stem} (
                  id, name, unit_name
                  ) VALUES (?, ?, ?)''', rows)

  con.commit()
  con.close()

mk_food_db(sys.argv[1], 'usda')
mk_nutrient_db(sys.argv[2], 'usda')