'''
A simple pokemon video game (Safari Zone Simulator) with GUI written in python using the tkinter library.
Created by Jack Tschetter, all rights reserved.
For instructions on how to play and run the game refer to the files readme.pdf, and dependencies.txt.
'''
import tkinter as tk
import random

#assumes each of the instance variables will be a list
class Pokemon:
    def __init__(self,species_name,dex_number,catch_rate,speed):
        get_a_random_number = random.randint(0,150)
        self.species_name = species_name[get_a_random_number]
        self.dex_number = dex_number[get_a_random_number]
        self.catch_rate = catch_rate[get_a_random_number]
        self.speed = speed[get_a_random_number]
        
    def __str__(self):
        return str(self.species_name)

    def name(self):
        return str(self.species_name)

    def dex(self):
        return str(self.dex_number)
    
    def rate(self):
        return int((min((int(self.catch_rate)+1),151)/449.5)*100)

    def angeredCatchRate(self):
        if self.rate() < 33:
            return int(self.rate() * 2)
        else:
            return str(self.rate())

    def speed(self):
        return str(self.speed())

    def escapeRate(self):
        return int((int(2*self.speed)/256))
    
    def angeredEscapeRate(self):
        return int(int(min(255,4*int(self.speed)))/256 *100)
    
    def eatingEscapeRate(self):
        return int(self.speed)/2/256 *100

    def eatingCatchRate(self):
        return int(self.rate()/2)


class SafariSimulator(tk.Frame):
    def __init__(self,master=None):
        self.startingballs = 30
        self.Angry = False
        self.Eating = False
        self.turnsAngry = 0
        self.turnsEating = 0
        self.dex = []
        self.name = []
        self.catch_rate = []
        self.speed = []
        fileobj = open('pokedex.csv','r')
        lines_read = fileobj.readlines()
        lines_read.remove('Dex,Pokemon,Catch Rate,Speed\n')
        lines_read.remove('122,Mr. Mime,45,50\n')
        for i in lines_read:
            var = i.split()
            for j in var:
                new = j.split(',')
                self.dex.append(new[0])
                self.name.append(new[1])
                self.catch_rate.append(new[2])
                self.speed.append(new[3])
        self.dex.insert(121,122)
        self.name.insert(121,'Mr. Mime')
        self.catch_rate.insert(121,45)
        self.speed.insert(121,57)
        self.pokemon_captured = []

        tk.Frame.__init__(self, master)
        master.minsize(width=400, height=350)
        master.maxsize(width=400, height=350)
        master.title("Safari Zone Simulator")
        self.grid()
        self.createWidgets()
        self.nextPokemon()
        self.currentPokemon()

    def createWidgets(self):
        self.pokemon = Pokemon(self.name,self.dex,self.catch_rate,self.speed)

        self.throwBallsButton = tk.Button(self)
        self.throwBallsButton["text"] = 'Throw Safari Ball (30 left)'
        self.throwBallsButton["command"] = self.throwBall
        self.throwBallsButton.grid(row=0,column=0,padx=0,sticky='w',ipadx=10)

        self.throwRocksButton = tk.Button(self)
        self.throwRocksButton["text"] = 'Throw rock'
        self.throwRocksButton["command"] = self.throwRocks
        self.throwRocksButton.grid(row=1,column=0,sticky='w',ipadx=58)

        self.throwBaitButton = tk.Button(self)
        self.throwBaitButton['text'] = 'Throw bait'
        self.throwBaitButton["command"] = self.throwBait
        self.throwBaitButton.grid(row=0,column=1,ipadx=60)

        
        self.runButton = tk.Button(self)
        self.runButton["text"] = "Run Away"
        self.runButton["command"] = self.nextPokemon
        self.runButton.grid(row=1,column=1,ipadx=60)

        # self.attackButton = tk.Button(self)
        # self.attackButton["text"] = "Attack with santa!"
        # self.attackButton["command"] = self.nextPokemon
        # self.attackButton.grid(row=2,column=0,ipadx=60)

        self.messageLabel = tk.Label(bg="grey", text= 'You encounter a wild ' + str(self.pokemon.name()))
        self.messageLabel.place(x = 0, width = 400, y = 60, height = 30)

        if self.Eating == True:
            self.catchProbLabel = tk.Label(bg="#F0FFFF", text= 'Your chance of catching it is ' + str(self.pokemon.eatingCatchRate()) + '%!')
            self.catchProbLabel.place(x=0,y=290,width=400,height=30)
        elif self.Angry == True:
            self.catchProbLabel = tk.Label(bg="#F0FFFF", text= 'Your chance of catching it is ' + str(self.pokemon.angeredCatchRate()) + '%!')
            self.catchProbLabel.place(x=0,y=290,width=400,height=30)
        else:
            self.catchProbLabel = tk.Label(bg="#F0FFFF", text= 'Your chance of catching it is ' + str(self.pokemon.rate()) + '%!')
            self.catchProbLabel.place(x=0,y=290,width=400,height=30)

        self.escapeProbLabel = tk.Label(bg="#F0F8FF", text= 'Its chance of running away is ' + str(self.pokemon.escapeRate()) + '%!')
        self.escapeProbLabel.place(x=0,y=320,width=400,height=30)

        file_string = ['sprites/',str(self.pokemon.dex()),'.gif']
        file_string_new = ''.join(file_string)

        self.image = tk.PhotoImage(file = file_string_new)
        self.image_label = tk.Label(self)
        self.image_label["image"] = self.image
        self.image_label.grid(pady=40,padx=95,columnspan=4)
       
    def nextPokemon(self):
        self.pokemon = Pokemon(self.name,self.dex,self.catch_rate,self.speed)
        self.messageLabel['text'] = 'You encounter a wild ' + str(self.pokemon.name())


        self.catchProbLabel['text'] = 'Your chance of catching it is ' + str(self.pokemon.rate()) + '%!'
        self.escapeProbLabel['text'] = 'Its chance of running away is ' + str(self.pokemon.escapeRate()) + '%!'

        file_string = ['sprites/',str(self.pokemon.dex_number),'.gif']
        file_string_new = ''.join(file_string)

        self.image = tk.PhotoImage(file = file_string_new)
        self.image_label["image"] = self.image
        self.image_label.grid(pady=40,padx=95,columnspan=4)

    def currentPokemon(self):
        # self.pokemon = Pokemon(self.name,self.dex,self.catch_rate,self.speed)
        self.messageLabel['text'] = 'You encounter a wild ' + str(self.pokemon.name())

        self.catchProbLabel['text'] = 'Your chance of catching it is ' + str(self.pokemon.angeredCatchRate()) + '%!'
        self.escapeProbLabel['text'] = 'Its chance of running is ' + str(self.pokemon.angeredEscapeRate()) + '%!'

        file_string = ['sprites/',str(self.pokemon.dex_number),'.gif']
        file_string_new = ''.join(file_string)

        self.image = tk.PhotoImage(file = file_string_new)
        self.image_label["image"] = self.image
        self.image_label.grid(pady=40,padx=95,columnspan=4)

    # def clearPokemon(self):
    #     self.image_label.grid_forget()
    #     self.messageLabel.place_forget()
    #     self.catchProbLabel.place_forget()
    #     self.escapeProbLabel.place_forget()

