/**
@startuml

hide circle

class announcements{
resultindex
bold
header
text
type
}

class attendees{
eventid
attendee
}

class buttons{
ordr
name
link
image
perms
test
}
class coverage{
stbyindex
stbytype
id
name
coverername
show
}
class crewchiefschedule{
id
mm
dd
yyyy
ccid
}
class dutycrewcoverage{
dcindex
mm
dd
yyyy
name
coverer
show
}

class dutycrewmembers{
mm
yyyy
firstname
lastname
traininglevel
dutycrewnumber
}

class dutycrewschedule{
mm
dd
yyyy
dutycrewnumber
}
class events{
eventid
dd
mm
yyyy
orderdate
time
name
allow_signups
}

class forums{
forumname
forumtext
forumdescription
perms
postid
datetimestamp
username
firstname
lastname
day
month
year
hour
minute
second
message
isold
}

class links{
name
link
show
}
class logintimes{
username
logintime
TSTAMP
isold
}
class meetingmins{
mm
dd
yyyy
minutes
TSTAMP
meeting_index
}
class mtg_mins_content{
mtg_index
section_index
title
content
}

class overall{
service
totallogins
mailman
message
}
class pictures{
album
url
folder
resultindex
caption
leadpic
}
class quizes{
qNum
question
A
B
C
D
correctanswer
answerexplaination
}
class sparky{
datetimestamp
monthyear
name
info
}
class standbys{
standbyid
dd
mm
yyyy
time
type
event
ccpic
active1
active2
prob1
prob2
notes
}
class users{
id
username
password
firstname
privledges
midinitial
lastname
nickname
street
city
state
zip
residence
roomnumber
phonenumber
email
traininglevel
certnumber
memberstatus
portablenumber
comment
mailman
quizqleftoff
hastakenquiz
position
isCrewChief
}
@enduml
**/
