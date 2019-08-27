import unittest
import re

class CodeMatcher(unittest.TestCase):
  

  def matchSnipped(self, snipped, template):
    res = self.doMatchSnipped(snipped.strip(), template.strip())

    if not res:
      self.fail(f"{snipped} does not match given template {template}")
      

  def doMatchSnipped(self, snipped, template):
    replacements = {}
    pattern = re.compile("\$.?[0-9]")

    pattern2 = re.compile("[A-Z][A-Z][A-Z][A-Z][A-Z]")

    positions = [p.start() - i for i,p in enumerate(pattern.finditer(template))]

    keys = pattern.findall(template)
    offset = 0

    for i,pos in enumerate(positions):
      if len(snipped) < pos + offset + 1:
        return False

      match = pattern2.search(snipped, positions[i] + offset)
      if match:
        snip = match.group(0)
        replacements[keys[i]] = snip
        offset += len(snip) - 1

    s = template
    for k,v in replacements.items():
      s = s.replace(k,v)

    return snipped == s

