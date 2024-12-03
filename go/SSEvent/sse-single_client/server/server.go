package server

import (
	"sse/topic"
)

type server struct {
	TopicQuene chan *topic.Topic

	Topic2Client map[topic.TopicTitle]map[string]chan *topic.Topic
}

func (s *server) Start() {
	for {
		select {
		case topic_ := <-s.TopicQuene:
			for _, topicChan := range s.Topic2Client[topic_.Title] {
				topicChan <- topic_
			}
		}
	}
}

var Server = &server{
	TopicQuene:   make(chan *topic.Topic),
	Topic2Client: make(map[topic.TopicTitle]map[string]chan *topic.Topic),
}
