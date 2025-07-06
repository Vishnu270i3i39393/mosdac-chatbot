const express = require("express");
const cors = require("cors");
const chatRoutes = require("./routes/chat");

const app = express();

// allow CORS
app.use(cors());
app.use(express.json());

// connect the /chat route
app.use("/chat", chatRoutes);

// dynamically use Render's PORT if provided
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
});

