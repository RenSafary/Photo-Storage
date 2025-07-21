package models

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"go_services/database"
	"go_services/redis"
	"log"
)

type User struct {
	Username string `json:"username"`
}

func CachedUser(user string) (*User, error) {
	var user_rdb User
	// connect to redis
	rdb, ctx, err := redis.RedisClient()
	if err != nil {
		return &user_rdb, fmt.Errorf("redis connection failed: %w", err)
	}
	defer rdb.Close()

	// connect to database
	db, err := database.DB_Conn()
	if err != nil {
		return &user_rdb, fmt.Errorf("database connection failed: %w", err)
	}
	defer db.Close()

	// get user id
	var userID int
	err = db.QueryRowContext(ctx, "SELECT id FROM Users WHERE username = ?", user).Scan(&userID)
	if err != nil {
		if err == sql.ErrNoRows {
			return &user_rdb, fmt.Errorf("user not found")
		}
		return &user_rdb, fmt.Errorf("query failed: %w", err)
	}

	// getting user data
	text := fmt.Sprintf("user_id:%d", userID)
	val, err := rdb.Get(ctx, text).Result()

	if err != nil {
		panic(err)
	}

	err = json.Unmarshal([]byte(val), &user_rdb)
	if err != nil {
		panic(err)
	}

	log.Printf("Found user ID: %d", userID)
	return &user_rdb, nil
}
