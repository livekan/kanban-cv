# LiveKan Backend

## Overview

This is the backend server that mediates and stores the data between our CV system and web-app.
Our web-app uses React to display the data and is expecting a certain data
model from the CV. The front-end could do a few routes but will mostly be
interacting with the ML layer of this backend.

This backend is structured in three layers, first a API interface where the CV camera
POST's information to this server. When information is posted, it is stored in a
in a PostgreSQL database.

In PostgreSQL, events are stored in a chronological
fashion. (Our storage system works like a traditional database but the methodology
behind it is one of a CQRS model.) Separate of that, we have a users DB.

The users DB has events that user does and has data tied to them where we can
run analytics on the program.

## How to get up and running

First install node if you haven't

Then run `npm install`
Then run `node server.js`

This will start a instance of the backend server

_In it's current iteration, we don't have auto packagers installed.
Documentation pending on the ML layer._

## Routes

__CV__

#### POST/createboard

Sends JSON that looks like the following

```
{
"channels": [
  {
    "title": "Later",
    "titleid": "1"
    "notes": [
      {
        "taskid": "1",
        "color": "#FA351B  ",
        "desc": "Create Spring Notes",
        "assignee": ""
      },
      {
        "taskid": "2",
        "color": "#1B87FA  ",
        "desc": "Email Devin Action Items Discussed",
        "assignee": ""
      }
    ]
  },
  {
    "title": "Upcoming",
    "titleid": "2"
    "notes": [
      {
        "taskid": "3",
        "color": "#BBFA1B  ",
        "desc": "Call Onstar to Confirm Cancellation",
        "assignee": ""
      },
      {
        "taskid": "4",
        "color": "#F21BFA  ",
        "desc": "Buy LED Light Bulbs",
        "assignee": ""
      }
    ]
  }
]
}
```

Returns a 200 when created

Our server parses this data and stores it.

Assignee is left empty.

Description is most likely left blank

Color could associate with a assignee


#### GET/getboard

Gets a picture of the board when last updated. The jpg photo is sent in a JSON
object link.

```
{
  "boardphoto":[
    {"photoid":"1", "photolink":"ip".photo.jpg", }
]
}
```

#### GET/imageofidx

Gets a picture of the note when requested. The jpg photo is sent in a JSON
object.

Place holder image

```
{
    {"idx":"1", "idxphoto":("ip".photo.jpg")}
]
}
```
