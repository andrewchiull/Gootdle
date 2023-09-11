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
    // if (typeof window !== "undefined") {
    //   window.onload = function () {
    //     // 页面已加载完成，可以执行您的代码
    //     // 例如，执行滚动操作
    //     window.scrollTo(0, 700); // 将页面滚动到指定高度
    //   };
    // }
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
  const goToHomePage = () => {
    router.push("/"); // 这里的 '/' 表示首页的路由路径
  };

  return (
    <>
      <div className={styles.root}>
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

        <div>
          <div>
            <div className={styles.top}>TOP</div>
            <div className={styles.all}>
              {topClothes.length > 0 && currentIndex < topClothes.length ? (
                topClothes.map((clothingItem) => (
                  <div key={clothingItem.id} className={styles.cloth}>
                    {clothingItem.state == "OUT" ? (
                      <>
                        <img
                          src={clothingItem.photo_path}
                          alt="TRI"
                          width={100}
                          height={97}
                        />

                        <div className={styles.info}>{clothingItem.state}</div>
                      </>
                    ) : (
                      <div
                        onClick={() => goToClothesPage(clothingItem.id)}
                        className={styles.cloth}
                      >
                        <img
                          src={clothingItem.photo_path}
                          alt="TRI"
                          width={100}
                          height={97}
                        />
                        <div className={styles.info}>{clothingItem.state}</div>
                      </div>
                    )}
                    {/* <div
                      onClick={() => goToClothesPage(clothingItem.id)}
                      className={styles.cloth}
                    >
                      <img
                        src={clothingItem.photo_path}
                        alt="TRI"
                        width={100}
                        height={97}
                      />
                      <div className={styles.info}>{clothingItem.state}</div>
                    </div> */}
                  </div>
                ))
              ) : (
                <div className={styles.skeleton}></div>
              )}
            </div>
          </div>
          <div>
            <div className={styles.bottom}>BOTTOM</div>
            <div className={styles.all}>
              {bottomClothes.length > 0 &&
              currentIndexbottom < bottomClothes.length ? (
                bottomClothes.map((clothingItem) => (
                  <div key={clothingItem.id} className={styles.cloth}>
                    <div
                      onClick={() => goToClothesPage(clothingItem.id)}
                      className={styles.cloth}
                    >
                      <img
                        src={clothingItem.photo_path}
                        alt="TRI"
                        width={100}
                        height={97}
                      />
                      <div className={styles.info}>{clothingItem.state}</div>
                    </div>
                  </div>
                ))
              ) : (
                <div className={styles.skeleton}></div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default HomePage;
