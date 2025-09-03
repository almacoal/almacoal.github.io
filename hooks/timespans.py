from datetime import datetime
import re

DATE_FORMAT = '%Y-%m-%d'
placeholder = '<br/>(On-going)'
debug_ph = '<br/>(Debugging)'

date_dict = {
    # On-going roles
    "Mar'25": '2025-03-05', # NOS
    "Oct'24": '2024-10-21', # Azure Tech-Owner
    "May'23": '2023-05-08', # WireIT + INW
    # Career start
    "Jul'15": '2015-07-13'
}

def get_ongoing_timespan(start_date, debugging=False, only_years=False):
    start = datetime.strptime(start_date, DATE_FORMAT)
    end = datetime.today()
    ref = datetime(2000, 1, 1)

    start_days = (start - ref).days
    end_days = (end - ref).days
    diff = end_days - start_days
    yr_diff = diff // 365
    mo_diff = round((diff % 365) / 30 * 2) / 2
    mo_str = f"{mo_diff:g}mo"
    yr_str = f"{yr_diff}yr" if yr_diff > 0 else ""
    diff_str = f"{yr_str} {mo_str}".strip()
    # print(f"aadbg> Start: {start}, End: {end}, Diff: {yr_str}{mo_str}")

    if only_years:
        diff_str = str(yr_diff) + ('.5' if mo_diff >= 6 else '') + ' years'
    if debugging:
        diff_str += '<br/>`[{start} - {end} = {year_diff}yr {month_diff}mo]`'.format(
            start=start.strftime(DATE_FORMAT),
            end=end.strftime(DATE_FORMAT),
            year_diff=yr_diff,
            month_diff=mo_diff
        )
    return diff_str

def replace_dict_dates(markdown):
    new_markdown = markdown
    for key in date_dict:
        if key == "Jul'15": # Career start
            from_str = key + placeholder.replace('<br/>', ' ')
            to_str = get_ongoing_timespan(date_dict[key], only_years=True)
        elif placeholder in new_markdown:
            from_str = key + placeholder
            to_str = key + ' :material-timer: ' + get_ongoing_timespan(date_dict[key])
        elif debug_ph in new_markdown:
            from_str = key + debug_ph
            to_str = key + ' :material-timer: ' + get_ongoing_timespan(date_dict[key], debugging=True)
        else:
            from_str = ""
            to_str = ""
        new_markdown = new_markdown.replace(from_str, to_str)
    return new_markdown

def on_page_markdown(markdown, **kwargs):
    return replace_dict_dates(markdown).replace('today()', datetime.today().strftime(DATE_FORMAT))

def on_pre_build(**kwargs):
    timeline_path = './docs/timeline.yaml'
    with open(timeline_path, 'r', encoding='utf-8') as f:
        timeline_content = f.read()
        today_str = datetime.today().strftime(DATE_FORMAT)
        match = re.search(r"^define: &today ([^\n]*)", timeline_content, flags=re.MULTILINE)
        if match and match.group(1).strip() == today_str:
            return  # Already up to date, skip writing
    timeline_content = re.sub(
        r"^define: &today [^\n]*",
        f"define: &today {datetime.today().strftime(DATE_FORMAT)}",
        timeline_content,
        flags=re.MULTILINE
    )
    with open(timeline_path, 'w', encoding='utf-8') as f:
        f.write(timeline_content)
