const express = require("express");
// const app = express();
const cors = require("cors");

// app.use(express.static("public"));
// app.use(express.urlencoded({ extended: true }));
// app.use(express.json());
// app.use(cors());

// app.set("view engine", "ejs");

// const userRouter = require("./routes/users");

// app.use("/users", userRouter);

// //app.listen(3000);

// const port = 4000;
// app.listen(port, () => {
//   console.log(`Server started on port ${port}`);
// });

// app.get("/", (req, res) => {
//   res.send("Hello World From Cafe Near U");
// });

const dev = process.env.NODE_ENV !== "production";
const app = next({ dev });
const handle = app.getRequestHandler();
const { createClient } = require("@supabase/supabase-js");

const supabaseUrl = "https://coyaufptrmnlgigadncn.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNveWF1ZnB0cm1ubGdpZ2FkbmNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTE4OTU4NzQsImV4cCI6MjAwNzQ3MTg3NH0.slmrVRDTouxBGMc2iByI_zN2vCpyMCZu8t66kiQY0Qk";
const supabase = createClient(supabaseUrl, supabaseKey);

server.get("/api/getData", async (req, res) => {
  try {
    // 使用 Supabase 客戶端從數據庫中檢索數據
    const { data, error } = await supabase.from("closet").select("*");

    if (error) {
      throw error;
    }

    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: "An error occurred." });
  }
});

app.prepare().then(() => {
  const server = express();

  // 定義自訂的 Express 路由或 API 請求處理

  // 處理 Next.js 頁面路由
  server.all("*", (req, res) => {
    return handle(req, res);
  });

  server.listen(3000, (err) => {
    if (err) throw err;
    console.log("> Ready on http://localhost:3000");
  });
});

// 其他路由設置...
