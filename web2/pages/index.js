import React, { useEffect, useState } from "react";
import Image from "next/image";
import styles from "./homepage.module.scss";
import Link from "next/link";
import { useRouter } from "next/router";

const HomePage = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/api/getData")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);
  console.log(data);
  const bottomClothes = data.filter((item) => item.cloth_type === "bottom");
  const topClothes = data.filter((item) => item.cloth_type === "top");

  // 衣服
  console.log(topClothes);
  const [currentIndex, setCurrentIndex] = useState(0); // Track current index
  const handleNextClick = async () => {
    const nextIndex = (currentIndex + 1) % topClothes.length;
    await preloadImage(topClothes[nextIndex].photo_path);
    setCurrentIndex(nextIndex);
  };

  const handlePrevClick = async () => {
    const prevIndex =
      currentIndex === 0 ? topClothes.length - 1 : currentIndex - 1;
    await preloadImage(topClothes[prevIndex].photo_path);
    setCurrentIndex(prevIndex);
  };

  // 褲子
  const [currentIndexbottom, setCurrentIndexbottom] = useState(0); // Track current index
  const handleNextClickbottom = () => {
    setCurrentIndexbottom(
      (prevIndex) => (prevIndex + 1) % bottomClothes.length
    );
  };

  const handlePrevClickbottom = () => {
    setCurrentIndexbottom((prevIndex) =>
      prevIndex === 0 ? bottomClothes.length - 1 : prevIndex - 1
    );
  };

  const preloadImage = (url) => {
    return new Promise((resolve, reject) => {
      const img = new window.Image(); // Use the regular Image object
      img.src = url;
      img.onload = resolve;
      img.onerror = reject;
    });
  };

  const router = useRouter();

  const goToClothesPage = (id) => {
    router.push(`/clothes/${id}`);
  };

  // const goToClothesPage = async (id) => {
  //   try {
  //     // 向后端发送请求，更改 Supabase 数据
  //     const response = await fetch(`/api/updateClothes/${id}`, {
  //       method: "POST", // 使用 POST 请求
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         newData: "out",
  //       }),
  //     });

  //     if (!response.ok) {
  //       // 请求失败，可以处理错误
  //       throw new Error("Network response was not ok");
  //     }

  //     // 请求成功后，导航到新页面
  //     router.push(`/clothes/${id}`);
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  return (
    <>
      <div className={styles.root}>
        <div className={styles.closet}>
          <div className={styles.smart}>
            <div className={styles.wordup}>
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

        <div>
          <div>
            <div className={styles.top}>Top</div>
            <div className={styles.all}>
              <Image
                src="/Polygon 4.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handlePrevClick}
                className={styles.tri}
              />

              {topClothes.length > 0 && currentIndex < topClothes.length ? (
                <div key={topClothes[currentIndex].id}>
                  <div
                    className={styles.cloth}
                    onClick={() => goToClothesPage(topClothes[currentIndex].id)}
                  >
                    <div className={styles.cloth}>
                      <img
                        src={topClothes[currentIndex].photo_path}
                        alt="TRI"
                        width={100}
                        height={97}
                      />
                      <div className={styles.info}>
                        {topClothes[currentIndex].color_name}
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <p>No data available.</p>
              )}
              <Image
                src="/Polygon 1.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handleNextClick}
                className={styles.tri}
              />
            </div>
          </div>
          <div>
            <div className={styles.bottom}>BOTTOM</div>
            <div className={styles.all}>
              <Image
                src="/Polygon 4.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handlePrevClickbottom}
                className={styles.tri}
              />
              {bottomClothes.length > 0 &&
              currentIndexbottom < bottomClothes.length ? (
                <div key={bottomClothes[currentIndexbottom].id}>
                  <div className={styles.cloth}>
                    <img
                      src={bottomClothes[currentIndexbottom].photo_path}
                      alt="TRI"
                      width={100}
                      height={97}
                    />
                    <div className={styles.info}>
                      {bottomClothes[currentIndexbottom].color_name}
                    </div>
                  </div>
                </div>
              ) : (
                <p>No data available.</p>
              )}
              <Image
                src="/Polygon 1.png"
                alt="TRI"
                width={50}
                height={97}
                onClick={handleNextClickbottom}
                 className={styles.tri}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default HomePage;
