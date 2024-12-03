package handle

import (
	"github.com/gin-gonic/gin"
	"sse/server"
	"sse/topic"
)

func Pub(c *gin.Context) {
	t := &topic.Topic{}
	err := c.BindJSON(t)
	if err != nil {
		return
	}

	server.Server.TopicQuene <- t

	c.JSON(200, gin.H{})
}
