package redis

import (
	"context"

	"github.com/redis/go-redis/v9"
)

type RedisCli struct {
	Client *redis.Client
}

func RedisClient() (*redis.Client, context.Context) {
	var ctx = context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})

	return rdb, ctx
}

func NewRedisDB(rdb *redis.Client) *RedisCli {
	return &RedisCli{
		Client: rdb,
	}
}
