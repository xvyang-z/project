package server

import (
	"github.com/google/uuid"
	"sse/client"
	"sse/topic"
	"sync"
	"time"
)

type server struct {
	TopicQuene chan *topic.Topic

	TopicTitle2ClientMap sync.Map //线程安全map, 替换 map[topic.TopicTitle]map[uuid.UUID]*client.Client
}

func (s *server) Start() {
	for {
		select {
		case topic_ := <-s.TopicQuene:
			value, _ := s.TopicTitle2ClientMap.Load(topic_.Title)
			clientMap := value.(*sync.Map)

			clientMap.Range(func(uuid_ any, client_ any) bool {
				go func() {
					uuid_ := uuid_.(uuid.UUID)
					client_ := client_.(*client.Client)

					// 对于已经关闭的client, 不会从 client_.MsgChan 取出数据, 这时又有新消息到来会阻塞, 10s后删除该链接
					select {
					case client_.MsgChan <- topic_:
						println("放入 topic", uuid_.String())

					case <-time.After(10 * time.Second):
						clientMap.Delete(uuid_)
						println("offline", uuid_.String(), CountSyncMap(clientMap))
					}

				}()

				return true
			})
		}
	}
}

var Server = &server{
	TopicQuene:           make(chan *topic.Topic),
	TopicTitle2ClientMap: sync.Map{},
}

func CountSyncMap(m *sync.Map) int {
	count := 0
	m.Range(func(key, value interface{}) bool {
		count++
		return true
	})
	return count
}
