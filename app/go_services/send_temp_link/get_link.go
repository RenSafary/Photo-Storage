package send_temp_link

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	//"github.com/gorilla/mux"
)

type DataForm struct {
	User     string `form:"user"`
	Url      string `form:"url"`
	Platform string `form:"platform"`
}

func HandleGetLink(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	err := r.ParseForm()
	if err != nil {
		http.Error(w, "Parsing error", http.StatusBadRequest)
		return
	}

	data := DataForm{
		User:     r.PostFormValue("user"),
		Url:      r.PostFormValue("url"),
		Platform: r.PostFormValue("platform"),
	}

	if data.User == "" || data.Url == "" || data.Platform == "" {
		http.Error(w, "Missing required fields", http.StatusBadRequest)
		return
	}

	fmt.Printf("Received: user=%s, url=%s, platform=%s\n", data.User, data.Url, data.Platform)

	shareURL := generateShareURL(data) // поменять на ссылку со своим доменом и в img вставлять её. добавить роутер для этого
	if shareURL == "" {
		http.Error(w, "Unsupported platform", http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":   "success",
		"message":  "File shared successfully",
		"shareURL": shareURL,
	})
}

func generateShareURL(data DataForm) string {
	var text string = "Hi! You can see my photo!"

	encodedURL := url.QueryEscape(data.Url)
	encodedText := url.QueryEscape(text)

	switch data.Platform {
	case "telegram":
		return fmt.Sprintf("https://t.me/share/url?url=%s&text=%s", encodedURL, encodedText)
	case "whatsapp":
		return fmt.Sprintf("https://wa.me/?text=%s%%20%s", encodedText, encodedURL)
	default:
		return ""
	}
}
