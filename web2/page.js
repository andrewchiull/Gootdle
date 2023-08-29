"use client";
import Image from "next/image";
import styles from "./homepage.module.scss";
import { useEffect, useState } from "react";

import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://coyaufptrmnlgigadncn.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNveWF1ZnB0cm1ubGdpZ2FkbmNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTE4OTU4NzQsImV4cCI6MjAwNzQ3MTg3NH0.slmrVRDTouxBGMc2iByI_zN2vCpyMCZu8t66kiQY0Qk";
const supabase = createClient(supabaseUrl, supabaseKey);

export default function Home() {
  const [clothingData, setClothingData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0); // Track current index
  // var cors = require("cors");
  useEffect(() => {
    // 发送 GET 请求并获取数据
    fetch("http://localhost:8000/data/")
      .then((response) => response.json())
      .then((data) => {
        console.log("host");
        console.log(data); // 在控制台中输出获取的数据
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  // 取得所有衣服資料
  useEffect(() => {
    async function fetchClothingData() {
      const { data, error } = await supabase.from("closet").select("*");
      if (error) {
        console.error("Error fetching data:", error);
      } else {
        setClothingData(data);
        console.log("clothingData");
        console.log(data);
      }
    }

    fetchClothingData();
  }, []);

  // 取得上衣資料
  const [topClothingData, setTopClothingData] = useState([]);

  useEffect(() => {
    async function fetchTopClothingData() {
      const { data, error } = await supabase
        .from("closet")
        .select("*")
        .eq("cloth_type", "top"); // Use eq to filter by cloth_type

      if (error) {
        console.error("Error fetching data:", error);
      } else {
        setTopClothingData(data);
      }
    }

    fetchTopClothingData();
  }, []);
  const handleNextClick = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % topClothingData.length);
  };

  // 按下確認按鈕更改資料庫資料
  const handleConfirmClick = async () => {
    // 取得目前顯示的衣物資料
    const currentClothing = topClothingData[currentIndex];

    // 更新資料庫中的資料
    try {
      const { data, error } = await supabase
        .from("closet")
        .update({ wore_times: currentClothing.wore_times + 1 }) // 假設有一個 worn_times 屬性用於記錄穿著次數
        .eq("id", currentClothing.id); // 根據 id 更新特定資料

      if (error) {
        console.error("Error updating data:", error);
      } else {
        console.log("Data updated successfully:", data);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  // useEffect(() => {
  //   // Subscribe to real-time changes of a specific table
  //   const subscription = supabase
  //     .from("closet")
  //     .on("INSERT", payload => {
  //       console.log("New record inserted:", payload.new);
  //       // Handle the new record
  //     })
  //     .on("UPDATE", payload => {
  //       console.log("Record updated:", payload.new);
  //       // Handle the updated record
  //     })
  //     .on("DELETE", payload => {
  //       console.log("Record deleted:", payload.old);
  //       // Handle the deleted record
  //     })
  //     .subscribe();

  //   return () => {
  //     // Unsubscribe when the component unmounts
  //     subscription.unsubscribe();
  //   };
  // }, []); // Empty dependency array to ensure subscription only happens once on initial render

  return (
    <div>
      <div className={styles.head}>
        <div className={styles.google}>
          <Image
            src="/image 1.png"
            alt="google Picture"
            width={120}
            height={80}
          />
        </div>
        <div className={styles.team}>HPS 2023 TEAM 8</div>
        <button className={styles.teammember}>
          <div className={styles.word}>TEAM MEMBER</div>
        </button>
      </div>
      <div className={styles.line}></div>
      <div className={styles.closet}>
        <div className={styles.smart}>
          <div className={styles.wordup}>SMART CLOSET </div>
          <div className={styles.worddown}>SMART YOUR EVERYDAY LIFE</div>
        </div>
        <div className={styles.season}>
          <div className={styles.word}>SPRING</div>
          <div className={styles.word}>SUMMER</div>
          <div className={styles.word}>AUTUMN</div>
          <div className={styles.word}>WINTER</div>
        </div>
      </div>
      <div className={styles.line}></div>
      <div className={styles.webmain}>
        <div className={styles.choose}>
          <div className={styles.topchoose}>
            <div className={styles.word}>TOP</div>
            <div className={styles.topitem}>
              <div className={styles.tri}>
                <Image src="/Polygon 4.png" alt="TRI" width={50} height={97} />
              </div>
              <div className={styles.cloth}>
                <Image
                  src={clothingData.photo_path}
                  alt="TRI"
                  width={50}
                  height={97}
                />
                <div className={styles.info}>
                  <div className={styles.detail}>
                    <div className={styles.bigname}>Red Long Sleeve Top</div>
                    <div className={styles.season}>WINTER</div>
                  </div>
                  {/* <div className={styles.time}>
                    <div className={styles.word}>WORE 3 TIMES</div>
                  </div> */}
                </div>
              </div>
              <div className={styles.tri2}>
                <Image src="/Polygon 1.png" alt="TRI" width={50} height={97} />
              </div>
            </div>
          </div>
          <div className={styles.topchoose}>
            <div className={styles.word}>BOTTOM</div>
            <div className={styles.topitem}>
              <div className={styles.tri}>
                <Image src="/Polygon 4.png" alt="TRI" width={50} height={97} />
              </div>
              <div className={styles.cloth}>
                <Image src="/image 4.png" alt="TRI" width={50} height={97} />
                <div className={styles.info}>
                  <div className={styles.detail}>
                    <div className={styles.bigname}>Red Long Sleeve Top</div>
                    <div className={styles.season}>WINTER</div>
                  </div>
                  {/* <div className={styles.time}>
                    <div className={styles.word}>WORE 3 TIMES</div>
                  </div> */}
                </div>
              </div>
              <div className={styles.tri2}>
                <Image src="/Polygon 1.png" alt="TRI" width={50} height={97} />
              </div>
            </div>
          </div>
        </div>
        <div className={styles.outcome}>
          <Image src="/image 4.png" alt="TRI" width={50} height={97} />
          <button className={styles.teammember} onClick={handleConfirmClick}>
            <div className={styles.word}>COMFIRM</div>
          </button>
        </div>
      </div>

      {/* {clothingData.map((item) => (
        <div key={item.id}>
          <Image src={item.photo_path} alt="TRI" width={50} height={97} />
          <div className={styles.info}>
            <div className={styles.detail}>
              <div className={styles.bigname}>{item.colo_namer}</div>
              <div className={styles.season}>{item.season}</div>
            </div>
          </div>
        </div>
      ))} */}
      <div>
        <div>
          <h1>Top Clothing Data</h1>
          <ul>
            {topClothingData.length > 0 &&
            currentIndex < topClothingData.length ? (
              <li key={topClothingData[currentIndex].id}>
                Color: {topClothingData[currentIndex].color_name}, Season:{" "}
                {topClothingData[currentIndex].season}
                <Image
                  src={topClothingData[currentIndex].photo_path}
                  alt="TRI"
                  width={100}
                  height={97}
                />
              </li>
            ) : (
              <li>No data available.</li>
            )}
          </ul>

          <button onClick={handleNextClick}>Next</button>
        </div>
      </div>
    </div>
  );
}
