import moodlexml as MX

# Create an empty quiz
quiz = MX.Quiz()

# Create a multichoice question and append to quiz
name = "Multichoice - Exemplo 1"
text = "<p>Qual é a área de um triângulo de base 7 e altura 4?</p>"
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
