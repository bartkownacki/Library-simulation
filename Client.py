import random

nazwiska=["Kowalski", "Nowak", "Jurga", "Kownacki", "Tórz", "Kosakowski", "Olszewki", "Kuś", "Walenczewski", "Mumot", "Kamiński", "Adamczewski", "Adamkiewicz", "Owsienko", "Ciszewski", "Kycler", "Rau", "Matuszewski", "Kościuszko", "Poniatowski", "Szczerbal", "Abski", "Borucki", "Morski", "Stonoga"]
imiona = ["Ada", "Adam", "Alfred", "Bartosz", "Anita", "Anna", "Antonina", "Juri", "Cezary", "Lech", "Jakub", "Marek", "Tomasz", "Janusz", "Ignacy", "Basia", "Oliwia", "Vanessa", "Laura", "Aleksandra", "Olaf", "Urszula", "Weronikia", "Wiktor", "Wiktoria", "Zbigniew", "Zdzisław"]


def ServiceTime():
    x = random.gauss(3, 2)
    if (x < 0 or x > 10):
        return ServiceTime()
    else:
        return x


class Client:
    returnTime = 0
    queueTime = 0
    borrowedBook = 0
    def __init__(self,timeNow, day, month):
        self.serviceTime = round(ServiceTime(),2)
        self.arrivalTime = round(timeNow)
        self.name = random.choice(imiona)
        self.lastname = random.choice(nazwiska)
        self.orderTime = self.serviceTime
        self.day = day
        self.month = month

    def __str__(self):
        return 'Name: ' + self.name + ' || Lastname: ' + self.lastname + ' || Arrival time: ' +str(self.arrivalTime) + ' || Queue time: ' + str(self.queueTime) \
               + ' || Order time: ' + str(self.orderTime) + " || Month: " + str(self.month) + " || Day: " + str(self.day) + " || BorrowedBook: " + str(self.borrowedBook)+ " || ReturnTime: " + str(self.returnTime)

