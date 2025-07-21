package redis

import (
	"context"
	"fmt"
	"log"

	"github.com/redis/go-redis/v9"
)

type RedisCli struct {
	Client *redis.Client
	Ctx    context.Context
}

func RedisClient() (*redis.Client, context.Context, error) {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})

	if err := rdb.Ping(ctx).Err(); err != nil {
		return nil, nil, fmt.Errorf("redis ping failed: %w", err)
	}

	log.Println("Redis connected successfully")
	return rdb, ctx, nil
}