#The GUI has two ways to differentiate captured, and escaped pokemon
#If a pokemon escapes the message label is updated for 1750 miliseconds
#If a pokemon is captured the capture message label is updated for 1750 miliseconds
#Only if a pokemon is captured the safari ball is displayed for 1750 miliseconds
#The safari ball display is in addition to the message change

#Throw rock method sets self.Eating to False
#Because self.Eating, and self.Angered can not both be true
#Throw rocks updates the catchProb, and escapeProb labels accordingly

    def throwRocks(self):

        a_random_number = random.randint(0,1)
        self.Eating = False
        self.turnsAngry + random.randint(1,5)

        self.newImage = tk.PhotoImage(file = 'sprites/rock.gif')
        # self.image_label.grid(pady=90,padx=150,columnspan=4)
        # self.image_label["image"] = self.newImage

        if self.turnsAngry > 0:
            self.Angry = True
        if int(self.pokemon.escapeRate()) > int(100* a_random_number): #Case where pokemon does escape.
            self.image_label.grid(pady=90,padx=90,columnspan=4)
            self.image_label["image"] = self.newImage
            self.messageLabel['text'] = 'Oh no it escaped'
            self.messageLabel.after(2000,self.nextPokemon) #Changed from 1750
        else:
            self.image_label.grid(pady=90,padx=150,columnspan=4)
            self.image_label["image"] = self.newImage

            self.messageLabel.after(2000,self.currentPokemon) #Changed from 1750

            self.catchProbLabel['text'] = 'Your chance of catching it is ' + str(self.pokemon.angeredCatchRate()) + '%!'
            self.escapeProbLabel['text'] = 'Its chance of running is ' + str(self.pokemon.angeredEscapeRate()) + '%!'
     

    def throwBait(self):
        a_random_number = random.randint(0,1)
        self.Angry = False
        self.turnsEating + random.randint(1,5)

        self.newImage = tk.PhotoImage(file = 'sprites/bait.gif')

        if self.turnsEating > 0:
            self.Eating = True
        if int(self.pokemon.escapeRate()) > int(100* a_random_number):
            # self.image_label.grid(pady=40,padx=0,columnspan=4)
            # self.image_label["image"] = self.newImage
            
            self.messageLabel['text'] = 'Oh no it escaped!'

            self.image_label.grid_forget()

            self.messageLabel.after(2000,self.nextPokemon) #Changed from 1750

        else:
            self.image_label.grid(pady=40,padx=0,columnspan=4)
            self.image_label["image"] = self.newImage
            
            self.catchProbLabel['text'] = 'Your chance of catching it is ' + str(self.pokemon.angeredCatchRate()) + '%!'
            self.escapeProbLabel['text'] = 'Its chance of running is ' + str(self.pokemon.angeredEscapeRate()) + '%!'

            self.messageLabel.after(2000,self.currentPokemon) #Changed from 1750

    def throwBall(self):
        self.turnsAngry - 1
        self.turnsEating - 1
        if self.startingballs > 0:
            self.startingballs -= 1
            self.throwBallsButton["text"] = "Throw Safari Ball (" + str(self.startingballs) + " left)"
            if self.Angry == True:
                a_random_number = random.randint(0,1)
                if int(self.pokemon.angeredCatchRate()) < int(100* a_random_number):
                    self.newImage = tk.PhotoImage(file = 'sprites/safari_ball.gif')
                    self.image_label.grid(pady=90,padx=150,columnspan=4)
                    self.image_label["image"] = self.newImage
                    self.messageLabel['text'] = 'The pokemon was captured!'
                    self.pokemon_captured.append(self.pokemon.name())
                    self.image_label.after(1750,self.nextPokemon)
                else:
                    if int(self.pokemon.angeredEscapeRate()) > int(100* a_random_number):
                        self.escapeProbLabel['text'] = 'Oh no it escaped'
                        self.escapeProbLabel.after(1750,self.nextPokemon)
            elif self.Eating == True:
                a_random_number = random.randint(0,1)
                if int(self.pokemon.eatingCatchRate()) < int(100* a_random_number):
                    self.newImage = tk.PhotoImage(file = 'sprites/safari_ball.gif')
                    self.image_label.grid(pady=90,padx=150,columnspan=4)
                    self.image_label["image"] = self.newImage
                    self.messageLabel['text'] = 'The pokemon was captured!'
                    self.pokemon_captured.append(self.pokemon.name())
                    self.image_label.after(1750,self.nextPokemon)
                else:
                    if int(self.pokemon.eatingEscapeRate()) > int(100* a_random_number):
                        self.escapeProbLabel['text'] = 'Oh no it escaped'
                        self.escapeProbLabel.after(1750,self.nextPokemon)
            else:
                a_random_number = random.randint(0,1)
                if int(self.pokemon.rate()) < int(100* a_random_number):
                    self.newImage = tk.PhotoImage(file = 'sprites/safari_ball.gif')
                    self.image_label.grid(pady=90,padx=150,columnspan=4)
                    self.image_label["image"] = self.newImage
                    self.messageLabel['text'] = 'The pokemon was captured!'
                    self.pokemon_captured.append(self.pokemon.name())
                    self.image_label.after(1750,self.nextPokemon)
                else:
                    if int(self.pokemon.escapeRate()) > int(100* a_random_number):
                        self.messageLabel['text'] = 'Oh no it escaped!'

                        self.image_label.grid_forget()

                        self.messageLabel.after(1750,self.nextPokemon)                
        else:
            self.endAdventure()
            
    def endAdventure(self):
        caught = '\n'.join(self.pokemon_captured)
        self.throwBallsButton.grid_forget()
        self.throwBaitButton.grid_forget()
        self.throwRocksButton.grid_forget()
        self.runButton.grid_forget()
        self.image_label.grid_forget()
        self.messageLabel.place_forget()
        self.catchProbLabel.place_forget()
        self.escapeProbLabel.place_forget()
        self.closingLabel = tk.Label(bg="white", text= 'You are all out of balls, hope you had fun!')
        self.closingLabel.place(x=0,width=400,y=30, height=30)
        self.catchLabel = tk.Label(bg="white")
        if len(self.pokemon_captured) > 0:
            self.catchLabel['text'] = 'You caught ' + str(len(self.pokemon_captured)) + ' pokemon:' +'\n' + str(caught)
            self.catchLabel.place(x=0,width=400,y=60)
        else:
            self.catchLabel['text'] = 'Oops you caught 0 pokemon!'
            self.catchLabel.place(x=0,width=400,y=60)

app = SafariSimulator(tk.Tk())
app.mainloop()
