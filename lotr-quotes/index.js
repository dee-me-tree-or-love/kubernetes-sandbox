const express = require("express")

const quotes = require("./quotes.json");
const config = require("./config.json");


const createApp = (config) => {
    return { app: express(), port: config.port || 3000, appName: config.appName || "" };
};

const createQuote = (quoteItem) => {
    return {
        "quote": quoteItem ? quoteItem.quote || "" : "N/A",
        "author": quoteItem ? quoteItem.author || "unknown" : "N/A"
    };
    //return { "quote": "N/A" };
};

const selectRandomElement = (collection, createElement) => {
    const index = Math.floor(Math.random() * collection.length);
    return createElement(collection[index]);
};

const getReadyIndicator = (quotes) => {
    return { "ready": quotes.length > 0 };
};

const { app, port, appName } = createApp(config);

app.get("/quote", (req, res) => res.json(
    selectRandomElement(quotes, createQuote)
));

app.get("/ready", (req, res) => res.json(
    getReadyIndicator(quotes)
));

app.listen(port, () => console.log(`"${appName}" listening on port ${port}!`));

