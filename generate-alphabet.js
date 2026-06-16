
const fs = require("fs");

const files = ["posts.json", "posts_1.json"];

const alphabet = {};

function safeArray(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (data.items) return data.items;
  return [data];
}

function processPosts(json) {
  const posts = safeArray(json);

  for (const post of posts) {

    const caption = (
      post?.string_map_data?.Caption?.value ||
      post?.title ||
      post?.caption ||
      ""
    ).toUpperCase();

    const tags = caption.match(/#[A-Z]/g) || [];

    const uri = post?.uri;
    if (!uri) continue;

    const filename = uri.split("/").pop();

    const imageUrl = "/imagens/" + filename;

    for (const tag of tags) {
      const letter = tag.replace("#", "");

      if (!alphabet[letter]) {
        alphabet[letter] = [];
      }

      alphabet[letter].push(imageUrl);
    }
  }
}

for (const file of files) {
  if (!fs.existsSync(file)) continue;

  const raw = fs.readFileSync(file, "utf8");
  const json = JSON.parse(raw);

  processPosts(json);
}

fs.writeFileSync(
  "alphabet.json",
  JSON.stringify(alphabet, null, 2)
);

console.log("✔ alphabet.json gerado com sucesso");
