package main

import (
	"github.com/gin-gonic/gin"
	"sse/handle"
	"sse/server"
)

func init() {
	go server.Server.Start()
}

func main() {
	r := gin.Default()
	r.GET("/", handle.Index)

	// 订阅话题消息
	r.GET("sub", handle.Sub)

	// 发布话题消息
	r.POST("pub", handle.Pub)
	r.Run(":8000")
}
