# Bron 1: https://stackoverflow.com/questions/20302682/mastermind-in-python

import random
import time

def startgame():
    global Secretcode
    global algo_choice
    # variable voor keuze: eigen code of random generated
    # waarde 0 = user
    # waarde 1 = RNG
    howtocode = int(input("Code zelf maken of laten genereren?\n0=user input, 1=RNG"))

    #Gebruiker selecteerd optie: handmatige invoer van geheime code
    if howtocode ==0:
        #de input wordt eerst als string gemaakt, omdat bijvoorbeeld de code '0011'  als integer automatisch zou veranderen naar '11'
        Secretcode = [int(i) for i in [char for char in str(input('vul 4 cijfers in (0 t/m 5): '))]]
        print(f'Dit is de code dmv userinpit {Secretcode}')
    #Gebruiker selecteerd optie: random generated geheime code
    elif howtocode ==1:
        #hier word een list dat 4 willekeurige intergers bevat(0 tot 6) aangemaakt
        Secretcode = list(map(int, random.sample(range(0, 6), 4)))
        print(f'Dit is de code dmv random {Secretcode}')
    algo_choice = int(input("Welk algorithme wil je gebruiken?\n0=user input, 1=worst case strategy, 2=simple strategy"))
    selectalgo(algo_choice)


def selectalgo(algo_choice):
    # variable die aangeeft welk algoritme gebruikt word
    # waarde 0 = user input
    # waarde 1 = worst case strategy
    # waarde 2 = simple strategy
    if algo_choice==0:
        breakit()
    if algo_choice==1:
        worstcasestrat(Secretcode)
    if algo_choice == 2:
        simplestrat(Secretcode)

#de gebruiker heeft gekozen om handmatig de code te kraken
def breakit():
    # de input wordt eerst als string gemaakt, omdat bijvoorbeeld de code '0011'  als integer automatisch zou veranderen naar '11'
    guess = [int(i) for i in [char for char in str(input('vul 4 cijfers in (0 t/m 5): '))]]
    print(f'Dit is de guess dmv userinput {guess}')
    print(pegs(guess, Secretcode, algo_choice))
    if pegs(guess, Secretcode, algo_choice) != [4,0]:
        breakit()
    else:
        print('GGWP')
        quit()

#deze functie returned een list met aantal red en white pegs.  Format:[red, white]
#inspired from 'bron 1'
def pegs(guess, Secretcode,algo_choice):
    red = 0
    white = 0
    secretcop = Secretcode.copy()
    guesscop = guess.copy()
    for i in range(len(Secretcode)):
        if guess[i] == Secretcode[i]:
            red += 1
            secretcop.remove(Secretcode[i])
            guesscop.remove(guess[i])

    for i in range(len(secretcop)):
        if guesscop[i] in secretcop:
            white += 1
            secretcop.remove(guesscop[i])
    return [red, white]

#functie die de simpele strategie volgt
def simplestrat(Secretcode):
    count = 0
    alloption = []
    currentoption = []
    # Loop die alle mogelijk combinaties, in lists plaatst
    # De lists worden zo aangemaakt, dat ze gelijk gesorteerd zijn.
    for i0 in range(0, 6):
        for i1 in range(0, 6):
            for i2 in range(0, 6):
                for i3 in range(0, 6):
                    alloption.append([i0, i1, i2, i3])
                    currentoption.append([i0, i1, i2, i3])

    while True:
        #maak een gok met de eerst mogelijke optie uit een gesorteerde lijst
        guess = currentoption[0]
        count += 1
        feedback = pegs(guess, Secretcode,algo_choice)
        print(f'Guess: {guess} Feedback:{feedback}')

        #als de feedback [4,0] is, is het algoritme klaar
        if feedback == [4,0]:
            print(f'\nGGWP GAMER, het heeft {count} turns gekost')

            quit()

        #Hier wordt een lijst gemaakt waar alle mogelijke codes worden getest tegen de guess
        checklst=[]
        for i0 in range(0, 6):
            for i1 in range(0, 6):
                for i2 in range(0, 6):
                    for i3 in range(0, 6):
                        checksecret=[i0,i1,i2,i3]
                        if pegs(guess, checksecret, algo_choice)==feedback:
                            checklst.append(checksecret)

        #de mogelijke opties  worden in de lijst geplaatst
        currentoption =[item for item in currentoption if item in checklst]
        print(f'Possible options left: {len(currentoption)}')



def worstcasestrat(Secretcode):
    count = 0
    alloption = []
    currentoption = []
    # Loop die alle mogelijk combinaties, in lists plaatst
    # De lists worden zo aangemaakt, dat ze gelijk gesorteerd zijn.
    for i0 in range(0, 6):
        for i1 in range(0, 6):
            for i2 in range(0, 6):
                for i3 in range(0, 6):
                    alloption.append([i0, i1, i2, i3])
                    currentoption.append([i0, i1, i2, i3])
    guess = [0,0,1,1]
    count += 1
    feedback = pegs(guess, Secretcode, algo_choice)
    print(f'guess: {guess} feedback:{feedback}')
    if feedback == [4, 0]:
        print(f'Hole in one!')
        quit()

    while True:
        guess = currentoption[0]
        count += 1
        feedback = pegs(guess, Secretcode, algo_choice)
        print(f'guess: {guess} feedback:{feedback}')

        # als de feedback [4,0] is, is het algoritme klaar
        if feedback == [4, 0]:
            print(f'GGWP GAMER, het heeft {count} turns gekost')
            print(f'De code was {Secretcode}.')
            quit()

        # Hier wordt een lijst gemaakt waar alle mogelijke codes worden getest tegen de guess
        checklst = []
        for i0 in range(0, 6):
            for i1 in range(0, 6):
                for i2 in range(0, 6):
                    for i3 in range(0, 6):
                        checksecret = [i0, i1, i2, i3]
                        if pegs(guess, checksecret, algo_choice) == feedback:
                            checklst.append(checksecret)
        # de mogelijke opties  worden in de lijst geplaatst
        currentoption = [item for item in currentoption if item in checklst]

        if len(currentoption)>1:
            for i in currentoption:
                counter = 0
                for y in currentoption:
                    tempfb = tuple(pegs(y,i,algo_choice))
                    temptuple = tuple(i)
                    counter+=1
                comboding = (tempfb,counter)
                matrix={temptuple:comboding}
                print(matrix)






startgame()
