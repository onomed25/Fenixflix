package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/playwright-community/playwright-go"
)

type ResponseData struct {
	M3U8 string `json:"m3u8"`
	Erro string `json:"erro,omitempty"`
}

// --- Código de Extração Original ---
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
		reqUrl := request.URL()
		if strings.Contains(reqUrl, ".m3u8") && (strings.Contains(reqUrl, "master") || strings.Contains(reqUrl, "index")) && linkM3U8 == "" {
			linkM3U8 = reqUrl
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

	// Em vez de devolver o link direto, devolvemos o link do nosso proxy
	// r.Host pega automaticamente o IP/Domínio e porta do seu servidor Go
	proxyURL := fmt.Sprintf("http://%s/proxy?url=%s", r.Host, url.QueryEscape(m3u8))

	json.NewEncoder(w).Encode(ResponseData{M3U8: proxyURL})
}

// --- NOVO: Sistema de Proxy HLS ---
func handleProxy(w http.ResponseWriter, r *http.Request) {
	targetURL := r.URL.Query().Get("url")
	if targetURL == "" {
		http.Error(w, "Falta o parâmetro URL", http.StatusBadRequest)
		return
	}

	req, err := http.NewRequest("GET", targetURL, nil)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Cabeçalhos essenciais para enganar a SprintCDN
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
	req.Header.Set("Referer", "https://streamberry.com.br/")
	req.Header.Set("Origin", "https://streamberry.com.br")

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, "Erro ao contactar CDN: "+err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// Copiar os cabeçalhos da resposta da CDN para o Stremio
	for k, vv := range resp.Header {
		for _, v := range vv {
			w.Header().Add(k, v)
		}
	}
	// Permite que o Stremio web leia o proxy sem problemas de CORS
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.WriteHeader(resp.StatusCode)

	// Se for uma playlist .m3u8, precisamos reescrever os links internos
	if strings.Contains(targetURL, ".m3u8") || strings.Contains(resp.Header.Get("Content-Type"), "mpegurl") {
		bodyBytes, _ := io.ReadAll(resp.Body)
		linhas := strings.Split(string(bodyBytes), "\n")

		baseURL, _ := url.Parse(targetURL)

		for i, linha := range linhas {
			linha = strings.TrimSpace(linha)
			// Se a linha não for um comentário e não estiver vazia, é um link
			if linha != "" && !strings.HasPrefix(linha, "#") {
				// Resolve o link (suporta links relativos e absolutos)
				chunkURL, _ := baseURL.Parse(linha)
				// Substitui pelo link do nosso próprio proxy
				linhas[i] = fmt.Sprintf("http://%s/proxy?url=%s", r.Host, url.QueryEscape(chunkURL.String()))
			}
		}
		// Envia a playlist modificada para o Stremio
		w.Write([]byte(strings.Join(linhas, "\n")))
	} else {
		// Se não for m3u8 (se for um ficheiro .ts), retransmite o vídeo diretamente (Stream)
		io.Copy(w, resp.Body)
	}
}

func main() {
	err := playwright.Install()
	if err != nil {
		fmt.Printf("[GO] Aviso ao instalar Playwright: %v\n", err)
	}

	http.HandleFunc("/extract", handleExtract)
	http.HandleFunc("/proxy", handleProxy) // Regista a nova rota

	fmt.Println("[GO] Servidor extrator e proxy rodando na porta 8080...")
	http.ListenAndServe(":8080", nil)
}
