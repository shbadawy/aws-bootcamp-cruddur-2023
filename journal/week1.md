# Week 1 — App Containerization
I have done the following :
* Added the documentation of the notification API to the openAPI file.

```
/api/activities/notifications:
    get:
      description: 'Return activities for the people we are following'
      parameters: []
      tags:
        - activities
      responses:
        '200':
          description: Return list of activities for the people we are following
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Activity'
```

## Backend part:
  * Added the notification route to the app.py file 
  
``` 
from services.notifications_activities import *

@app.route("/api/activities/notifications", methods=['GET'])
def notificaitons_handle():
model = NotificationsActivities.run()
if model['errors'] is not None:
  return model['errors'], 422
else:
  return model['data'], 200
```

  * Created [Notification service](../backend-flask/services/notifications_activities.py)

## Front-end part:
  * Added notification route to frontend's app.py 
```
   {
    path: "/notifications",
    element: <NotificationPage />
  }
```
  * Created NotificationPage [js](../frontend-react-js/src/pages/NotificationPage.js) and [css](../frontend-react-js/src/pages/NotificationPage.css) files 
  
* Added Postgres and DynamoDB to the [compose file](docker-compose.yml)
