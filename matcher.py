import unittest
import re

class CodeMatcher(unittest.TestCase):
  

  def matchSnipped(self, snipped, template, removeLinebreaks: bool = False):
    res, mapping, templateReplaced, reason = CodeMatcher.doMatchSnipped(snipped.strip(), template.strip(),removeLinebreaks)
    if not res:
      mapstr = "with mapping:\n"
      for templ,tVar in mapping.items():
        mapstr += f"\t{templ} -> {tVar}\n"

      if not templateReplaced:
        templateReplaced = "N/A"

      self.fail(f"Mismatch\nFound:    {snipped}\nExpected: {template}\nReplaced: {templateReplaced}\nReason:\t{reason}\n{mapstr}")
      

  @staticmethod
  def doMatchSnipped(snipped, template, removeLinebreaks):
    pattern = re.compile(r"\$t[0-9]+")
    pattern2 = re.compile("t[0-9]+")

    placeholders = pattern.findall(template)
    occurences = pattern2.findall(snipped)

    mapping = {}
    for p,o in zip(placeholders, occurences):
      if p not in mapping:
        mapping[p] = o
      elif p in mapping and mapping[p] != o:
        return False, mapping, "", f"Mapping error: {p} -> {mapping[p]} exists, but {p} -> {o} found"

    # if we get here, the occurences match the templates

    if len(placeholders) != len(occurences):
      return False, mapping, "", f"number of placeholders {len(placeholders)} does not match occurences {len(occurences)}"

    for (k,v) in mapping.items():
      template = template.replace(k,v)

    templateClean = template.replace("\n","").replace(" ","").lower()
    snippedClean = snipped.replace("\n","").replace(" ","").lower()
    
    matches = snippedClean == templateClean

    if not matches:
      print()
      print(snippedClean)
      for i in range(len(snippedClean)):
        if snippedClean[i] != templateClean[i]:
          print("^")
          break

        print(" ",end="")
      print(templateClean)
    return matches, mapping, template, "Snipped does not match template" if not matches else ""
