from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timedelta
import calendar

app = FastAPI(title="Numerology API", version="1.0")

PLANETARY_MAP = {
    1: ("Sun", 1),
    2: ("Moon", 2),
    3: ("Jupiter", 3),
    4: ("Rahu", 4),
    5: ("Mercury", 5),
    6: ("Venus", 6),
    7: ("Ketu", 7),
    8: ("Saturn", 8),
    9: ("Mars", 9)
}

DAY_MAPPING = {
    "Sunday": 1,
    "Monday": 2,
    "Tuesday": 9,
    "Wednesday": 5,
    "Thursday": 3,
    "Friday": 6,
    "Saturday": 8
}

def validate_dob(dob_str: str) -> datetime:
    try:
        dob = datetime.strptime(dob_str, "%d-%m-%Y")
        if dob.year < 1900 or dob.year > 2100:
            raise ValueError
        return dob
    except ValueError:
        raise HTTPException(status_code=400, detail="Provide valid DOB in DD-MM-YYYY.")

def reduce_to_single_digit(num: int, ignore_zero=False) -> int:
    while num >= 10:
        digits = [int(d) for d in str(num) if not (ignore_zero and d == '0')]
        num = sum(digits)
    return num

def get_basic_number(dob: datetime) -> int:
    dd_digits = [int(d) for d in str(dob.day) if d != '0']
    return reduce_to_single_digit(sum(dd_digits), ignore_zero=True)

def get_destiny_number(dob: datetime) -> int:
    all_digits = [int(d) for d in dob.strftime("%d%m%Y")]
    return reduce_to_single_digit(sum(all_digits))

def get_numerology_grid(dob: datetime, basic_num: int, destiny_num: int) -> dict:
    yy = dob.year % 100
    digits = [int(d) for d in f"{dob.day:02}{dob.month:02}{yy:02}" if d != 0]
    grid_digits = digits.copy()
    grid_digits.append(destiny_num)
    if dob.day > 10 and dob.day not in (20, 30):
        grid_digits.append(basic_num)
    return {i: grid_digits.count(i) for i in range(1, 10)}

def get_mahadasha_sequence(basic_num: int, birth_year: int, end_year: int):
    seq = []
    current_num = basic_num
    year_pointer = birth_year
    while year_pointer <= end_year:
        planet, duration = PLANETARY_MAP[current_num]
        seq.append({"MD_Number": current_num, "Planet": planet, "Start_Year": year_pointer, "End_Year": year_pointer + duration})
        year_pointer += duration
        current_num = current_num + 1 if current_num < 9 else 1
    return seq

def get_antardasha_year(year: int, dob: datetime, basic_num: int) -> int:
    yy_reduced = reduce_to_single_digit(year % 100)
    mm_reduced = reduce_to_single_digit(dob.month)
    weekday_name = calendar.day_name[datetime(year, dob.month, dob.day).weekday()]
    day_num = DAY_MAPPING[weekday_name]
    total = yy_reduced + basic_num + mm_reduced + day_num
    return reduce_to_single_digit(total)

def get_monthly_dasha(ad_year_num: int, dob: datetime, year: int):
    seq = []
    start_date = datetime(year, dob.month, dob.day)
    current_num = ad_year_num
    for _ in range(9):
        days = current_num * 8
        end_date = start_date + timedelta(days=days)
        seq.append({
            "Start_Number": current_num,
            "Days": days,
            "Start_Date": start_date.strftime("%d-%b"),
            "End_Date": end_date.strftime("%d-%b")
        })
        start_date = end_date
        current_num = current_num + 1 if current_num < 9 else 1
    return seq

def get_day_lord(date: datetime, month_num: int) -> dict:
    weekday_name = calendar.day_name[date.weekday()]
    day_lord_num = DAY_MAPPING[weekday_name]
    day_number = reduce_to_single_digit(day_lord_num + month_num)
    return {
        "Date": date.strftime("%d-%b-%Y"),
        "Day_Lord": day_lord_num,
        "Month_Number": month_num,
        "Day_Number": day_number
    }

