import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import styles from "./homepage.module.scss";
import Image from "next/image";
import Swal from "sweetalert2";
const axios = require("axios");

const ClothesDetailPage = () => {
  const router = useRouter();
  const { id } = router.query; // 获取动态路由中的id参数
  console.log(id);

  const [clothesData, setClothesData] = useState(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    if (id) {
      // 发送 GET 请求到服务器获取衣物数据
      fetch(`/api/getClothes/${id}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => setClothesData(data))
        .catch((error) => console.error("Error fetching data:", error));
    }
  }, [id]);
  console.log(clothesData);

  if (!clothesData) {
    return <p>Loading...</p>;
  }

  const nextImage = () => {
    setCurrentImageIndex((prevIndex) => (prevIndex < 2 ? prevIndex + 1 : 0));
    console.log(clothesData.recommendation_slot[currentImageIndex]);
  };

  // 切换到上一张图片
  const prevImage = () => {
    setCurrentImageIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : 2));
    console.log(clothesData.recommendation_slot[currentImageIndex]);
  };

  const openCustomDialog = () => {
    const slotLocation = clothesData.recommendation_slot[currentImageIndex];
    const recommend = [];

    // 向樹莓派後端發送POST請求
    const postData = {
      slot: slotLocation,
      recommendations: recommend,
    };
    axios
      .post("http://172.20.10.10:8000/items/confirm", postData, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        // 请求成功的处理逻辑
        console.log("响应数据:", response.data);
      })
      .catch((error) => {
        // 请求失败的处理逻辑
        console.error("请求错误:", error);
      });
    Swal.fire({
      title: "THE OUTFIT IS ON THE WAY !",
      text: "HAVE A NICE DAY !",
      background: "#FAFAF5",
      confirmButtonText: "SURE!",
      confirmButtonColor: "#426B1F",
    });
  };

  const goToHomePage = () => {
    router.push("/"); // 这里的 '/' 表示首页的路由路径
  };

  const send = () => {
    if (id) {
      // 发送 GET 请求到服务器获取衣物数据
      fetch(`/api/se/${id}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => setClothesData(data))
        .catch((error) => console.error("Error fetching data:", error));
    }
  };
  return (
    <div>
      <div className={styles.closet}>
        <div className={styles.smart}>
          <div
            className={styles.wordup}
            style={{ cursor: "pointer" }}
            onClick={goToHomePage}
          >
            <span className={styles.gootdleletter}>G</span>
            <span className={styles.gootdleletter}>o</span>
            <span className={styles.gootdleletter}>o</span>
            <span className={styles.gootdleletter}>t</span>
            <span className={styles.gootdleletter}>d</span>
            <span className={styles.gootdleletter}>l</span>
            <span className={styles.gootdleletter}>e</span>
          </div>
          <div className={styles.worddown}>SMART DRESSING ZERO MESSING</div>
        </div>
      </div>
      <div className={styles.line}></div>
      <div className={styles.season}>
        <div className={styles.word}>SPRING</div>
        <div className={styles.word}>SUMMER</div>
        <div className={styles.word}>AUTUMN</div>
        <div className={styles.word}>WINTER</div>
      </div>
      <div className={styles.line}></div>
      <div className={styles.all}>
        <div className={styles.cloth}>
          <div className={styles.butt}>
            <div
              className={styles.image}
              onClick={prevImage}
              style={{ cursor: "pointer" }}
            />

            <img
              src={clothesData.suit[currentImageIndex]}
              alt="TRI"
              width={100}
              height={97}
            />
            <div
              className={styles.image}
              onClick={nextImage}
              style={{ cursor: "pointer" }}
            />
          </div>
          <div className={styles.info}>HAVE A NICE DAY!</div>
        </div>
      </div>
      <button className={styles.comfirm} onClick={openCustomDialog}>
        <div className={styles.word}>COMFIRM</div>
      </button>
    </div>
  );
};

export default ClothesDetailPage;
