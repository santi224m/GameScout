import bbcode

class BBParser:
  """Holds our custom implementation of BBParser"""
  def __init__(self) -> None:
    self.parser = bbcode.Parser()
    self.parser.add_simple_formatter('h1', '<h1>%(value)s</h1>')
    self.parser.add_simple_formatter('h2', '<h2>%(value)s</h2>')
    self.parser.add_simple_formatter('h3', '<h3>%(value)s</h3>')
    self.parser.add_formatter('noparse', self._render_noparse, strip=True, swallow_trailing_newline=True, render_embedded=False)
    self.parser.add_simple_formatter('spoiler', '<span class="spoiler">%(value)s</span>')
    self.parser.add_simple_formatter('olist', '<ol>%(value)s</ol>')
    self.parser.add_simple_formatter('strike', '<s>%(value)s</s>')
    self.parser.add_formatter('*', self._render_list_item, newline_closes=True, tranform_newlines=False, same_tag_closes=True, strip=True)
    self.parser.add_formatter('quote', self._render_quote, strip=True, swallow_trailing_newline=True)
    self.parser.add_simple_formatter('table', '<table>%(value)s</table>')
    self.parser.add_formatter('th', self._render_table_header, strip=True, swallow_trailing_newline=True)
    self.parser.add_formatter('tr', self._render_table_row, strip=True, swallow_trailing_newline=True)
    self.parser.add_formatter('td', self._render_table_data, strip=True, swallow_trailing_newline=True)
    self.parser.add_formatter('code', self._render_code, strip=False)

  def get_parser(self) -> bbcode.Parser:
    """Returns the parser"""
    return self.parser
  
  def format_text(self, text: str) -> str:
    """Returnes HTML formated text from BBCode"""
    return self.parser.format(text)
  
  def _render_code(self, name, value, options, parent, context): return '<code>%s</code>' % value

  def _render_noparse(self, name, value, options, parent, context): return '<span>%s</span>' % value

  def _render_list_item(self, name, value, options, parent, context):
    if not parent or (parent.tag_name != "list" and parent.tag_name != "olist"):
        return "[*]%s<br />" % value
    return "<li>%s</li>" % value

  def _render_quote(self, name, value, options, parent, context):
      author = ''
      # [quote author=Somebody]
      if 'author' in options:
          author = options['author']
      # [quote=Somebody]
      elif 'quote' in options:
          author = options['quote']
          author = author.split(";")[0]
      # [quote Somebody]
      elif len(options) == 1:
          key, val = list(options.items())[0]
          if val:
              author = val
          elif key:
              author = key
      # [quote Firstname Lastname]
      elif options:
          author = ' '.join([k for k in options.keys()])
      extra = '<small>Originally posted by %s:</small>' % author if author else ''
      return '<blockquote>%s<p>%s</p></blockquote>' % (extra, value)

  def _render_table_header(self, name, value, options, parent, context):
     if not parent or parent.tag_name != "table": return value
     return "<th>%s</th>" % value
  
  def _render_table_row(self, name, value, options, parent, context):
     if not parent or parent.tag_name != "table": return value
     return "<th>%s</th>" % value
  
  def _render_table_data(self, name, value, options, parent, context):
     if not parent or parent.tag_name != "table": return value
     return "<td>%s</td>" % value