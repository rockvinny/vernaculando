export default async function handler(req, res) {

  const FEED_URL =
    "https://rss.app/feeds/v1.1/4aUmbnZaAmP38RRZ.json";

  const response = await fetch(FEED_URL);
  const data = await response.json();

  const alphabet = {};

  data.items.forEach(item => {

    const text = (item.content_text || "").toUpperCase();

    const tags = text.match(/#([A-Z])\b/g) || [];

    tags.forEach(tag => {

      const letter = tag.replace("#", "");

      if (!alphabet[letter]) {
        alphabet[letter] = [];
      }

      alphabet[letter].push(item.image);

    });

  });

  res.status(200).json(alphabet);

}
