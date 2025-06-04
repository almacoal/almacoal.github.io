from datetime import datetime
import math

date_dict = {
    "Mar'25": "2025-03-05",
    "Oct'24": "2024-10-21",
    "May'23": "2023-05-08"
}
placeholder = "<br/>(On-going)"

def get_timespan(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.today()
    diff = (end.year - start.year) * 12 + (end.month - start.month)
    yr_diff = math.floor(diff / 12)
    mo_diff = diff - yr_diff * 12 + (.5 if end.day - start.day > 15 else 0)

    temp = start.replace(year=start.year + yr_diff)
    month_temp = temp.month + mo_diff
    year_temp = temp.year + (month_temp - 1) // 12
    month_temp = (month_temp - 1) % 12 + 1
    temp = temp.replace(year=year_temp, month=month_temp)
    day_diff = (end - temp).days

    day_str = '.5' if -15 < day_diff < 0 else ''
    mo_str = str(mo_diff) + day_str + "mo"
    yr_str = str(yr_diff) + "yr " + mo_str
    diff_str = mo_str if yr_diff <= 0 else yr_str
    return diff_str

def replace_dict(markdown):
    new_markdown = markdown
    for key in date_dict:
        from_str = key + placeholder
        to_str = key + '<br/>(' + get_timespan(date_dict[key]) + ')'
        new_markdown = new_markdown.replace(from_str, to_str)
    return new_markdown

def on_page_markdown(markdown, **kwargs):
    return replace_dict(markdown)
