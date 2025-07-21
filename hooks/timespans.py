from datetime import datetime
import math

date_dict = {
    "Jul'15": '2015-07-13',
    "Mar'25": '2025-03-05',
    "Oct'24": '2024-10-21',
    "May'23": '2023-05-08'
}
placeholder = '<br/>(On-going)'
debug_ph = '<br/>(Debugging)'

def get_timespan(start_date, debugging=False, only_years=False):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.today()
    diff = (end.year - start.year) * 12 + (end.month - start.month)
    yr_diff = math.floor(diff / 12)
    mo_diff = diff - yr_diff * 12 + (.5 if end.day - start.day > 15 else 0)

    temp = start.replace(year=start.year + yr_diff)
    month_temp = temp.month + mo_diff
    year_temp = int(temp.year + (month_temp - 1) // 12)
    month_temp = int((month_temp - 1) % 12 + 1)
    temp = temp.replace(year=year_temp, month=month_temp)
    day_diff = (end - temp).days + 1

    day_str = '.5' if -15 < day_diff < 0 else ''
    mo_str = str(mo_diff) + day_str + 'mo'
    yr_str = str(yr_diff) + 'yr ' + mo_str

    if not only_years:
        diff_str = mo_str if yr_diff <= 0 else yr_str
    else:
        diff_str = str(yr_diff) + ('.5' if mo_diff >= 6 else '') + ' years'

    if debugging:
        diff_str += '<br/>`[{start} - {end} = {year_diff}yr {month_diff}mo {day_diff}d]`'.format(
            start=start.strftime('%Y-%m-%d'),
            end=end.strftime('%Y-%m-%d'),
            year_diff=yr_diff,
            month_diff=mo_diff,
            day_diff=day_diff
        )
    return diff_str

def replace_dict(markdown):
    new_markdown = markdown
    for key in date_dict:
        if key == "Jul'15":
            from_str = key + placeholder.replace('<br/>', ' ')
            to_str = get_timespan(date_dict[key], only_years=True)
        elif placeholder in new_markdown:
            from_str = key + placeholder
            to_str = key + '<br/>(' + get_timespan(date_dict[key]) + ')'
        elif debug_ph in new_markdown:
            from_str = key + debug_ph
            to_str = key + '<br/>(' + get_timespan(date_dict[key], debugging=True) + ')'
        new_markdown = new_markdown.replace(from_str, to_str)
    return new_markdown

def on_page_markdown(markdown, **kwargs):
    return replace_dict(markdown)
