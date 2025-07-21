package main

import (
	"fmt"
	"go_services/send_temp_link"
	"go_services/stories"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/gallery/api/share_file/", send_temp_link.HandleGetLink).Methods("POST")
	r.HandleFunc("/gallery/api/stories/{username}/", stories.Get_Images).Methods("GET")

	fmt.Println("Server started on http://127.0.0.1:8080")
	http.ListenAndServe(":8080", r)
}
