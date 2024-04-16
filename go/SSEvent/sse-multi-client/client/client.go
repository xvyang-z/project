package client

import (
	"sse/topic"
)

type Client struct {
	Id      uint64 //用户唯一标识符, 这个不能做链接的标识符, 考虑到一个用户开多个链接的情况
	MsgChan chan *topic.Topic
}
