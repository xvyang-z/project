package handle

import (
	"fmt"
	"github.com/gin-gonic/gin"
)

func Index(c *gin.Context) {
	user := c.Query("user")
	topics := c.Query("topics")

	c.Writer.WriteString(fmt.Sprintf(`
			<!doctype html>
			<html lang="en">

			<head>
					<meta charset="UTF-8">
					<title>Server Sent Event</title>
			</head>

			<body>
			<div>Topic Messages:</div>
			<div id="event-data"></div>
			</body>

			<script>
					// EventSource object of javascript listens the streaming events from our go server and prints the message.
					var stream = new EventSource("/sub?user=%s&topics=%s");
					stream.onmessage = function(e){
						var eventData = document.createTextNode(e.data);
						var br = document.createElement("br");
						document.getElementById('event-data').appendChild(eventData);
						document.getElementById('event-data').appendChild(br);
					};
			</script>

			</html>`, user, topics))
}
