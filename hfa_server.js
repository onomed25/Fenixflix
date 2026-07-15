require('dotenv').config();
const http = require('http');
const hfa = require('./hfa.js');

// Inicializa os provedores e os bancos de dados em background
hfa.initProviders();
hfa.ensureAllCatalogsSequentially().catch(err => console.error("[HFA] Erro no prewarm:", err));

const server = http.createServer(async (req, res) => {
    if (req.method === 'POST' && req.url === '/search') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', async () => {
            try {
                const { titles, contentType, season, episode, year } = JSON.parse(body);
                const results = await hfa.searchAllProviders(titles, contentType, season, episode, year);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(results));
            } catch (err) {
                console.error(err);
                res.writeHead(500);
                res.end(JSON.stringify({ error: err.message }));
            }
        });
    } else {
        res.writeHead(404);
        res.end();
    }
});

const PORT = 38472;
server.listen(PORT, '127.0.0.1', () => {
    console.log(`[HFA Internal Server] Listening on ${PORT}`);
});
