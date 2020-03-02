import time
import random
import math
from Client import Client
import pymysql
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook


cnxn = pymysql.connect(host="localhost", user="root", passwd="", database="Library")
cursor = cnxn.cursor()
cursor.execute(f"SELECT MAX(Id) as MaxID from Books")
maxId = cursor.fetchone()[0]


def CleanDatabaseClients():
    cursor.execute("DELETE FROM clients;")
    cnxn.commit()
    cursor.execute("ALTER TABLE clients AUTO_INCREMENT = 1")
    cnxn.commit()

def ResetDatabaseBooks():
    cursor.execute("DELETE FROM books;")
    cnxn.commit()
    cursor.execute("ALTER TABLE books AUTO_INCREMENT = 1")
    cnxn.commit()
    workbook = load_workbook(filename="books.xlsx")
    sheet = workbook.active
    print("----Rozpoczęto wgrywanie książek do bazy danych----")
    for i in range(2, 816):
        title = "'" + sheet[f"A{i}"].value + "'"
        author = "'" + sheet[f"B{i}"].value + "'"
        signature = "'" + str(sheet[f"C{i}"].value) + "'"
        amount = int(random.randint(1, 5))
        cursor.execute("INSERT INTO books(Title, Author, Signature, Amount) VALUES (%s,%s,%s,%d)" % (
        title, author, signature, amount))
        cnxn.commit()
    print("----Ukończono wgrywanie książek do bazy danych----")

def BorrowABook(client):
    randomBookId = random.randint(1, maxId)
    cursor.execute(f"Select Amount FROM BOOKS WHERE Id = '{randomBookId}'")
    quantity = cursor.fetchone()[0]
    if (quantity != 0):
        cursor.execute(f"UPDATE Books SET Amount = Amount - 1 Where Id ='{randomBookId}'")
        client.borrowedBook = randomBookId
        client.returnTime = [0,0,1,2].pop(random.randint(0,3))
        cnxn.commit()

def ReturnABook(borrowedBookId):
    cursor.execute(f"UPDATE Books SET Amount = Amount + 1 Where Id ='{borrowedBookId}'")

def GetSimulationTime():
    try:
        monthsOfSimulation = int(input("Podaj liczbe miesiecy symulacji: "))
        daysOfSimulation = int(input("Podaj liczbe dni symulacji: "))
        hoursOfSimulation = int(input("Podaj liczbe godzin symulacji: "))
        minutesOfSimulation = int(input("Podaj liczbe minut symulacji: "))
        return float(minutesOfSimulation + hoursOfSimulation * 60 + daysOfSimulation * 480 + monthsOfSimulation * 14400)
    except ValueError:
        print("Podaj poprawna wartosc czasu.")
        return GetSimulationTime()

