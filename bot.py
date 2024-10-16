import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

DRIVER_PATH = "./chromedriver.exe"
TIMEOUT = 5
READ_TIME = 5


HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def customPrint(text, texttype="MESSAGE"):
    if texttype == "WARNING":
        print(f"{WARNING}${texttype}: {text}{ENDC}")
    elif texttype == "SUCCESS":
        print(f"{OKGREEN}${texttype}: {text}{ENDC}")
    elif texttype == "INFO":
        print(f"{OKCYAN}${texttype}: {text}{ENDC}")
    elif texttype == "ERROR":
        print(f"{FAIL}${texttype}: {text}{ENDC}")
    elif texttype == "MESSAGE":
        print(f"{OKBLUE}${texttype}: {text}{ENDC}")
    else:
        print(f"{FAIL}{text}{ENDC}")


class Bot:
    default_tab = ""
    visited = []

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.get("https://myacademy.oracle.com/lmt/xlr8login.login?site=oa")

        self.parent_handle = self.driver.current_window_handle
        with open("visited.txt", "r") as file:
            for line in file:
                self.visited.append(line.strip())

    def appendCompleted(self, string):
        with open("visited.txt", "a") as visited_file:
            self.visited.append(string)
            visited_file.write(string + "\n")

    def getFirstIncomplete(self):
        while True:
            try:
                collapsibles = self.driver.find_elements_by_class_name(
                    "learning-path--detail__section"
                )

                collapsibles.pop(0)
                customPrint("Got Collapsables", "INFO")
                for collapsible in collapsibles:
                    items = None
                    try:
                        items = collapsible.find_elements_by_class_name("card")
                    except:
                        continue
                    for item in items:
                        try:
                            comp = False
                            try:
                                completed = item.find_element_by_class_name(
                                    "course-badges"
                                )
                                comp = True
                            except:
                                comp = False
                            quiz = item.find_element_by_tag_name("a")

                            quizzer = quiz.find_element_by_tag_name("span").text
                            customPrint(quizzer, "MESSAGE")
                            if comp == True:
                                comp = False
                                customPrint("completed badge found skipping", "INFO")
                                self.appendCompleted(quizzer)
                                continue
                            elif quizzer in self.visited:
                                customPrint("VISITED Skipping", "INFO")
                                continue
                            elif "Quiz" in quizzer:
                                customPrint("QUIZ Skipping", "INFO")
                                self.appendCompleted(quizzer)
                                continue
                            elif "Exam" in quizzer:
                                customPrint("EXAM Skipping", "INFO")
                                self.appendCompleted(quizzer)

                                continue
                            raise Exception
                        except Exception as e:
                            self.appendCompleted(quizzer)

                            return item
                return None
            except Exception as err:
                time.sleep(TIMEOUT)
            quiz_detect = ""

    def completeOne(self, item):
        customPrint("Completing One", "INFO")
        while True:
            try:

                box = item.find_element_by_tag_name("img").click()
                customPrint("Entered the course", "SUCCESS")
                return True
            except:
                time.sleep(TIMEOUT)

    def closeAllOtherHandles(self):
        handles = self.driver.window_handles
        size = len(handles)
        for x in range(size):
            if handles[x] != self.parent_handle:
                self.driver.switch_to_window(handles[x])
                print(self.driver.title)
                self.driver.close()
        self.driver.switch_to_window(self.parent_handle)
        customPrint("Closed All Other Handles", "INFO")

    def play(self):
        while True:
            try:
                time.sleep(3)
                section = self.driver.find_element_by_class_name("section")
                main_div = section.find_element_by_class_name("main")
                course_div = main_div.find_element_by_class_name(
                    "course-details__intro"
                )
                but_div = course_div.find_element_by_class_name("cta")

            except Exception as e:
                customPrint("Error Occured in Finding Play Button", "ERROR")
                time.sleep(TIMEOUT)
            try:
                # Find the anchor tag with the class "play" within the detail div
                play_button = but_div.find_element_by_tag_name("a")

                if play_button:
                    play_button.click()
                    customPrint("Clicked on play button", "SUCCESS")
                    time.sleep(READ_TIME)
                    self.switchTabs()
                    self.nextPress()
                    break

                else:
                    customPrint("Play button not found within the detail div", "ERROR")
            except Exception as e:
                customPrint("Exception occurred:", "ERROR")
                time.sleep(TIMEOUT)
                break
        return True

    def nextPress(self):
        runner = True
        flag = 0
        flag1 = 0
        while True:
            if flag != 0:
                break
            try:
                wait = WebDriverWait(self.driver, 20)
                iframe = wait.until(
                    EC.presence_of_element_located((By.ID, "content-iframe"))
                )
                self.driver.switch_to.frame(iframe)
                while True:
                    try:
                        max_wait_time = 5
                        elapsed_time = 0

                        if runner:
                            while True:

                                try:
                                    try:
                                        try:
                                            # Check if the next button is clickable
                                            next_button = WebDriverWait(
                                                self.driver, 1
                                            ).until(
                                                EC.element_to_be_clickable(
                                                    (
                                                        By.CSS_SELECTOR,
                                                        ".universal-control-panel__button_next, .universal-control-panel__button_right-arrow",
                                                    )
                                                )
                                            )
                                            # If found, click on it and exit the loop

                                            next_button.click()
                                            break
                                        except:
                                            try:
                                                # Check if the next button is clickable
                                                next_button = WebDriverWait(
                                                    self.driver, 1
                                                ).until(
                                                    EC.element_to_be_clickable(
                                                        (
                                                            By.CSS_SELECTOR,
                                                            ".uikit-primary-button_next, .uikit-primary-button_next navigation-controls__button_next",
                                                        )
                                                    )
                                                )
                                                # If found, click on it and exit the loop

                                                next_button.click()
                                                break
                                            except:

                                                next_button = WebDriverWait(
                                                    self.driver, 1
                                                ).until(
                                                    EC.element_to_be_clickable(
                                                        (
                                                            By.CSS_SELECTOR,
                                                            ".window-button, .window-button_yes",
                                                        )
                                                    )
                                                )
                                                # If found, click on it and exit the loop

                                                next_button.click()
                                                break
                                    except:
                                        if flag1 == 0:
                                            time.sleep(2)
                                            elapsed_time = 0
                                            self.quizExtractor()
                                            flag1 = 1
                                            break
                                        if flag1 == 1:
                                            raise "myException"

                                except:
                                    # If the button is not found within 1 second or if it's not clickable, check elapsed time
                                    elapsed_time += 1
                                    # If the elapsed time exceeds the maximum wait time, exit the loop
                                    if elapsed_time > max_wait_time:
                                        customPrint(
                                            "Button not found within the maximum wait time. Proceeding without waiting.",
                                            "INFO",
                                        )

                                        break
                                    else:

                                        runner = False

                                        customPrint(
                                            "Failed to find or click the next button:",
                                            "INFO",
                                        )
                                        return

                        else:
                            break
                    except Exception as e:
                        self.visited.append()

                        break

            except:
                self.visited.append(self.quiz_detect)
                flag = 1
                with open("visited.txt", "w") as file:
                    for item in self.visited:
                        file.write("%s\n" % item)

                break

    def switchTabs(self):

        try:
            global default_tab
            default_tab = self.driver.window_handles[0]
            new_tab_handle = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_tab_handle)
            customPrint("switched tabs", "INFO")

        except:
            customPrint("Cannot switch", "ERROR")

    def defaultSwitch(self):
        try:

            self.driver.switch_to.window(default_tab)
            customPrint("switched to default tab", "SUCCESS")
        except:
            customPrint("Cannot switch", "ERROR")

    def goBackToLearningPath(self):
        customPrint("Going back to learning path", "INFO")
        self.driver.close()
        time.sleep(2)
        self.defaultSwitch()
        time.sleep(2)
        self.driver.back()
        time.sleep(2)
        self.driver.refresh()
        time.sleep(4)
        return True

    def quizExtractor(self):
        quizCounter = 0
        while quizCounter != 2:
            # time.sleep(2)
            quizQuestionOption = {"question": "", "options": []}

            optArr = []
            try:
                waiter = WebDriverWait(self.driver, 16)
                waiter.until(
                    EC.presence_of_element_located(
                        (
                            By.CLASS_NAME,
                            "player-shape-view__shape-view-rich-text-view_wrap-text",
                        )
                    )
                )

                question = self.driver.find_element_by_class_name(
                    "player-shape-view__shape-view-rich-text-view_wrap-text"
                )

                try:
                    option = self.driver.find_elements_by_class_name("choice-view")
                    for i in option:
                        optArr.append(i.text)

                except:
                    customPrint("options not found", "ERROR")

            except:
                customPrint("question not found", "ERROR")
                quizCounter += 1
                return

            quizQuestionOption["question"] = question.text
            quizQuestionOption["options"] = optArr
            print(quizQuestionOption)

            quiz_json = json.dumps(quizQuestionOption)
            url = "http://127.0.0.1:5000/sendquestion"
            try:
                response = requests.post(url, json=quiz_json)
                if response.status_code == 200:
                    customPrint("Question Sent Succesfully", "SUCCESS")
                    result = response.json()
                    finalAnswer = result["message"]

                else:
                    pass
            except Exception as e:
                print(e)
            if finalAnswer in optArr:
                index = optArr.index(finalAnswer)
            else:
                index = 0
            self.quizPress(index)
            quizCounter += 1

    def quizPress(self, option):
        try:
            optPressButton = self.driver.find_elements_by_class_name(
                "choice-view__choice-container"
            )
            optPressButton[option].click()
            customPrint("clicked option", "INFO")

            try:
                submitButton = self.driver.find_element_by_class_name(
                    "quiz-control-panel__text-label"
                )
                submitButton.click()
                customPrint("clicked submit button", "INFO")
            except:
                customPrint("SUBMIT BUTTON NOT FOUND", "ERROR")
        except:
            customPrint("OPTIONS NOT FOUND", "ERROR")
            pass
        try:

            continueButton = self.driver.find_element_by_class_name(
                "quiz-control-panel__button_show-arrow"
            )
            continueButton.click()

        except:

            viewResult = self.driver.find_element_by_class_name(
                "quiz-control-panel__container_right"
            )
            viewResult.click()

        return

    def close(self):
        customPrint("Closed Bot", "INFO")
        self.driver.close()
