import moodlexml as MX

# Create an empty quiz
quiz = MX.Quiz()

# Create a category with name and append to quiz
cat = MX.Category("Multichoice questions")
quiz.append(cat)

# Create multichoice question with name, text, answers. Append to quiz
name = "<p>Example 1 - The simplest multichoice question</p>"
text = "<p>What is the area of a triangle of base 7 and height 4?</p>"
ans1 = ["100", "<p>14</p>"]
ans2 = ["0", "<p>28</p>"]
ans3 = ["0", "<p>11</p>"]
answers = [ans1, ans2, ans3]
question_mc = MX.Multichoice(name, text, answers)
quiz.append(question_mc)

# Print quiz to stdout
print(quiz)

# Write quiz to a file
file_name = "multichoice_1.xml"
text_file = open(file_name, "w")
print(quiz, file=text_file)
text_file.close()
