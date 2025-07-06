const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");
const Fuse = require("fuse.js");

// load the generated Q&A pairs
const qaPairsPath = path.join(__dirname, "../data/mosdac_qa_pairs.json");
let qaPairs = [];

try {
  qaPairs = JSON.parse(fs.readFileSync(qaPairsPath, "utf-8"));
  console.log(`✅ Loaded ${qaPairs.length} Q&A pairs`);
} catch (err) {
  console.error("⚠️ Could not load mosdac_qa_pairs.json:", err.message);
}

// set up Fuse with a higher threshold (more fuzzy)
const fuse = new Fuse(qaPairs, {
  keys: ["question"],
  includeScore: true,
  threshold: 0.6,  // more forgiving
});

router.post("/", (req, res) => {
  const userMessage = req.body.message;
  if (!userMessage) {
    return res.status(400).json({ answer: "No message provided." });
  }

  // fuzzy search
  const results = fuse.search(userMessage);

  console.log("🔍 Fuse results for:", userMessage, results);

  if (results.length > 0) {
    res.json({ answer: results[0].item.answer });
  } else {
    res.json({ answer: "Sorry, I could not find a relevant answer." });
  }
});

module.exports = router;
