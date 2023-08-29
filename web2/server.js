const express = require("express");
const next = require("next");

const dev = process.env.NODE_ENV !== "production";
const app = next({ dev });
const handle = app.getRequestHandler();

const { createClient } = require("@supabase/supabase-js");
const SERVICE_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNveWF1ZnB0cm1ubGdpZ2FkbmNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MTg5NTg3NCwiZXhwIjoyMDA3NDcxODc0fQ.s17n0nPQBcADiy5xxvVXEeNz6Kzc9QzHNq40p3nThjM";

const SUPABASE_URL = "https://coyaufptrmnlgigadncn.supabase.co";

const supabase = createClient(SUPABASE_URL, SERVICE_KEY);

const server = express(); // 定義 Express.js 伺服器

server.get("/api/getData", async (req, res) => {
  try {
    // 使用 Supabase 客戶端從數據庫中檢索數據
    let { data: closet, error } = await supabase.from("closet").select("*");

    if (error) {
      throw error;
    }

    res.status(200).json(closet); // Use 'closet' instead of 'data'
  } catch (error) {
    res.status(500).json({ error: "An error occurred." });
  }
});
// server.get("/api/getClothes/:id", async (req, res) => {
//   try {
//     const { id } = req.params;
//     let { data: clothes, error } = await supabase
//       .from("closet")
//       .select("*")
//       .eq("id", id);

//     if (error) {
//       throw error;
//     }
//     if (clothes.length === 0) {
//       res.status(404).json({ error: "Clothing not found." });
//     } else {
//       res.status(200).json(clothes[0]); // 返回特定 ID 的衣物信息
//     }
//   } catch (error) {
//     res.status(500).json({ error: "An error occurred." });
//   }
// });

// andrew 注意這裡
const axios = require('axios');

server.get("/api/getClothes/:id", async (req, res) => {
  try {
    const { id } = req.params;
    let { data: clothes, error } = await supabase
      .from("closet")
      .select("*")
      .eq("id", id);

    if (error) {
      throw error;
    }
    if (clothes.length === 0) {
      res.status(404).json({ error: "Clothing not found." });
    } else {
      // 獲取slot_location
      const slotLocation = clothes[0].slot_location;

      // 向樹莓派後端發送POST請求
      const raspberryPiEndpoint = 'http://raspberry-pi-ip:port'; // 替換為你的樹莓派的IP地址和端口
      const requestBody = { slot_location: slotLocation };

      // 發送POST請求
      await axios.post(`${raspberryPiEndpoint}/your-endpoint`, requestBody);

      res.status(200).json(clothes[0]); // 返回特定ID的衣物信息
    }
  } catch (error) {
    res.status(500).json({ error: "An error occurred." });
  }
});

app.prepare().then(() => {
  // 處理 Next.js 頁面路由
  server.all("*", (req, res) => {
    return handle(req, res);
  });

  server.listen(3000, (err) => {
    if (err) throw err;
    console.log("> Ready on http://localhost:3000");
  });
});
