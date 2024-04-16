package client

import (
	"sse/topic"
)

type Client struct {
	Name    string
	MsgChan chan *topic.Topic
}
