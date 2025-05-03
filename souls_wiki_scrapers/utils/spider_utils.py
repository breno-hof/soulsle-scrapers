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