import xml.etree.ElementTree as ET
import xml.sax.saxutils as SU
import moodlexml as MX

quiz = MX.Quiz()

c1 = MX.Category("Calculus")
quiz.append(c1)

c2 = MX.Category("Calculus/Integral Calculus")
quiz.append(c2)

name = "Name of question"
text = "<p>Text of question</p>"
a1 = ["100", "<p>Text of answer 1</p>"]
a2 = ["0", "<p>Text of answer 2</p>"]
answers = [a1, a2]
q = MX.Multichoice(name, text, answers)
quiz.append(q)

quiz_str = ET.tostring(quiz, encoding="unicode", xml_declaration=True)
quiz_str = SU.unescape(quiz_str)
print(quiz_str)

text_file = open("output.xml", "w")
text_file.write(quiz_str)
text_file.close()
