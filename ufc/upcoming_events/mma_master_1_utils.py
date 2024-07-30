def extract_text_safely(soup, *find_args):
  """Extracts text from a BeautifulSoup object using nested find operations.

  Args:
    soup: The BeautifulSoup object.
    *find_args: A list of arguments for successive find operations.

  Returns:
    The extracted text, or None if an error occurs.
  """

  try:
    element = soup
    for arg in find_args:
      element = element.find(*arg)
      if element is None:
        return None
    return element.text.replace("\n", " ").strip()
  except AttributeError:
    return None