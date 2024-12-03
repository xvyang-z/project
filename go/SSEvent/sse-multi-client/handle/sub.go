package handle

import (
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"io"
	"sse/client"
	"sse/server"
	"sse/topic"
	"strconv"
	"strings"
	"sync"
)

func Sub(c *gin.Context) {
	uuid_ := uuid.New()
	id, _ := strconv.ParseUint(c.Query("id"), 10, 64)
	topics := c.Query("topics")

	client_ := &client.Client{Id: id, MsgChan: make(chan *topic.Topic)}

	for _, topicTitle := range strings.Split(topics, "|") {
		title := topic.TopicTitle(topicTitle)

		value, _ := server.Server.TopicTitle2ClientMap.Load(title)
		clientMap, _ := value.(*sync.Map)
		if clientMap == nil {
			server.Server.TopicTitle2ClientMap.Store(title, &sync.Map{})
		}

		// 这里需要重新 Load, 不能直接用上面的 clientMap
		value, _ = server.Server.TopicTitle2ClientMap.Load(title)
		clientMap, _ = value.(*sync.Map)
		clientMap.Store(uuid_, client_)
		println("online", uuid_.String(), server.CountSyncMap(clientMap))
	}

	// Stream message to client
	c.Stream(func(w io.Writer) bool {
		if message, ok := <-client_.MsgChan; ok {
			c.SSEvent("message", message)
			return true
		}
		return false
	})
}
