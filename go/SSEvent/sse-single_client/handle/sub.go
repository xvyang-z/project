package handle

import (
	"github.com/gin-gonic/gin"
	"io"
	"sse/client"
	"sse/server"
	"sse/topic"
	"strings"
)

func Sub(c *gin.Context) {
	user := c.Query("user")
	topics := c.Query("topics")

	client_ := &client.Client{Name: user, MsgChan: make(chan *topic.Topic)}

	for _, topicTitle := range strings.Split(topics, "|") {
		title := topic.TopicTitle(topicTitle)
		if server.Server.Topic2Client[title] == nil {
			server.Server.Topic2Client[title] = make(map[string]chan *topic.Topic)
		}
		server.Server.Topic2Client[title][client_.Name] = client_.MsgChan
	}

	// 如果连接端开，删除该客户端
	//defer func() {
	//	delete(server.Server.Topic2Client, client.User)
	//	close(client.C)
	//}()

	// Stream message to client
	c.Stream(func(w io.Writer) bool {
		if message, ok := <-client_.MsgChan; ok {
			c.SSEvent("message", message)
			return true
		}
		return false
	})
}
