import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import styles from "./homepage.module.scss";

const ClothesDetailPage = () => {
  const router = useRouter();
  const { id } = router.query; // 获取动态路由中的id参数
  console.log(id);

  const [clothesData, setClothesData] = useState(null);

  useEffect(() => {
    // 在这里根据id参数获取特定衣物的数据，您可以使用您的数据源来替换这里的代码
    // 例如：根据id从API获取衣物数据并将其存储在clothesData状态中
    if (id) {
      fetch(`/api/getClothes/${id}`)
        .then((response) => response.json())
        .then((data) => setClothesData(data))
        .catch((error) => console.error("Error fetching data:", error));
    }
  }, [id]);
  console.log(clothesData);

  



  if (!clothesData) {
    return <p>Loading...</p>;
  }

  // 渲染衣物详细信息
  return (
    <div>
      <div className={styles.closet}>
        <div className={styles.smart}>
          <div className={styles.wordup}>Gootdle </div>
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

      
      <h1>{clothesData.color_name}</h1>
      <p>Color: {clothesData.slot_location}</p>
      {/* 其他衣物信息 */}
    </div>
  );
};

export default ClothesDetailPage;
