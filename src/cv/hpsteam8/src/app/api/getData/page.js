import db from '../../db.js'; // 根据实际路径修改

export default async function handler(req, res) {
  try {
    // 使用 await 关键字来等待数据库查询的结果
    console.log('1');
    const results = await new Promise((resolve, reject) => {
      // 假设你的数据库查询方法为 queryColorData，需要根据实际情况修改
      db.query('SELECT * FROM colors', (error, results) => {
        if (error) {
          
          reject(error);
        } else {
          console.log('2');
          resolve(results);
        }
      });
    });

    // 返回查询结果作为 JSON 响应
    res.status(200).json(results);
    console.log(results);
  } catch (error) {
    // 处理错误情况，返回错误信息作为 JSON 响应
    res.status(500).json({ error: 'Database error' });
  }
}
