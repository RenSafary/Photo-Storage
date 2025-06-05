package send_temp_link

import (
	"fmt"
	"net/http"
	//"github.com/gorilla/mux"
)

func HandleGetLink(w http.ResponseWriter, r *http.Request) {
	//vars := mux.Vars(r)
	user := r.FormValue("username")
	urlParam := r.FormValue("url")

	fmt.Println(user, urlParam)

	w.WriteHeader(http.StatusOK)
}
