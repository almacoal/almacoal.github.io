from datetime import datetime

date_dict = {
    "Mar'25": "2025-03-08",
    "Oct'24": "2024-10-19",
    "May'23": "2023-05-08"
}
placeholder = " (On-going)"

def get_timespan(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.today()
    diff = (end.year - start.year) * 12 + (end.month - start.month)
    return diff + "mo"

def replace_dict(markdown, date):
    new_markdown = markdown
    for key in date_dict:
        from_str = key + placeholder
        to_str = key + ' (' + get_timespan(date_dict[key]) + ')'
        new_markdown = new_markdown.replace(from_str, to_str)
    return new_markdown

def on_page_markdown(markdown, **kwargs):
    return replace_dict()