# Existing full package endpoint
@app.get("/numerology")
def numerology(dob: str = Query(...), year: int = Query(...)):
    dob_obj = validate_dob(dob)
    basic_num = get_basic_number(dob_obj)
    destiny_num = get_destiny_number(dob_obj)
    grid = get_numerology_grid(dob_obj, basic_num, destiny_num)
    md_seq = get_mahadasha_sequence(basic_num, dob_obj.year, 2030)
    ad_year_num = get_antardasha_year(year, dob_obj, basic_num)
    monthly_seq = get_monthly_dasha(ad_year_num, dob_obj, year)
    return {
        "Basic_Number": basic_num,
        "Destiny_Number": destiny_num,
        "Numerology_Grid": grid,
        "Mahadasha_Sequence": md_seq,
        "Antardasha_Year_Number": ad_year_num,
        "Monthly_Dasha": monthly_seq
    }

# New modular endpoints
@app.get("/basic-number")
def basic_number(dob: str = Query(...)):
    dob_obj = validate_dob(dob)
    basic_num = get_basic_number(dob_obj)
    grid = get_numerology_grid(dob_obj, basic_num, get_destiny_number(dob_obj))
    return {"Basic_Number": basic_num}

@app.get("/destiny-number")
def destiny_number(dob: str = Query(...)):
    dob_obj = validate_dob(dob)
    destiny_num = get_destiny_number(dob_obj)
    grid = get_numerology_grid(dob_obj, get_basic_number(dob_obj), destiny_num)
    return {"Destiny_Number": destiny_num}

@app.get("/grid")
def numerology_grid(dob: str = Query(...)):
    dob_obj = validate_dob(dob)
    grid = get_numerology_grid(dob_obj, get_basic_number(dob_obj), get_destiny_number(dob_obj))
    return {"Grid": grid}

@app.get("/mahadasha")
def mahadasha(dob: str = Query(...)):
    dob_obj = validate_dob(dob)
    basic_num = get_basic_number(dob_obj)
    seq = get_mahadasha_sequence(basic_num, dob_obj.year, 2030)
    grid = get_numerology_grid(dob_obj, basic_num, get_destiny_number(dob_obj))
    return {"Mahadasha": seq, "Grid": grid}

@app.get("/antardasha")
def antardasha(dob: str = Query(...), year: int = Query(...)):
    dob_obj = validate_dob(dob)
    basic_num = get_basic_number(dob_obj)
    ad_year_num = get_antardasha_year(year, dob_obj, basic_num)
    grid = get_numerology_grid(dob_obj, basic_num, get_destiny_number(dob_obj))
    return {"Antardasha_Year_Number": ad_year_num, "Grid": grid}

@app.get("/monthly-dasha")
def monthly_dasha(dob: str = Query(...), year: int = Query(...)):
    dob_obj = validate_dob(dob)
    basic_num = get_basic_number(dob_obj)
    ad_year_num = get_antardasha_year(year, dob_obj, basic_num)
    monthly_seq = get_monthly_dasha(ad_year_num, dob_obj, year)
    grid = get_numerology_grid(dob_obj, basic_num, get_destiny_number(dob_obj))
    return {"Monthly_Dasha": monthly_seq, "Grid": grid}

@app.get("/day-dasha")
def day_dasha(dob: str = Query(...), date: str = Query(...), month_num: int = Query(...)):
    dob_obj = validate_dob(dob)
    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Provide valid date in DD-MM-YYYY.")
    day_lord_info = get_day_lord(date_obj, month_num)
    grid = get_numerology_grid(dob_obj, get_basic_number(dob_obj), get_destiny_number(dob_obj))
    return {"Day_Dasha": day_lord_info, "Grid": grid}
