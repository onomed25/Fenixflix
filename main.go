package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/playwright-community/playwright-go"
)

type ResponseData struct {
	M3U8 string `json:"m3u8"`
	Erro string `json:"erro,omitempty"`
}

func extrairM3U8Streamberry(urlVideo string) (string, error) {
	pw, err := playwright.Run()
	if err != nil { return "", err }
	defer pw.Stop()

	browser, err := pw.Chromium.Launch(playwright.BrowserTypeLaunchOptions{
		Headless: playwright.Bool(true),
	})
	if err != nil { return "", err }
	defer browser.Close()

	context, err := browser.NewContext(playwright.BrowserNewContextOptions{
		UserAgent: playwright.String("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"),
					   ExtraHttpHeaders: map[string]string{
						   "Referer":         "https://streamberry.com.br/",
						   "Origin":          "https://streamberry.com.br",
						   "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
					   },
	})
	if err != nil { return "", err }

	page, err := context.NewPage()
	if err != nil { return "", err }

	var linkM3U8 string

	page.On("request", func(request playwright.Request) {
		url := request.URL()
		if strings.Contains(url, ".m3u8") && (strings.Contains(url, "master") || strings.Contains(url, "index")) && linkM3U8 == "" {
			linkM3U8 = url
		}
	})

	_, err = page.Goto(urlVideo, playwright.PageGotoOptions{
		WaitUntil: playwright.WaitUntilStateLoad,
		Timeout:   playwright.Float(30000),
	})

	for i := 0; i < 15; i++ {
		if linkM3U8 != "" { break }
		time.Sleep(1 * time.Second)
	}

	return linkM3U8, nil
}

func handleExtract(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	w.Header().Set("Content-Type", "application/json")

	if id == "" {
		json.NewEncoder(w).Encode(ResponseData{Erro: "ID não fornecido"})
		return
	}

	urlDoEmbed := fmt.Sprintf("https://byseraguci.com/e/%s", id)
	fmt.Printf("[GO] Trabalhando no ID: %s\n", id)

	m3u8, err := extrairM3U8Streamberry(urlDoEmbed)
	if err != nil {
		json.NewEncoder(w).Encode(ResponseData{Erro: err.Error()})
		return
	}

	json.NewEncoder(w).Encode(ResponseData{M3U8: m3u8})
}

func main() {
	// Isso tenta instalar o driver e o browser se eles não existirem
	err := playwright.Install()
	if err != nil {
		fmt.Printf("[GO] Aviso ao instalar Playwright: %v\n", err)
	}
	
	http.HandleFunc("/extract", handleExtract)
	fmt.Println("[GO] Servidor extrator rodando na porta 8080...")
	http.ListenAndServe(":8080", nil)
}
