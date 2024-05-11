import json

sampleDictionary = []

with open("Task.txt", "r") as file:
    # questionNumber
    current_question_number = 0

    skip_next_line = False  # Flag to skip the next line after encountering '\section*{Choose the correct answer :}'

    for line in file:
        if skip_next_line:
            skip_next_line = False  # Reset the flag
            continue  # Skip the current line

        # Skip the line starting with '\section*{Choose the correct answer :}'
        if line.startswith("\\section*{Choose the correct answer :}"):
            skip_next_line = True  # Set the flag to skip the next line
            continue

        # questionId
        if "Question ID: " in line:
            current_question_number += 1
            questionId = line.split(": ")[1]
            while questionId and not questionId[-1].isdigit():
                questionId = questionId[:-1]

            current_question = {
                "questionNumber": current_question_number,
                "questionId": int(questionId),
                "questionText": "",
                "options": [
                    {"optionNumber": 1, "optionText": "", "isCorrect": False},
                    {"optionNumber": 2, "optionText": "", "isCorrect": False},
                    {"optionNumber": 3, "optionText": "", "isCorrect": False},
                    {"optionNumber": 4, "optionText": "", "isCorrect": False},
                ],
                "solutionText": "",
            }
            sampleDictionary.append(current_question)

        # solutionText
        elif "Sol." in line:
            solutionText = line.strip().split("Sol.")[1].strip()
            current_question["solutionText"] = solutionText

        # options
        elif line.startswith("("):
            optionNumber = line.strip()[1]  # Extract the option number directly
            optionText = line.strip()[3:].strip()
            index = ord(optionNumber) - ord("A")
            current_question["options"][index]["optionText"] = optionText

        # isCorrect
        elif "Answer (" in line:
            answerOption = line[line.index("(") + 1]
            correctOptionIndex = ord(answerOption) - ord("A") + 1
            if 1 <= correctOptionIndex <= len(current_question["options"]):
                current_question["options"][correctOptionIndex - 1]["isCorrect"] = True

        # optionText
        else:
            current_question["questionText"] += line.strip()

# Convert the sample dictionary to JSON format
json_data = json.dumps(sampleDictionary, indent=2)

# Write the JSON data to a file
with open("output.json", "w") as json_file:
    json_file.write(json_data)
