# Building a Multi-player Game with WebSockets

> Source: `Building a Multi-player Game with WebSockets.txt` · Transcript 7 of 43

## 📝 Description
A long live-coding session building a real-time **multiplayer browser game** from scratch with a Node.js **WebSocket** server and the **server-authoritative** model. Players click cells to color the board, and the player who owns the most cells wins.

## ⚠️ Problem
Several players must see the same game state in real time. If each client decides the outcome, they drift apart and can cheat.

## ✅ Solution
Keep one source of truth on the server. Clients send *intents* (clicks) over a persistent WebSocket, the server validates and updates the state, then broadcasts the new state to everyone.

## 🔍 Explanation
1. **Why WebSockets:** a persistent, bi-directional connection lets the server push updates at any time without repeated HTTP polling.
2. **Server-authoritative:** the client only says "player X clicked cell N". The server applies the rules and sends back the state.
3. **Game flow:** a client creates a game and gets a URL. Others open the URL and join. Each client is assigned a color. Clicks change cell colors, and the board is broadcast.
4. **Two servers:** one port serves the HTML page (Express), and another port runs the WebSocket server.
5. **Game state on the server:** a map of clients, a map of games and the board state. Joining, creating, playing and updating are message types.
6. **Debugging:** the session shows real errors (for example "cannot convert undefined or null to object") and how they appear when state isn't initialized.

## 💻 Relevant Code
Skeleton of the server pattern (illustrative, using the `ws` library):
```js
const WebSocket = require("ws");
const http = require("http");
const wss = new WebSocket.Server({ port: 9090 });
const clients = {}; const games = {};

wss.on("connection", (ws) => {
  const clientId = Math.random().toString(36).slice(2);
  clients[clientId] = { ws };
  ws.send(JSON.stringify({ method: "connect", clientId }));

  ws.on("message", (raw) => {
    const msg = JSON.parse(raw);
    if (msg.method === "play") {
      games[msg.gameId].state[msg.cellId] = msg.color;     // server decides
      for (const c of games[msg.gameId].clients)
        clients[c.clientId].ws.send(JSON.stringify({ method: "update", game: games[msg.gameId] }));
    }
  });
});
```

## 🤖 Claude's Notes
- Real games add a **tick loop** (broadcast at a fixed rate) instead of broadcasting on every click, to limit bandwidth.
- Validate every message on the server. Never trust client data, even the color or player id.

## 🎯 Key Takeaways
- WebSockets suit real-time two-way communication.
- The server must own the game state to prevent cheating and desync.
- Broadcast changes to all connected clients on each update.

## ❓ Questions
1. Why not let each client keep its own copy of the truth?
2. What does the server broadcast, and when?
3. Why use two ports in this demo?

## 🔁 Follow-up Questions
1. How would you handle a player disconnecting mid-game?
2. How would you scale this to many games across multiple servers?

## 🤔 Questions to Think About
- What changes if the game is fast-paced and latency matters (prediction, interpolation)?
- Where would WebSockets be a poor fit?
