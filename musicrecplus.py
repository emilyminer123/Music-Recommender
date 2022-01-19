"""
@author Emily Miner

"""

userData = {}
privateUserData = {}


def loadFiles():
    """Load file from musicrecplus.txt and save it in the global variable userData. Easiest to use usernames as the keys and arrays of artists as the values."""
    global userData
    global privateUserData
    try:
        data = open("musicrecplus.txt", 'r')
        f = data.readlines()
        for user in f:
            name = ''
            artists = ''
            for i in range(0,len(user)):
                if user[i] != ':':
                    name += user[i]
                else:
                    for x in range(i+1,len(user)):
                        artists += user[x]
                    if '$' in name:
                        privateUserData[name] = artists.strip("\n")
                    else:
                        userData[name] = artists.strip("\n")
                    break
        data.close()
    except IOError:
        data = open("musicrecplus.txt","w+")
        data.close()

def artistListMaker(artistString):
    """Takes in a string and converts it to a list"""
    if artistString == '':
        return []
    else: 
        artist = ''
        artistsList = []
        for x in range(0,len(artistString)):
            if artistString[x] == ",":
                artistsList += [artist]
                artist = ''
            else:
                artist += artistString[x]
        artistsList += [artist]
        return artistsList



def setPreferences(userName):
    """Prompts the user to input their preferences (with input function), and overwrites the old ones.
    Directly modify userData."""
    global userData
    global privateUserData
    
    def loop(userName,artists,stringArtists):
        """Helper function"""
        a = input("Enter an artist that you like (Enter to finish):\n")
        if a != '':
            artists += [a]
            loop(userName,artists,stringArtists)
        else:
            for i in range(0,len(artists)):
                if i == (len(artists)-1):
                    stringArtists += artists[i]
                else:
                    stringArtists += artists[i] + ','
            if '$' in userName:
                privateUserData[userName] = stringArtists
            else:
                userData[userName] = stringArtists
    return loop(userName,[],'')

def bestMatch(username):
    """Finds the user with the most similar music taste as the user"""
    try: userArtists = artistListMaker(userData[username])
    except: return []
    if userArtists == []:
        return []
    else:
        similarityDct = {}
        similarity = 0
        for user in userData:
            listArtists = artistListMaker(userData[user])
            if (listArtists != userArtists):
                for i in listArtists:
                    if i in userArtists:
                        similarity += 1
                if similarity != len(listArtists):
                    similarityDct[user] = similarity
                similarity = 0
        if similarityDct != {}:
            L=[]
            for i in similarityDct:
                L.append((similarityDct[i],i))
            L.sort()
            L.reverse()
            return (max(L))[1]
        else:
            return []
            

def getRecommendations(username):
    """Gets artist recommendations from public users and prints them."""
    if bestMatch(username) == []:
        print("No recomendations available at this time")
    else:
        matchingUser = artistListMaker(userData[bestMatch(username)])
        userListOfArtists = artistListMaker(userData[username])
        for i in matchingUser:
            if i not in userListOfArtists:
                print(i)


def calculatesSongPopularity():
    """Calculates the popularity of an artist"""
    occurances = {}
    for user in userData:
        artistsString = userData[user]
        artist = ''
        if userData[user] != '':
            for char in artistsString:
                if char != ",":
                    artist += char
                else:
                    if artist in occurances:
                        occurances[artist]+=1
                    else:
                        occurances[artist]=1
                    artist = ''
            if artist in occurances:
                occurances[artist]+=1
            else:
                occurances[artist]=1
    L=[]
    for i in occurances:
        L.append((occurances[i],i))
    L.sort()
    L.reverse()
    return L

def getPopular(userName):
    """Prints the most popular artist(s)."""
    L = calculatesSongPopularity()
    if L == []:
        print("Sorry, no artists found.")
    else:
        a = max(L)
        for i in L[0:3]:
            if i[0] == a[0]:
                print(i[1])

def getHowPopular(userName):
    """Prints how popular the most popular artist is."""
    L = calculatesSongPopularity()
    if L == []:
        print("Sorry, no artists found.")
    else:
        print(L[0][0])


def getMostUser(userName):
    """Prints the public user who likes the most music."""
    numberOfSongs = {}
    for user in userData:
        artist = ''
        if userData[user] != '':
            for char in userData[user]:
                if char != ",":
                    artist += char
                else:
                    try: numberOfSongs[user]+=1
                    except: numberOfSongs[user]=1
                    artist = ''
            try: numberOfSongs[user]+=1
            except: numberOfSongs[user]=1
    L=[]
    for i in numberOfSongs:
        L.append((numberOfSongs[i],i))
    L.sort()
    a = max(L)
    for i in L:
        if i[0] == a[0]:
            print(i[1])


def saveData():
    """Save data from userData into file"""
    open("musicrecplus.txt", 'w').close()
    data = open("musicrecplus.txt", 'r+')
    for user in userData:
        data.write(user+':'+userData[user]+"\n")
    for user in privateUserData:
        data.write(user+':'+privateUserData[user]+"\n")
    data.close()


def menuInput():
    """Get user input from main menu"""
    menu = \
        '''Enter a letter to choose an option:
e - Enter preferences
r - Get recommendations
p - Show most popular artists
h - How popular is the most popular
m - Which user has the most likes
q - Save and quit
'''
    return input(menu)


# dictionary defined commands
userPossibleChoices = {
    'e': setPreferences,
    'r': getRecommendations,
    'p': getPopular,
    'h': getHowPopular,
    'm': getMostUser
}


def main():
    """main function for music recommender"""
    # load data
    loadFiles()

    #get username
    username = input('Enter your name (put a $ symbol after your name if you wish your preferences to remain private):\n')
    
    # initialize new user if does not exist
    if username not in userData:
        if username not in privateUserData:
            setPreferences(username)
            
    # begin program functionality using a while loop
    while(True):
        userChoice = menuInput()
        if userChoice in userPossibleChoices:
            userPossibleChoices[userChoice](username)
        elif userChoice == 'q':
            saveData()
            break
        else:
            print("Invalid command, try again.")


if __name__ == "__main__":
    main()
