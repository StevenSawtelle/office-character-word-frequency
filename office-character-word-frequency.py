import requests
import re
import matplotlib.pyplot as plt
import numpy as np

#graphs must be this big to see all words
fig_size = plt.rcParams["figure.figsize"] 
fig_size[0] = 16
fig_size[1] = 12

def show_graph(character, name):
  # set up graph
  y_pos = np.arange(len(character))
  # get words and frequency from tuple
  c1 = [f[0] for f in character]
  c2 = [f[1] for f in character]
  # ax needed for putting number on bar graphs
  fig, ax = plt.subplots()
  # set color depending on character
  c = 'black'
  if name == "Michael":
    c = 'black'
  elif name == "Dwight":
    c = 'goldenrod'
  elif name == "Jim":
    c = 'royalblue'
  elif name == "Pam":
    c = 'mediumorchid'
  elif name == "Andy":
    c = 'darkorange'
  elif name == "Kevin":
    c = 'darkgreen'
  elif name == "Angela":
    c = 'dimgray'
  elif name == "Erin":
    c = 'gold'
  elif name == "Oscar":
    c = 'peru'
  elif name == "Darryl":
    c = 'darkblue'
  elif name == "Ryan":
    c = 'sienna'
  elif name == "Phyllis":
    c = 'orchid'
  elif name == "Kelly":
    c = 'hotpink'
  elif name == "Toby":
    c = 'slategrey'
  elif name == "Stanley":
    c = 'firebrick'
  elif name == "Meredith":
    c = 'orange'
  elif line[0] == "Creed":
    c = 'silver'
  # create actual bar graph
  plt.barh(y_pos, c2, align='center', color = c, alpha=0.5)
  width = 0.4
  # label bars with their number
  for i, v in enumerate(c2):
    ax.text(v, i-.3, str(v), color='black', fontweight='bold')
  # generate y tick intervals
  ax.set_yticks(y_pos+width/2)
  # label words
  ax.set_yticklabels(c1, minor=False)
  # x label (y label not given to avoid clutter)
  plt.xlabel('Number of Times')
  # generate title from parameter (other ways to do, this is easiest)
  plt.title('{}\'s most used words'.format(name))
  # set size for plot
  plt.rcParams["figure.figsize"] = fig_size
  # save the fig (comment for debugging)
  plt.savefig('{}.png'.format(name))
  # show the fig (comment for publishing)
  #plt.show()

def top50(character):
  # get list of tuples for each char
  character = [(v, k) for k, v in character.items()]
  # sort the list inversely
  character.sort()
  character.reverse()
  # grab just the top 50 (mostly an arbitrary number)
  character = character[:50]
  # regenerate list of tuples with word first again
  character = [(k, v) for v, k in character]
  return character


#start of actual script

#words to not use
rejects = {"a":1,"about":1,"all":1,"also":1,"and":1,"as":1,"at":1,"be":1,"because":1,"but":1,"by":1,"can":1,"come":1,"could":1,"day":1,"do":1,"even":1,"find":1,"first":1,"for":1,"from":1,"get":1,"give":1,"go":1,"have":1,"he":1,"her":1,"here":1,"him":1,"his":1,"how":1,"I":1,"if":1,"in":1,"into":1,"it":1,"its":1,"just":1,"know":1,"like":1,"look":1,"make":1,"man":1,"many":1,"me":1,"more":1,"my":1,"new":1,"no":1,"not":1,"now":1,"of":1,"on":1,"one":1,"only":1,"or":1,"other":1,"our":1,"out":1,"people":1,"say":1,"see":1,"she":1,"so":1,"some":1,"take":1,"tell":1,"than":1,"that":1,"the":1,"their":1,"them":1,"then":1,"there":1,"these":1,"they":1,"thing":1,"think":1,"this":1,"those":1,"time":1,"to":1,"two":1,"up":1,"use":1,"very":1,"want":1,"way":1,"we":1,"well":1,"what":1,"when":1,"which":1,"who":1,"will":1,"with":1,"would":1,"year":1,"you":1,
            "your":1,"":1,"i":1,"is":1,"are":1,"dont":1,"im":1,"oh":1,"okay":1,"was":1,"right":1,"going":1,"uh":1,"um":1,"something":1,"things":1,"down":1,"over":1,"where":1,"off":1,"lets":1,"theres":1,"off":1,"much":1,"doing":1,"guy":1,"gonna":1,"does":1,"put":1,"why":1,"whats":1,"doesnt":1,"lot":1,"cant":1,"theyre":1,"any":1,"id":1,"wont":1,"own":1,"said":1,"whos":1,"wasnt":1,
            "thats":1,"yeah":1,"am":1,"hey":1,"yes":1,"youre":1,"ok":1,"were":1,"did":1,"an":1,"has":1,"had":1,"really":1,"hes":1,"got":1,"back":1,"didnt":1,"been":1,"ive":1,"shes":1,"ill":1,"us":1,"didnt":1,"should":1,"too":1,"let":1}