def drawPlots():
    cnxn = pymysql.connect(host="localhost", user="root", passwd="", database="Library")
    cursor = cnxn.cursor()
    plot = input("1. Ilosc klientow zadowolonych oraz niezadowolonych\n"
                 "2. Ilosc klientow w poszczegolne dni\n"
                 "3. Stosunek udanych wypozyczen do nieudanych\n"
                 "Jaki wykres wybierasz (wpisz 0 dla zakonczenia programu): ")
    if plot == "0":
        exit()
    if plot == "1":
        objects = ('Zadowolony', 'Niezadowolony')
        y_pos = np.arange(len(objects))
        cursor.execute(f"Select Pleased, count(*) as Amount FROM Clients Group By Pleased Order By Pleased ASC")
        rows = cursor.fetchall()
        unpleasedClients = 0
        pleasedClients = 0
        if rows:
            if rows[0][0] == "YES":
                pleasedClients = rows[0][1]
            if rows[0][0] == "NO":
                unpleasedClients = rows[0][1]
                pleasedClients = rows[1][1]

        quantityOfObject = [pleasedClients,unpleasedClients]
        plt.title("Ilosc klientow zadowolonych oraz niezadowolonych")
        plt.xlabel("Klient")
        plt.ylabel("Ilosc")
        plt.bar(y_pos, quantityOfObject, color = ["green","red"],align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.show()
    if plot == "2":
        cursor.execute(
            f"Select DayDATE, MonthDATE, count(*) as Amount FROM Clients Group By DayDate, MonthDate Order By DayDate,MonthDate ASC")
        rows = cursor.fetchall()
        objects = []
        amountOfPeople = []
        for row in rows:
            amountOfPeople.append(row[2])
            objects.append("M" + str(row[1]) + "D" + str(row[0]))
        y_pos = np.arange(len(objects))
        plt.title("Ilosc klientow w poszczegolne dni")
        plt.xlabel("Miesiac oraz dzien")
        plt.ylabel("Ilosc klientow")
        plt.bar(y_pos, amountOfPeople, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.show()
    if plot == "3":
        objects = ('Ksiazka wypozyczona', 'Ksiazka niewypozyczona')
        y_pos = np.arange(len(objects))
        cnxn = pymysql.connect(host="localhost", user="root", passwd="", database="Library")
        cursor = cnxn.cursor()
        cursor.execute("SELECT count(*) from Clients where BorrowedBook = 0")
        row = cursor.fetchone()
        if row:
            notBorrowedAmount = row[0]
        cursor.execute("SELECT count(*) from Clients")
        row = cursor.fetchone()
        if row:
            borrowedAmount = row[0] - notBorrowedAmount
        quantityOfObject = [borrowedAmount, notBorrowedAmount]
        plt.title("Stosunek udanych wypozyczen do nieudanych")
        plt.ylabel("Ilosc")
        plt.bar(y_pos, quantityOfObject, color=["green", "red"], align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.show()

def Symulacja(simulationTime):
    startTime = time.time()
    startOfRunningTime = time.time()
    queue = []
    timer = 0
    pleasedClients = 0
    unpleasedClients = 0
    day = 1
    month = 1
    minutesOfWorkInDay = 480
    while True:
        timeNow = time.time() - startTime  # POKAZUJE CZAS W SEKUNDACH OD ROZPOCZECIA SYMULACJI
        runningTime = time.time() - startOfRunningTime
        ############################## KONCZENIE SYMULACJI ##############################
        if (timeNow + (day-1)*minutesOfWorkInDay + (month-1)*minutesOfWorkInDay*30 >= simulationTime and len(queue)==0):
            print("Zakonczono symulowanie " + str(round((simulationTime/minutesOfWorkInDay),2)) + " dnia pracy. Liczba zadowolonych klientow: " + str(pleasedClients) + ". Liczba niezadowolonych klientow: " + str(unpleasedClients) + ".")
            drawPlots()
        #################################################################################
        if (timeNow - timer) >= 1:
            ######### SZANSA WZGLEDEM CZASU #########
            if timeNow <= 20:
                chance = 30
            if timeNow > 20 and timeNow <= 60:
                chance = 15
            if timeNow > 60 and timeNow <= 120:
                chance = 20
            if timeNow > 120 and timeNow <= 420:
                chance = 25
            if timeNow > 420 and timeNow <= 480:
                chance = 40
            if timeNow > minutesOfWorkInDay or timeNow > simulationTime:
                chance = 0
            ##########################################
            ################### GENEROWANIE KLIENTA ###################
            if random.randint(0, 99) < chance:
                newClient = Client(timeNow, day, month)
                if len(queue) > 0:
                    newClient.queueTime = round(queue[len(queue) - 1].orderTime - (newClient.arrivalTime - queue[len(queue) - 1].arrivalTime), 2)
                    newClient.orderTime = round(newClient.serviceTime + newClient.queueTime, 2)
                if (newClient.queueTime < 5 and newClient.borrowedBook!=0):
                    pleasedClients += 1
                else:
                    unpleasedClients += 1
                queue.append(newClient)
                BorrowABook(newClient)
                ###########################################################
                ################################## WGRYWANIE KLIENTA DO BAZY DANYCH ##################################
                name = "'" + newClient.name + "'"
                lastname = "'" + newClient.lastname + "'"
                time_ = timeNow
                minute_ = timeNow % 60
                hour_ = math.floor(time_ / 60)
                if (newClient.queueTime < 5 and newClient.borrowedBook!=0):
                    pleased = "'" + 'YES' + "'"
                else:
                    pleased = "'" + 'NO' + "'"

                cursor.execute("INSERT INTO Clients(Name,Lastname,MonthDATE,DayDATE,HourDATE,MinuteDATE,ArrivalTime,OrderTime,ServiceTime,QueueTime,Pleased,BorrowedBook,ReturnTime) "
                               "VALUES (%s,%s,%d,%d,%d,%d,%d,%f,%f,%f,%s,%d,%d)" %(name,lastname,month,day,hour_,minute_,math.floor(newClient.arrivalTime),newClient.orderTime,newClient.serviceTime,newClient.queueTime,pleased,newClient.borrowedBook,newClient.returnTime))
                cnxn.commit()
                ######################################################################################################



            print(str(round(timeNow))+"min"+ " =================================================================================== " + str(round(runningTime))+"s")
            for i in queue:
                print(i)
            if len(queue)==0:
                print("Nie ma nikogo w kolejce.")
            timer = time.time() - startTime
        ################## USUWANIE KLIENTA Z KOLEJKI ##################
        if len(queue)>0:
            if(timeNow - queue[0].arrivalTime) > queue[0].orderTime:
                queue.pop(0)
        ################################################################
        #################### ZMIANA DNI I MIESIECY  ####################
        if len(queue) == 0 and timeNow >= minutesOfWorkInDay:
            day += 1
            if day > 30:
                day = 1
                month += 1
            cursor.execute(f"Select DayDATE, MonthDATE,ReturnTime,BorrowedBook From Clients WHERE BorrowedBook!=0")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    monthDelay = 0
                    d = row[0]
                    ret = row[2]
                    if d + ret > 30:
                        monthDelay = math.floor((d + ret) / 30)
                        d = (d + ret) % 30
                        ret = 0
                    if [d + ret, row[1] + 1 + monthDelay] == [day, month]:
                        ReturnABook(row[3])
            if timeNow<minutesOfWorkInDay+0.5:
                print(str(round(timeNow))+"min"+ " =================================================================================== " + str(round(runningTime))+"s")
                print("Nie ma nikogo w kolejce.")
            startTime = time.time()
            timer = 0
        ################################################################


if __name__ == "__main__":
    ResetDatabaseBooks()
    CleanDatabaseClients()
    Symulacja(GetSimulationTime())
