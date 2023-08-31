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
  const [isLoading, setIsLoading] = useState(true);

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
    setTimeout(() => {
      // 设置clothesData为模拟的数据

      setIsLoading(false); // 数据加载完成后停止显示加载图标
    }, 3000); // 4秒后加载数据
  }, [id]);
  console.log(clothesData);

  if (isLoading) {
    return (
      <div className={styles.ci}>
        <img
          src="/Gootdle_logo_large.png"
          alt="gootdle"
          width={250}
          height={83}
        />
      </div>
    );
  }

  const nextImage = async () => {
    const nextIndex =
      (currentImageIndex + 1) % clothesData.recommendation_slot.length;

    setCurrentImageIndex(nextIndex);
  };

  const prevImage = async () => {
    const prevIndex =
      currentImageIndex === 0
        ? clothesData.recommendation_slot.length - 1
        : currentImageIndex - 1;
    setCurrentImageIndex(prevIndex);
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
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "/";
      }
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
          <Image
            src="/Gootdle_logo_large.png"
            alt="gootdle"
            width={250}
            height={83}
            onClick={goToHomePage}
            className={styles.gootdle}
          />

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
        <Image
          src="/Polygon 4.png"
          alt="TRI"
          width={50}
          height={97}
          onClick={prevImage}
          className={styles.tri}
          style={{ cursor: "pointer" }}
        />
        <div className={styles.cloth}>
          <img
            src={clothesData.suit[currentImageIndex]}
            alt="TRI"
            width={100}
            height={97}
          />

          <div className={styles.info}>HAVE A NICE DAY!</div>
        </div>
        <Image
          src="/Polygon 1.png"
          alt="TRI"
          width={50}
          height={97}
          onClick={nextImage}
          className={styles.tri}
          style={{ cursor: "pointer" }}
        />
      </div>
      <button className={styles.comfirm} onClick={openCustomDialog}>
        <div className={styles.word}>COMFIRM</div>
      </button>
    </div>
  );
};

export default ClothesDetailPage;
