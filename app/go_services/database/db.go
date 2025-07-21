package database

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

func DB_Conn() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", "/home/not-home/Git/Photo-Storage/db.sqlite")
	if err != nil {
		return nil, err
	}

	if err = db.Ping(); err != nil {
		db.Close()
		return nil, err
	}

	return db, nil
}