# init dicts for each char we care about
michael = {}
dwight = {}
jim = {}
pam = {}
andy = {}
kevin = {}
angela = {}
erin = {}
oscar = {}
darryl = {}
ryan = {}
phyllis = {}
kelly = {}
toby = {}
stanley = {}
meredith = {}
creed = {}

# easiest to track which char is talking and then go from there
# this is what cur_dict is for
cur_dict = None
# iterate through all seasons and episodes(constant for the office)
for season in range(1, 10):
  for episode in range(1,27):
    print(str(season) +" "+str(episode))
    # easiest to set breaks here
    # necessary as the seasons are of different length
    if season == 1 and episode == 7:
      break
    if season == 2 and episode == 23:
      break
    if season == 3 and episode == 24:
      break
    if season == 4 and episode == 15:
      break
    if season == 9 and episode == 24:
      break
    if season == 6 and episode == 25:
      break
    if season == 7 and episode == 25:
      break
    if season == 8 and episode == 25:
      break
    # generate link - officequotes.net requires < 10 to have leading 0
    link = ""
    if episode < 10:
      link = "http://officequotes.net/no{}-0{}.php".format(season,episode)
    else:
      link = "http://officequotes.net/no{}-{}.php".format(season,episode)
    f = requests.get(link)
    
    # clever part - each page assigns bgcolor right before script starts
    # this line saves a lot of time that is otherwise 100% wasted
    txt = f.text[f.text.index("<td bgcolor=\"#FFF8DC\" valign=\"top\">"):]
    # regex to discard all html tags
    txt = re.sub('<[^<]+?>', '', txt)
    # regex to discard stage cues ie) [looks at camera]
    txt = re.sub("\[.*\]", "", txt)
    # split on each line of dialogue
    txt = txt.split('\n')
    
    for t in txt:
      # regex to discard tabs and carriage returns
      t = re.sub('[\t\r]+', '', t)
      # regex to discard all punctuation - needlessly splits up words
      t = re.sub('[^\w\s]','',t)
      # split each line on all the words
      line = t.split(' ')
      cur_dict = None
      if len(line) < 2:
        # ignore non dialogue lines
        pass
      elif line[0] == "random_text":
        # mostly redundant, used to parse out a lot of the info returned
        pass
      elif line[0] == 'Deleted':
        # deleted scenes given at teh end, this episode is over
        break
      # start processing for each character
      elif line[0] == "Michael":
        cur_dict = michael
      elif line[0] == "Dwight":
        cur_dict = dwight
      elif line[0] == "Jim":
        cur_dict = jim
      elif line[0] == "Pam":
        cur_dict = pam
      elif line[0] == "Andy":
        cur_dict = andy
      elif line[0] == "Kevin":
        cur_dict = kevin
      elif line[0] == "Angela":
        cur_dict = angela
      elif line[0] == "Erin":
        cur_dict = erin
      elif line[0] == "Oscar":
        cur_dict = oscar
      elif line[0] == "Darryl":
        cur_dict = darryl
      elif line[0] == "Ryan":
        cur_dict = ryan
      elif line[0] == "Phyllis":
        cur_dict = phyllis
      elif line[0] == "Kelly":
        cur_dict = kelly
      elif line[0] == "Toby":
        cur_dict = toby
      elif line[0] == "Stanley":
        cur_dict = stanley
      elif line[0] == "Meredith":
        cur_dict = meredith
      elif line[0] == "Creed":
        cur_dict = creed
      # now we know character, process rest of line
      if cur_dict != None:
        for i in range(1,len(line)):
          # assume all lowercase for simplicity
          word = line[i].lower()
          # pass if word is boring
          if word in rejects:
            pass
          # if word already said, increment
          elif word in cur_dict:
            cur_dict[word] = cur_dict[word] + 1
          # otherwise, set to 1
          else:
            cur_dict[word] = 1

# finishing up, create all graphs!
# probably an easier way to loop through this, but with names
# I just wanted to get it working
michael = top50(michael)
show_graph(michael, "Michael")

dwight = top50(dwight)
show_graph(dwight, "Dwight")

jim = top50(jim)
show_graph(jim, "Jim")

pam = top50(pam)
show_graph(pam, "Pam")

andy = top50(andy)
show_graph(andy, "Andy")

angela = top50(angela)
show_graph(angela, "Angela")

kevin = top50(kevin)
show_graph(kevin, "Kevin")

erin = top50(erin)
show_graph(erin, "Erin")

oscar = top50(oscar)
show_graph(oscar, "Oscar")

darryl = top50(darryl)
show_graph(darryl, "Darryl")

ryan = top50(ryan)
show_graph(ryan, "Ryan")

phyllis = top50(phyllis)
show_graph(phyllis, "Phyllis")

kelly = top50(kelly)
show_graph(kelly, "Kelly")

toby = top50(toby)
show_graph(toby, "Toby")

stanley = top50(stanley)
show_graph(stanley, "Stanley")

meredith = top50(meredith)
show_graph(meredith, "Meredith")

creed = top50(creed)
show_graph(creed, "Creed")
print("done")
