import reader as r
import plotly.express as px
import app.chart as chart
import app.analyzer as analyzer
from datetime import datetime
import os
from jinja2 import Environment, PackageLoader, select_autoescape

folder_path = 'report'
report_path = ""

def check_folders():
  if not os.path.exists(folder_path):
      os.makedirs(folder_path)

  global report_path
  report_path = folder_path + "/" + datetime.now().strftime('%Y-%m-%d')

  if not os.path.exists(report_path):
      os.makedirs(report_path)


def inialize_virtual_columns(df):
  df['Date'] = df['Date'].dt.date
  df['WeightNormalized'] = df['Weight'].replace(0, 1)
  df['Work'] = df['WeightNormalized'] * df['Set'] * df['Repetition'] - df['WeightNormalized'] * df['Missing']
  df['Power'] = df['Weight'] * df['Repetition']* df['Set']
  df['Action'] = df['Repetition']* df['Set']
  df.fillna(0, inplace=True)  # replaces all NaNs with 0, modifies df in-place

def generate_index(env, df, now_str, dateList, typeList):
  template = env.get_template("./index.html")
  rendered = template.render(
    date = now_str,
    dates = dateList,
    types = typeList,
    group_by_type=chart.group_by_type(df),
    group_by_date=chart.group_by_date(df))
  
  with open(report_path + "/index.html", "w") as f:
    f.write(rendered)

def generate_type_report(env, df, now_str, dateList, typeList):
  template = env.get_template("./type.html")

  for type in typeList:
        rendered = template.render(
        date = now_str,
        dates = dateList,
        type = type,
        types = typeList,
        group_by_type=chart.group_by_type(df),
        group_by_date=chart.group_by_date(df))
        with open(report_path + "/"+type["url"]+".html", "w") as f:
          f.write(rendered)

def generate_date_report(env, now_str, dateList, typeList):
  
  template = env.get_template("./date.html")

  for day in dateList:
        rendered = template.render(
        date = now_str,
        dates = dateList,
        day = day,
        types = typeList,
        )
        with open(report_path + "/"+day["url"]+".html", "w") as f:
          f.write(rendered)


def generate_report():
  check_folders()

  df = r.read_training_data()
  inialize_virtual_columns(df)

  env = Environment(
      loader=PackageLoader("app", "template"),
      autoescape=select_autoescape()
  )

  types  = df['Type'].unique().tolist()
  dates  = df['Date'].unique().tolist()
  typeList = analyzer.analyze(df,types)
  dateList = analyzer.analyze_date(df, dates)
  now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  generate_index(env, df, now_str, dateList, typeList)
  generate_type_report(env, df, now_str, dateList, typeList)
  generate_date_report(env, now_str, dateList, typeList)



generate_report()
