export default async function handler(req, res) {

  const FEED_URL =
    "https://rss.app/feeds/v1.1/4aUmbnZaAmP38RRZ.json";

  const response = await fetch(FEED_URL);
  const data = await response.json();

  const alphabet = {};

  data.items.forEach(item => {

    const text = (item.content_text || "").toUpperCase();

    // pega SOMENTE hashtags de UMA letra (#A, #B, etc)
    const tags = (text.match(/#[A-Z]/g) || [])
      .map(t => t.replace("#", ""))
      .filter(t => /^[A-Z]$/.test(t));

    tags.forEach(letter => {

      if (!alphabet[letter]) {
        alphabet[letter] = [];
      }

      alphabet[letter].push(item.image);

    });

  });

  res.status(200).json(alphabet);

}
