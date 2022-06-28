import getpass
import json
from secure.secure import *

def password(question=""):
    return getpass.getpass()


def line(question):
    text = input(question)
    return text


def cli_questions(questions_arr, counter=0):
    [name, question, secure] = questions_arr[counter].values()
    if secure:
        answer = password(question)
    else:
        answer = line(question)

    if counter == len(questions_arr) - 1:
        return {name:answer}

    return {name: answer, **cli_questions(questions_arr, counter + 1)}


def add_question():
    attach = input("Do you want to set security question? (Y/n) ")
    if attach == "Y":
        suggest_question = decode("E:/PycharmProjects/SPBD_labs/lab2/questions.json")
        number = 1
        for i in suggest_question['questions'].values():
            print("{}. {}".format(number, i))
            number += 1
        number_of_question = input("Choose the number of question: ")
        answer_secret_question = input("Enter the answer to the security question: ")
    return {"question": number_of_question, "answer": answer_secret_question}

