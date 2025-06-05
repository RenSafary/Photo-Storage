package main

import (
	"fmt"
	"github.com/gorilla/mux"
	"go_services/send_temp_link"
	"net/http"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/Photo-Storage/api/send-link", send_temp_link.HandleGetLink).Methods("POST")

	fmt.Println("Сервер запущен на http://127.0.0.1:8080")
	http.ListenAndServe(":8080", r)
}
