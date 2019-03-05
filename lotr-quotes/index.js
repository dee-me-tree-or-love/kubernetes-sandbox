const express = require("express")

const quotes = require("./quotes.json");
const config = require("./config.json");


const createApp = (config) => {
    return { app: express(), port: config.port || 3000, appName: config.appName || "n/a" };
}

const createQuote = (quoteItem) => {
    return { "quote": quoteItem ? quoteItem.quote || "" : "n/a" };
}

const selectRanomElement = (collection, createElement) => {
    const index = Math.floor(Math.random() * collection.length);
    return createElement(collection[index]);
}


const { app, port, appName } = createApp(config);

app.get("/quote", (req, res) => res.json(
    selectRanomElement(quotes, createQuote)
))

app.listen(port, () => console.log(`"${appName}" listening on port ${port}!`));

