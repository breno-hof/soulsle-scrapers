import re

EMPTY_VALUES = ["", "-", "--", "n/a", "none", "?"]

def sanitize_values(values, bad_values = []):
  return [sanitize_value(item, bad_values) for item in values if item.strip() and item not in bad_values]

def sanitize_value(value, bad_values = []):
  for bad_value in bad_values:
    value = value.replace(bad_value, '')

  return value.strip()

def loop_selectors(html, selectors):
  for selector in selectors:
    values = html.css(selector).getall()
    values = [item.strip() for item in values if item.strip()]

    if values != []:
      break

  return values

def clean_text(selector):
  return ' '.join(text.strip() for text in selector.css('::text').getall() if text.strip())

def dedupe(values):
  seen = set()
  return [value for value in values if not (value.lower() in seen or seen.add(value.lower()))]

def cell_values(cell, bad_values = []):
  # Prefer link texts (skipping image links); fall back to the cell's text split on , and /
  values = [text.strip() for text in cell.css('a:not(.mw-file-description)::text').getall()]
  values = [value for value in values if value.lower() not in EMPTY_VALUES]

  if values == []:
    for text in cell.css('::text').getall():
      values += re.split(r'[,/]', text)

  values = sanitize_values(values, bad_values)
  return dedupe([value for value in values if value.lower() not in EMPTY_VALUES])

def infobox_fields(table):
  # Maps lowercased labels to their value cell. Handles both "label | value" rows
  # and a row of labels followed by a row of values in the same columns.
  fields = {}
  rows = table.css('tr')

  for index, row in enumerate(rows):
    cells = row.xpath('./th|./td')
    labels = [clean_text(cell).lower() for cell in cells]

    if len(cells) == 2 and labels[0] and labels[1]:
      fields.setdefault(labels[0], cells[1])
    elif index + 1 < len(rows):
      next_cells = rows[index + 1].xpath('./th|./td')

      for column, label in enumerate(labels):
        if label and column < len(next_cells):
          fields.setdefault(label, next_cells[column])

  return fields

def field_values(fields, labels, bad_values = []):
  for label in labels:
    if label in fields:
      values = cell_values(fields[label], bad_values)

      if values != []:
        return values

  return []

def table_records(table):
  # Yields one {header: cell} dict per data row, keyed by the lowercased header text
  rows = table.css('tr')

  if rows == []:
    return

  headers = [clean_text(cell).lower() for cell in rows[0].xpath('./th|./td')]

  for row in rows[1:]:
    cells = row.xpath('./td')

    if len(cells) == len(headers):
      yield dict(zip(headers, cells))
