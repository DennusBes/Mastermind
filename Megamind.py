# Bron 1: https://stackoverflow.com/questions/20302682/mastermind-in-python
# Bron Levi Verhoef

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
        Secretcode = [random.randint(0,5) for i in range(4)]
        print(f'Dit is de code dmv random {Secretcode}')
    algo_choice = int(input("Welk algorithme wil je gebruiken?\n0=user input, 1=worst case strategy, 2=simple strategy, 3=Supercoole custom strat"))
    selectalgo(algo_choice)


def selectalgo(algo_choice):
    # variable die aangeeft welk algoritme gebruikt word
    # waarde 0 = user input
    # waarde 1 = worst case strategy
    # waarde 2 = simple strategy
    if algo_choice==0:
        breakit()
    elif algo_choice==1:
        worstcasestrat(Secretcode)
    elif algo_choice == 2:
        simplestrat(Secretcode)
    elif algo_choice == 3:
        customstrat(Secretcode)

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
        print(f'guess: {guess} feedback:{feedback}')

        #als de feedback [4,0] is, is het algoritme klaar
        if feedback == [4,0]:
            print(f'GGWP GAMER, het heeft {count} turns gekost')
            print(f'De code was {guess}.')
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
        print(len(currentoption))



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
    alloption.remove(guess)
    if guess in currentoption:
        currentoption.remove(guess)
    count += 1
    feedback = pegs(guess, Secretcode, algo_choice)
    print(f'guess: {guess} feedback:{feedback}')
    if feedback == [4, 0]:
        print(f'Hole in one!')
        quit()

    while True:

        # als de feedback [4,0] is, is het algoritme klaar
        if feedback == [4, 0]:
            print(f'GGWP GAMER, het heeft {count} turns gekost')
            with open('results.txt', "a") as f:  # append the results to a txt file, probably not in final product
                f.write(f'{count}\n')
                f.close()
            break

        # Hier wordt een lijst gemaakt waar alle mogelijke codes worden getest tegen de guess
        checklst = []
        for checksecret in currentoption:
            if pegs(guess, checksecret, algo_choice) == feedback:
                checklst.append(checksecret)
        # de mogelijke opties  worden in de lijst geplaatst
        currentoption = [item for item in currentoption if item in checklst]

        if len(currentoption) > 2:
            maxcodecount={}
            for maybeguess in alloption:
                matrix={}
                for maybesecret in currentoption:
                    tempfb = tuple(pegs(maybeguess, maybesecret, algo_choice))
                    try:
                        matrix[tempfb] += 1
                    except:
                        matrix[tempfb] = 1

                    maxcodecount[tuple(maybeguess)]=max(matrix.values())

            minikey = min(maxcodecount.values())
            possibilities = [ code for code in maxcodecount.keys() if maxcodecount[code] == minikey]

            for posibility in possibilities:
                if posibility in currentoption:
                    guess = posibility
                else:
                    guess = possibilities[0]
            guess = list(guess)
            alloption.remove(guess)
            if guess in currentoption:
                currentoption.remove(guess)

            count += 1
            feedback = pegs(guess, Secretcode, algo_choice)
            print(f'guess: {guess} feedback:{feedback}')
        else:
            guess = currentoption[0]
            count += 1
            feedback = pegs(guess, Secretcode, algo_choice)
            alloption.remove(guess)
            if guess in currentoption:
                currentoption.remove(guess)
            print(f'guess: {guess} feedback:{feedback}')

def customstrat(Secretcode):
    '''
    Elimineer de mogelijke waardes
    Mijn idee voor dit algoritme is als volgt:
    1. Er wordt een rij met eendezelfde waarde als gok gebruikt.
    2. Er word opgeslagen hoe vaak de secretcode de gegokte kleur bevat.
    3. Ga terug naar stap 1 als er nog waardes zijn die niet zijn getest.
    5. Er is nu feedback verkregen. De combinatie van de feedback zal zorgen voor een combinatie van gekleurde en witte pegs, waarvan er som 4 is.
    6. Maak nu een lijst met alle mogelijk codes aan de hand van de totale feedback.
    7. Probeer alle opties in de lijst. ( In het geval dat er 4 verschillende waardes zijn gebruikt in de code, is het totaal aantal mogelijkheden 4 * 3 * 2 * 1 = 24)
    8. Doel bereikt. GGWP.
    '''
    #Ik maak een dictionary waarin staat hoevaak de key ( Waarde 0 t/m 5 ) voor komst
    count = 0
    kleurenteller ={}
    for posiblenumbas in range(0,6,1):
        totalamount=0
        guess = [posiblenumbas,posiblenumbas,posiblenumbas,posiblenumbas]
        count += 1
        feedback = pegs(guess, Secretcode, algo_choice)
        totalamount = feedback[0] + feedback[1]
        if feedback == [4, 0]:
            print(f'De code was vrij simpel blijkbaar. Alsnog goed gedaan hoor  :) ')
            quit()
        if totalamount>0:
            kleurenteller[posiblenumbas]=totalamount
    #print(kleurenteller)
    usednumbers = []
    while len(usednumbers) < 4:
        for getal in kleurenteller:
            if kleurenteller[getal] >=1:
                usednumbers.append(getal)
                kleurenteller[getal] -= 1

    stage1 = []
    stage2 = []
    stage3 = []
    finalboss = []

    for i0 in range(len(usednumbers)):
        tempcop = usednumbers.copy()
        stage1 =tempcop[i0]
        tempcop.remove(stage1)
        for i1 in range(len(tempcop)):
            stage2cop=tempcop.copy()
            stage2 = stage2cop[i1]
            stage2cop.remove(stage2)
            for i2 in range(len(stage2cop)):
                stage3cop = stage2cop.copy()
                stage3 = stage3cop[i2]
                stage3cop.remove(stage3)
                for i3 in range(len(stage3cop)):
                    stage4cop = stage3cop.copy()
                    finalboss.append([stage1,stage2,stage3,stage4cop[i3]])
    for option in finalboss:
        count+=1
        if pegs(option,Secretcode,algo_choice) == [4,0]:
            print(f'Blijkbaar was {option} de geheime code!')
            print(f'GGWP GAMER, het heeft {count} turns gekost')
            quit()


startgame()
