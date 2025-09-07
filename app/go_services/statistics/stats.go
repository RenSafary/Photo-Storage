package statistics

import (
	"fmt"
	"go_services/models"
	"html/template"
	"net/http"

	"github.com/gorilla/mux"
)

func GetData(username string) (*models.User, error) {
	user, err := models.CachedUser(username)
	if err != nil {
		return nil, err
	}

	return user, nil
}

func Calculations() {

}

func ShowStats(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	w.Header().Set("Content-Type", "text/html")

	vars := mux.Vars(r)
	username := vars["username"]
	user, err := GetData(username)
	if err != nil {
		fmt.Println("Error getting user data:", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}
	fmt.Println("User data:", user)

	templatePath := "../templates/stats/stats.html"

	tmpl, err := template.ParseFiles(templatePath)
	if err != nil {
		fmt.Println("Error parsing template:", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, nil)
	if err != nil {
		fmt.Println("Error executing template:", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}
}
