from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import datetime
import random

server_name = "Asian Trio"
channel_name = "idle-miner"


class discord_bot:
    def __init__(self, login_email, login_password, server_name, channel_name):
        random.seed(time.time())
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        global driver
        driver = webdriver.Chrome(PATH)
        self.email = login_email
        self.password = login_password
        self.server = server_name
        self.channel = channel_name
        self.message = []
        self.p_level = 0
        self.b_level = 0
        self.cycle_time = 60
        self.total_cycle = 0
        self.session_cycle = 0
        self.full_time = 0
        self.rebirth_times = 0
        self.prestige_times = 0
        self.shards = 0
        self.quiz_answer = {}
        self.pets = {'Common': {}, 'Uncommon': {}, 'Rare': {},
                     'Epic': {}, 'Mythical': {}, 'Legendary': {}}

        self.init_persist()
        self.init_quiz()
        self.login()
        print('Logged in!\n')
        self.open_server_chat()
        print('Initializing...\n')
        self.update_profile()
        self.update_pets()
        print('Initialized! Starting cycle!')

    def init_quiz(self):
        file = open('quiz.txt')
        for line in file:
            (question, answer) = line.rstrip().split('~')
            self.quiz_answer[str(question)] = str(answer)
        file.close()

    def init_persist(self):
        try:
            file = open('bot persist.txt')
            self.total_cycle = int(file.readline().split("=")[1].strip())
            file.close()
        except FileNotFoundError:
            pass

    def update_persist(self):
        f = open("bot persist.txt", "w")
        f.write("Total cycle = "+str(self.total_cycle)+'\n')
        f.close()

    def login(self):
        driver.get("https://discordapp.com")
        driver.maximize_window()
        login = driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div/div/div[1]/div[1]/header[2]/nav/div[2]/a')
        login.click()

        WebDriverWait(driver, 3).until(presence_of_element_located(
            (By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/input')))

        email_element = driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/input')
        email_element.send_keys(self.email)
        password_element = driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input')
        password_element.send_keys(self.password)
        time.sleep(1)
        login = driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
        login.click()

    def open_server_chat(self):
        WebDriverWait(driver, 60).until(presence_of_element_located(
            (By.XPATH, '//a[@aria-label="' + self.server + '"]')))
        server = driver.find_element_by_xpath(
            '//a[@aria-label="' + self.server + '"]')
        driver.execute_script("arguments[0].click();", server)
        try:
            channel = driver.find_element_by_xpath(
                '//div[@aria-label="' + self.channel + ' (text channel)"]')
        except:
            channel = driver.find_element_by_xpath(
                '//div[@aria-label="unread, ' + self.channel + ' (text channel)"]')
        channel.click()

        driver.implicitly_wait(2)

    def get_message(self, message_id=50):
        # //*[@id="chat-messages-754553838798635018"]
        def get_message_quest(self, message_id):
            while message_id < 53:
                try:
                    WebDriverWait(driver, 3).until(
                        presence_of_element_located((By.XPATH, element)))
                    message = driver.find_element_by_xpath(
                        element).text.split("\n")
                    message.insert(0, "filler")
                    message.insert(0, "filler")
                    message.insert(0, "filler")
                    break
                except:
                    message_id += 1
            if message_id == 53:
                raise Exception("Quest message not found")
            else:
                return message

        time.sleep(random.random()*3)
        while True:
            try:
                #                element = '//*[@id="messages-'+str(message_id)+'"]'
                element = '/html/body/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/main/div[1]/div/div/div/div['+str(
                    message_id)+']'
                WebDriverWait(driver, 3).until(
                    presence_of_element_located((By.XPATH, element)))
                message_id += 1
            except:
                element = '/html/body/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/main/div[1]/div/div/div/div['+str(
                    message_id - 2)+']'
                message = driver.find_element_by_xpath(
                    element).text.split("\n")
                break

        try:
            if (message[4].split()[1] == "completed"):
                print("Quest message, retry! ")
                message = get_message_quest(self, message_id+1)

        except IndexError:
            pass

        self.message = message
        print(message)
        print('\n')
        return message

    def send_message(self, msg):
        textbox = driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div/main/form/div/div/div/div/div[3]/div[2]/div')
#        print('Sending '+msg+'!\n')
        textbox.send_keys(msg)
        textbox.send_keys(Keys.RETURN)
        time.sleep(2 + random.random()*3)

    def claimall(self):
        while True:
            try:
                self.send_message(";claimall")
#                self.get_message()
                print('Claimed all crates!\n')
                break
            except:
                print('No response from server, resending ;claimall command!\n')
                continue

    def prestige_kit(self):
        if self.prestige_times > 0:
            while True:
                try:
                    self.send_message(";prestigekit")
                    print('claimed prestige kit!\n')
#                    self.get_message()
                    break
                except:
                    print('No response from server, resending ;prestigekit command!\n')
                    continue

    def open_all(self):
        while True:
            try:
                self.send_message(";open all")
                print('Opened all crates!\n')
#                self.get_message()
                break
            except:
                print('No response from server, resending ;open_all command!\n')
                continue

    def wings(self):
        while True:
            try:
                self.send_message(";wings")
                print('Wing used!\n')
#                self.get_message(48)
                break
            except:
                print('No response from server, resending ;wings command!\n')
                continue

    def rage(self):
        while True:
            try:
                self.send_message(";rage")
                print('Rage used!\n')
#                self.get_message()
                break
            except:
                print('No response from server, resending ;rage command!\n')
                continue

    def earthquake(self):
        while True:
            try:
                self.send_message(";earthquake")
                print('Earthquake used!\n')
#                self.get_message()
                break
            except:
                print('No response from server, resending ;earthquake command!\n')
                continue

    def sell(self):
        while True:
            try:
                self.send_message(";sell")
#                self.get_message()
                print('Sold backpack!\n')
                break
            except:
                print('No response from server, resending ;sell command!\n')
                continue

    def hunt(self):
        while True:
            try:
                self.send_message(";hunt")
                print('Hunted!\n')
                self.get_message()
                try:
                    if self.message[3].split()[2] == "didn't":
                        pass
                    else:
                        self.update_pets()
                    break
                except IndexError:
                    self.update_pets()
                    break
            except:
                print('No response from server, resending ;hunt command!\n')
                continue

    def fish(self):
        while True:
            try:
                self.send_message(";fish")
                print('Fished!\n')
#                self.get_message()
                break
            except:
                print('No response from server, resending ;fish command!\n')
                continue

    def quiz(self):
        while True:
            try:
                self.send_message(";quiz")
                print('Requesting quiz!\n')
                self.get_message()
                break
            except:
                print('No response from server, resending ;quiz command!\n')
                continue
        answer_dic = {}
        line_num = 8
        try:
            question = self.message[7]
            while self.message[line_num].split()[0] != 'Idle':
                answer_choice = self.message[line_num].split(']')[1].lstrip()
                answer_letter = self.message[line_num].split(']')[
                    0].lstrip('[')
                answer_dic[answer_choice] = answer_letter
                line_num += 1
            answer = self.quiz_answer[question]
            self.send_message(answer_dic[answer])
        except KeyError:
            print("Key not found!")
            question_list = []
            f = open('quiz_not_found.txt', 'a+')
            f.seek(0)
            for line in f:
                question_list.append(line.split('[')[0])
            line_num = 7
            while self.message[line_num].split()[0] != 'Idle':
                if self.message[7] in question_list:
                    break
                f.write(self.message[line_num])
                line_num += 1
            if self.message[7] not in question_list:
                f.write('\n\n')
            f.close()
            return None
        except IndexError:
            print("Invalid quiz question!")
            return None

    def rebirth(self):
        while True:
            try:
                self.send_message(";rebirth")
                print('Rebirth!\n')
#                self.get_message()
                break
            except:
                continue

    def prestige(self):
        while True:
            try:
                self.send_message(";prestige")
                print('Prestige!\n')
#               self.get_message()
                break
            except:
                continue

    def up_tools(self):
        def up_p(self, level='a'):
            while True:
                try:
                    self.send_message(";up p "+str(level))
                    self.get_message()
                    break
                except:
                    print('No response from server, resending ' +
                          ";up p " + str(level) + ' command!\n')
                    continue

        def up_b(self, level='a'):
            while True:
                try:
                    self.send_message(";up b "+str(level))
                    self.get_message()
                    break
                except:
                    print('No response from server, resending ' +
                          ";up b " + str(level) + ' command!\n')
                    continue

        while True:

            if self.p_level < self.b_level < 190:
                up_p(self)
            elif self.b_level < self.p_level < 190:
                up_b(self)
            elif self.p_level > self.b_level and self.b_level < 200:
                print('Upgrading backpack!\n')
                up_b(self, 200 - self.b_level)
                if self.message[3].split()[2] == "can't":
                    up_b(self)
            elif self.b_level >= self.p_level and self.p_level < 200:
                print('Upgrading pickaxe!\n')
                up_p(self, 200 - self.p_level)
                if self.message[3].split()[2] == "can't":
                    up_p(self)
            self.update_profile()
            break

    def upgrade_pet(self):
        pet_max_level = 5 + 5 * self.rebirth_times

        def returnSum(mydict):
            s = 0
            for i in mydict.values():
                s += i
            if s == None:
                s = 0
            return s

        def up_pet(self, pet, level='a'):
            while True:
                try:
                    self.send_message(";up " + pet + " " + str(level))
                    self.get_message()
                    break
                except:
                    print('No response from server, resending ' +
                          ";up " + pet + " " + str(level) + ' command!\n')
                    continue

        def upgrade_common(self, level='a'):
            if common_sum == 0:
                return False
            common_list = list(self.pets.get('Common'))
            while True:
                target = common_list.pop(random.randrange(len(common_list)))
                if self.pets.get('Common').get(target) < pet_max_level:
                    print('Upgrading '+target+'!\n')
                    up_pet(self, target, level)
                    return True
                else:
                    if len(common_list) == 0:
                        return False
                    else:
                        continue

        def upgrade_uncommon(self, level='a'):
            if uncommon_sum == 0:
                return False
            uncommon_list = list(self.pets.get('Uncommon'))
            while True:
                target = uncommon_list.pop(
                    random.randrange(len(uncommon_list)))
                if self.pets.get('Uncommon').get(target) < pet_max_level:
                    print('Upgrading '+target+'!\n')
                    up_pet(self, target, level)
                    return True
                else:
                    if len(uncommon_list) == 0:
                        return False
                    else:
                        continue
        common_sum = returnSum(self.pets.get('Common'))
        uncommon_sum = returnSum(self.pets.get('Uncommon'))
        if common_sum > uncommon_sum:
            if upgrade_uncommon(self) == False:
                upgrade_common(self)
        else:
            if upgrade_common(self) == False:
                upgrade_uncommon(self)
        self.update_pets()

    def update_full_time(self):
        while True:
            try:
                self.send_message(";bp")
                print('Updating time to full backpack!\n')
                time = self.get_message()[9]
                break
            except:
                print('No response from server, resending ;bp command!\n')
                continue
        if time == "FULL":
            self.full_time = 0
            return 0
        else:
            if "h" in time.split()[2]:
                (hour, minute) = time.split()[2].split("h")
                minute = minute[:-1]
                self.full_time = (int(hour)*3600 + int(minute)*60 + 60)
                return int(hour)*3600 + int(minute)*60 + 60
            elif "m" in time.split()[2]:
                (minute, second) = time.split()[2].split("m")
                second = second[:-1]
                self.full_time = (int(minute)*60 + int(second))
                return int(minute)*60 + int(second)
            else:
                return int(time.split()[2][:-1])

    def update_profile(self):
        while True:
            try:
                self.send_message(";p")
                print('Fetching profile!\n')
                self.get_message()
                break
            except:
                print('No response from server, resending ;p command!\n')
                continue
        try:
            try:
                self.p_level = int(self.message[17].split()[1][:-1])
                self.b_level = int(self.message[13].split()[1][:-1])
                self.rebirth_times = int(self.message[10].split()[1])
                self.shards = int(self.message[9].split()[1])
            except ValueError:
                try:
                    self.prestige_times = int(self.message[8].split()[1])
                    self.p_level = int(self.message[21].split()[1][:-1])
                    self.b_level = int(self.message[17].split()[1][:-1])
                    self.rebirth_times = int(self.message[11].split()[1])
                    self.shards = int(self.message[10].split()[1])
                except ValueError:
                    self.prestige_times = int(self.message[8].split()[1])
                    self.p_level = int(self.message[20].split()[1][:-1])
                    self.b_level = int(self.message[16].split()[1][:-1])
                    self.rebirth_times = int(self.message[11].split()[1])
                    self.shards = int(self.message[10].split()[1])
        except IndexError:
            print("Cannot parse message into profile, reacquiring profile... ")
            self.update_profile()

    def update_pets(self):
        self.pets = {'Common': {}, 'Uncommon': {}, 'Rare': {},
                     'Epic': {}, 'Mythical': {}, 'Legendary': {}}
        while True:
            try:
                self.send_message(";pet")
                print('Fetching pets!\n')
                self.get_message()
                token = " "
                rarity = ''
                i = 9
                while True:
                    i += 1
                    token = self.message[i]
                    if token.split()[0] == "Idle":
                        break
                    if token in ["Common", "Uncommon", "Rare", "Epic", "Mythical", "Legendary"]:
                        rarity = token
                        continue
                    self.pets[rarity][str(token.split()[0])] = int(
                        token.split()[-1][:-1])
                break
            except:
                continue

    def process(self):
        try:
            while True:
                self.session_cycle += 1
                self.total_cycle += 1
                print("Starting cycle ", str(self.total_cycle), '... (Cycle ', str(
                    self.session_cycle), ' in current session) \n', sep='')
                self.sell()
                if ((self.session_cycle % (300 // self.cycle_time)) == 1) and ('Ender-dragon' in self.pets.get('Legendary')):
                    self.wings()
                    for i in range(55, 5, -5):
                        print(i, "seconds remaining")
                        time.sleep(5)
                    self.sell()
                self.up_tools()
                if ((self.p_level >= 200) != (self.b_level >= 200)):
                    self.up_tools()
                if self.p_level >= 200 and self.b_level >= 200:
                    if self.rebirth_times == 25:
                        self.prestige()
                        self.update_pets()
                    else:
                        self.rebirth()
                if (self.session_cycle % (300 // self.cycle_time)) == 1:
                    if ('Giant' in self.pets.get('Legendary')):
                        self.earthquake()
                        self.up_tools()
                    if ('Wither' in self.pets.get('Legendary')):
                        self.rage()
                    self.hunt()
                    self.fish()
                    self.quiz()
                    self.upgrade_pet()
                if (self.session_cycle % (3600 // self.cycle_time)) == 10:
                    self.claimall()
                    self.open_all()
                self.update_profile()
                print('Cycle '+str(self.total_cycle) +
                      ' done! Sleeping for '+str(self.cycle_time)+' seconds!\n')
                for i in range(self.cycle_time, 0, -10):
                    print(i, "seconds remaining")
                    time.sleep(10)
        except KeyboardInterrupt:
            print("Bot signing off! ")
            self.update_persist()
            driver.quit()
        finally:
            self.update_persist()
            driver.quit()


def main():
    try:
        f = open("login.txt")
        login_email = f.readline()
        login_password = f.readline()
    except FileNotFoundError:
        login_email = input("Please enter your login email: ")
        login_password = input("Please enter your login password: ")
    a = discord_bot(login_email, login_password, server_name, channel_name)
    a.process()


main()
