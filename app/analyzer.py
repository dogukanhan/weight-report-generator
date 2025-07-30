import app.chart as chart
import re
import unicodedata

from datetime import datetime
from dateutil.relativedelta import relativedelta


def analyze_date(df, dates):
    list = []
    for date in dates:
        list.append(analyze_each_day(df, date))
    
    return list

def analyze(df, types):
    list = []
    for type in types:
        list.append(analyze_type(df, type))
    
    return list

def make_it_url(name):
    text = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    
    # Replace all whitespace with hyphens
    text = re.sub(r'\s+', '-', text)
    
    # Remove any remaining non-word characters (optional)
    text = re.sub(r'[^\w\-]', '', text)

    return text

def analyze_each_day(df, date):
    result = { }
    data = df[df['Date'] == date]
    result["name"] = str(date)
    result["url"] = make_it_url(str(date))
    result["data"] = data
    result["typeWeightChart"] = chart.date_type_weight_chart(data)

    return result

def analyze_type(df, type):
    result = { }
    data = df[df['Type'] == type]
    result["name"] = type
    result["url"] = make_it_url(type)
    result["data"] = data
    result["maxWeightRow"] = df.iloc[data['Weight'].idxmax()]
    result["maxWorkRow"] = df.iloc[data['Work'].idxmax()]
    result["oneRmData"] = find_1rm_record(data)
    result["rms"] = None 
    result["bumbleChart"] = chart.type_bumble_chart(data)
    result["failChart"] = chart.type_fail_chart(data[data['Missing']>0])
    result["chartTrainingDays"] = chart.type_training_days(data)
    result["rpeChart"] = chart.type_rpe_chart(data)
    result["lastRow"] = data.sort_values('Date', ascending=True).iloc[-1]
    if(result["oneRmData"] is not  None):
        result["oneRm"] = calcualte_1rm(result["oneRmData"])
        today = datetime.today().date()
        one_month_ago = today - relativedelta(months=1)
        is_recent =  result["oneRmData"]["Date"] >= one_month_ago
        result["oneRmDataRecent"] = is_recent

        rms = {}
        rms[1] = result["oneRm"] 
        for i in range(2,12):
            rms[i] = round(calculate_nrm(result['oneRm'], i),1)

        result["rms"] = rms 

    result["analysisChart"] = chart.type_analysis_chart(data.sort_values('Date', ascending=False).head(1), result)
    return result


def find_1rm_record(df):
    
    filtered_df = df[
        (df['Set'] == 1) & 
        (df['Repetition'] <= 12) & 
        (df['RPE'] == 10)
    ].sort_values('Date', ascending=False)

    if not filtered_df.empty:
        latest_record = filtered_df.iloc[0]
        return latest_record


def calcualte_1rm(record):
    weight = record['Weight']
    repetition = record['Repetition']
    return weight * (1 + (repetition / 30))

def calculate_nrm(one_rm, n):
    return one_rm / (1 + (n - 1) / 30)