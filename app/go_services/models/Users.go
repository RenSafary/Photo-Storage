package models

import (
	"database/sql"
	"fmt"
	"go_services/database"
	"go_services/redis"
	"log"
)

func RedisUser(user string) error {
	// redis
	rdb, ctx, err := redis.RedisClient()
	if err != nil {
		return fmt.Errorf("redis connection failed: %w", err)
	}
	defer rdb.Close()

	// database
	db, err := database.DB_Conn()
	if err != nil {
		return fmt.Errorf("database connection failed: %w", err)
	}
	defer db.Close()

	var userID int
	err = db.QueryRowContext(ctx, "SELECT id FROM Users WHERE username = ?", user).Scan(&userID)
	if err != nil {
		if err == sql.ErrNoRows {
			return fmt.Errorf("user not found")
		}
		return fmt.Errorf("query failed: %w", err)
	}

	log.Printf("Found user ID: %d", userID)
	return nil
}
